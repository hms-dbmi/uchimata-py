import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import bioframe

    dir(bioframe)
    print(bioframe.__file__)
    # bioframe.__version__
    return (bioframe,)


@app.cell
def _(bioframe):
    assembly = "hg38"
    chromsizes = bioframe.fetch_chromsizes(assembly)
    chromsizes.tail()
    return


@app.cell
def _(bioframe):
    df2 = bioframe.from_any(
        [['chr1', 4, 8],
         ['chr1', 10, 11]],
        name_col='chrom')
    return


@app.cell
def _(bioframe):
    ctcf_peaks = bioframe.read_table(
        "https://www.encodeproject.org/files/ENCFF401MQL/@@download/ENCFF401MQL.bed.gz",
        schema="narrowPeak",
    )
    ctcf_peaks.head()
    return


@app.cell
def _(bioframe):
    genes_url = (
        "https://hgdownload.soe.ucsc.edu/goldenpath/hg38/bigZips/genes/hg38.ensGene.gtf.gz"
    )
    genes = bioframe.read_table(genes_url, schema="gtf").query('feature=="CDS"')

    genes.head()
    return (genes,)


@app.cell
def _(genes):
    type(genes)
    return


@app.cell
def _(bioframe, genes):
    bioframe.is_bedframe(genes)
    return


@app.cell
def _():
    import requests

    def fetchFile(url):
        response = requests.get(url)
        if (response.status_code == 200):
            # print(response.content[0:10])
            file = response.content
            return file
        else:
            print("Error fetching the remote file")
            return None

    # url = "https://pub-5c3f8ce35c924114a178c6e929fc3ac7.r2.dev/Tan-2018_GSM3271347_gm12878_01.arrow"
    url = "https://pub-5c3f8ce35c924114a178c6e929fc3ac7.r2.dev/Stevens-2017_GSM2219497_Cell_1_model_1.arrow"

    model = fetchFile(url)
    return (model,)


@app.cell
def _(bioframe, model):
    import uchimata as uchi

    df3 = bioframe.from_any(
        [['chr a', 3000000, 5000000],
         ['chr b', 3000000, 5000000]],
        name_col='chrom')

    submodel = uchi.select_bioframe(model, df3)
    w2 = uchi.Widget(structure=submodel)
    w2
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
