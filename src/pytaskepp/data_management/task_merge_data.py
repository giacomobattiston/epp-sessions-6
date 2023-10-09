from pathlib import Path

import pandas as pd

PICKLE_DATA = Path(__file__).parent / "bld"
BLD = Path(__file__).parent / "bld"


def task_clean_data(
    election_file=PICKLE_DATA / "elections_results.pkl",
    deficit_file=PICKLE_DATA / "deficits.pkl",
    produces=BLD / "elections_results.pkl",
):
    raw = pd.read_stata(raw_file, convert_categoricals=False)
    metadata = pd.io.stata.StataReader(raw_file)
    clean = _clean_data(raw, metadata)
    clean.to_pickle(produces)

def _clean_data(raw, metadata):
    df = pd.DataFrame(index=raw.index)
    for old, new in {
        "Country": "country",
        "Nuts_id": "nuts_id",
        "Name": "nuts_name",
    }.items():
        df[new] = raw[old].astype(pd.CategoricalDtype())
    df["year"] = raw["Year"].astype(pd.Int16Dtype())
    df["election_type"] = _convert_election_cats(
        raw_sr=raw["ElectionType"],
        labels_dict=metadata.value_labels()["ElectionType"],
    )
    df["number_eligible_voters"] = _round_to_uint32(raw["EligibleVoters"])
    df["number_valid_votes"] = _round_to_uint32(raw["Valid"])
    df["number_parties_effective"] = raw["HHI"]
    df["number_votes_far_right"] = _round_to_uint32(raw["Far_Right"])
    df["number_votes_far_left"] = _round_to_uint32(raw["Far_Left"])
    df["share_votes_far_right"] = raw["Far_Right_share"]
    df["share_votes_far_left"] = raw["Far_Left_share"]
    df["share_votes_far_any"] = raw["Far_share"]
    df["share_voter_turnout"] = raw["Turnout"]
    df["number_votes_far_any_incumbent"] = _round_to_uint32(raw["F0Far_Incumbent"])
    df["pm_party_orientation"] = _pm_party_orientation(raw["left"])
    return df


def _convert_election_cats(raw_sr, labels_dict):
    election_cats = labels_dict.copy()
    for i, to_append in (5, " A"), (7, " B"):
        election_cats[i] += to_append
        sr = raw_sr.astype(pd.Int8Dtype()).astype(pd.CategoricalDtype())
    return sr.cat.rename_categories(election_cats)


def _round_to_uint32(sr):
    return sr.round().astype(pd.UInt32Dtype())


def _pm_party_orientation(pm_party_left):
    sr = pm_party_left.astype(pd.Int8Dtype()).astype(pd.CategoricalDtype())
    return sr.cat.rename_categories(
        {0: "Other", 1: "Left-leaning"},
    )