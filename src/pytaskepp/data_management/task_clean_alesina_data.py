from pathlib import Path

import pandas as pd

ORIGINAL_DATA = Path(__file__).parent / "original_data"
BLD = Path(__file__).parent / "bld"


def task_clean_alesina_data(
    raw_file=ORIGINAL_DATA / "Alesina.xlsx",
    produces=BLD / "deficits.pkl",
):
    raw = pd.read_excel(
        raw_file,
        sheet_name="MacroData",
    )
    clean = _clean_data(raw)
    clean.to_pickle(produces)


def _clean_data(raw):
    df = pd.DataFrame(index=raw.index)
    df["country"] = raw["Unnamed: 1"]
    df["year"] = raw["Year"]
    df["raw_deficit"] = raw["deficit"]
    df["primary_deficit"] = raw["primary_def"]
    return df
