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
    return


if __name__ == "__main__":
    app.run()
