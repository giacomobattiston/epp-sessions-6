from pathlib import Path

import pandas as pd
pd.options.mode.copy_on_write = True
pd.options.future.infer_string = False
pd.options.plotting.backend = "plotly"

BLD = Path(__file__).parent / "bld"

# create products dictionary for all 6 combinations of deficits and share
deficits_columns = ['raw_deficit', 'primary_deficit']
share_far_columns = ["share_votes_far_right","share_votes_far_left","share_votes_far_any",]
products = {}
for i_def in range(len(deficits_columns)):
    def_name = deficits_columns[i_def].split("_")[0] + "deficit"
    for i_sha in range(len(share_far_columns)):
        product_name = "scatter-" + deficits_columns[i_def] + "-" + share_far_columns[i_sha]
        product_path = Path(__file__).parent / "figures" / f"{product_name}.pdf"
        products[product_name]=product_path

def task_create_scatterplots(
    merged_file =BLD / "merged_data.pkl",
    produces=products,
):
    merged = pd.read_pickle(merged_file)
    only_elections = merged[merged["election_type"].notna()]
    for combination, fig_file in produces.items():
        deficit = combination.split("-")[1]
        share = combination.split("-")[2]
        fig = only_elections.plot.scatter(x=deficit, y=share, color="country")
        fig.write_image(fig_file)