import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _(genes_df, mo):
    gene_options = genes_df["gene_name"].to_list()
    dropdown = mo.ui.dropdown(options=gene_options, value="ATR", label="Choose gene:")
    dropdown
    return


@app.cell
def _(model, uchi):
    vc = {
        "color": "silver",
        "scale": 0.001, "links": True, "mark": "sphere"
    }

    w4 = uchi.Widget(model, viewconfig=vc)
    w4
    return


@app.cell
def _(pd):
    genesListFileName = "./sample_data/sample-genes.csv"
    genes_df = pd.read_csv(genesListFileName)
    genes_df = genes_df.rename(columns={"chr": "chrom"}) # needed to be considered a bioframe dataframe
    genes_df
    return (genes_df,)


@app.cell
def _(fetchFile):
    url = "https://pub-5c3f8ce35c924114a178c6e929fc3ac7.r2.dev/Tan-2018_GSM3271347_gm12878_01.arrow"
    model = fetchFile(url)
    return (model,)


@app.cell
def _(requests):
    def fetchFile(url):
        response = requests.get(url)
        if (response.status_code == 200):
            file = response.content
            return file
        else:
            print("Error fetching the remote file")
            return None
    return (fetchFile,)


@app.cell
def _():
    import numpy as np
    import bioframe
    import uchimata as uchi
    import requests
    import marimo as mo
    import pandas as pd
    return mo, pd, requests, uchi


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
