import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _(pd):
    filepath = "./sample_data/Table_S1_pgp1_data_table.csv"

    data_df = pd.read_csv(filepath)
    data_df
    return (data_df,)


@app.cell
def _(data_df):
    # rename columns
    data_df_renamed = data_df.copy()
    data_df_renamed = data_df_renamed.rename(columns={'x_um': 'x', 'y_um': 'y', 'z_um': 'z'})

    # change type of chr field
    data_df_renamed['hg38_chr'] = 'chr' + data_df_renamed['hg38_chr'].astype(str)

    data_df_renamed
    return (data_df_renamed,)


@app.cell
def _(data_df_renamed, uchi):
    vc = {
        "color": {

            "field": "hg38_chr",
            "colorScale": "Spectral"
        }, 
        "scale": 0.01, "links": False, "mark": "sphere"
    }

    w_final = uchi.Widget(data_df_renamed, viewconfig=vc)
    w_final
    return


@app.cell
def _():
    import pyarrow as pa
    import pyarrow.ipc as ipc
    import pandas as pd


    import uchimata as uchi
    return pd, uchi


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
