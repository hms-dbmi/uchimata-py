import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import bioframe
    return (bioframe,)


@app.cell
def _(bioframe):
    ctcf_peaks = bioframe.read_table(
        "https://www.encodeproject.org/files/ENCFF401MQL/@@download/ENCFF401MQL.bed.gz",
        schema="narrowPeak",
    )
    ctcf_peaks.head()
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
    return (uchi,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## mouse genome""")
    return


@app.cell
def _(bioframe):
    assembly_mouse = "mm10"
    chromsizes_mouse = bioframe.fetch_chromsizes(assembly_mouse)
    chromsizes_mouse
    return (chromsizes_mouse,)


@app.cell
def _(bioframe):
    # taken from here: https://www.encodeproject.org/files/ENCFF871VGR/
    mouse_genes_url = "https://www.encodeproject.org/files/ENCFF871VGR/@@download/ENCFF871VGR.gtf.gz"
    mouse_genes = bioframe.read_table(mouse_genes_url, schema="gtf").query('feature=="CDS"')

    # mouse_genes.head()
    mouse_genes
    return (mouse_genes,)


@app.cell
def _(mouse_genes):
    # mouse_genes_chr1 = mouse_genes.query('chrom=="chr1"')
    mouse_genes_chr1 = mouse_genes
    mouse_genes_chr1
    return (mouse_genes_chr1,)


@app.cell
def _(bioframe, chromsizes_mouse, mouse_genes_chr1):
    bins = bioframe.binnify(chromsizes_mouse, 100_000)

    bin_gene_counts = bioframe.count_overlaps(bins, mouse_genes_chr1)
    bin_gene_counts
    return (bin_gene_counts,)


@app.cell
def _():
    import pyarrow as pa
    import pyarrow.ipc as ipc
    import pandas as pd
    return ipc, pa, pd


@app.cell
def _(ipc, model, pa):
    buf = pa.BufferReader(model)
    reader = ipc.RecordBatchFileReader(buf)

    table = reader.read_all()

    table
    return (table,)


@app.cell
def _(table):
    table_as_df = table.to_pandas()
    table_as_df
    return (table_as_df,)


@app.cell
def _(table_as_df):
    # rename 'chr a' to 'chr1' etc.
    table_df = table_as_df.copy()
    mapping = {
        'chr a': 'chr1',
        'chr b': 'chr2',
        'chr c': 'chr3',
        'chr d': 'chr4',
        'chr e': 'chr5',
        'chr f': 'chr6',
        'chr g': 'chr7',
        'chr h': 'chr8',
        'chr i': 'chr9',
        'chr j': 'chr10',
        'chr k': 'chr11',
        'chr l': 'chr12',
        'chr m': 'chr13',
        'chr n': 'chr14',
        'chr o': 'chr15',
        'chr p': 'chr16',
        'chr q': 'chr17',
        'chr r': 'chr18',
        'chr s': 'chr19',
        # 'chr a': 'chrX',
    }
    table_df['chr'] = table_df['chr'].map(mapping).fillna(table_df['chr'])

    # add 'end' column
    table_df['end'] = table_df['coord'] + 100_000

    # rename 'coord' to 'start'
    table_df = table_df.rename(columns={'coord': 'start'})

    # rename 'chr' to 'chrom'
    table_df = table_df.rename(columns={'chr': 'chrom'})

    table_df
    return (table_df,)


@app.cell
def _(bin_gene_counts, pd, table_df):
    merged_df = pd.merge(table_df, bin_gene_counts, on=["chrom", "start", "end"], how="inner")
    merged_df
    return (merged_df,)


@app.cell
def _(merged_df, pa):
    merged_table = pa.Table.from_pandas(merged_df)
    # xyzArrowTable = pa.Table.from_pandas(df)
    # Convert the Table to bytes
    output_stream = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(output_stream, merged_table.schema) as writer:
        writer.write_table(merged_table)

    # Get the table as Bytes
    merged_table_bytes = output_stream.getvalue().to_pybytes()

    # merged_table # this actually shouldn't really be needed, because I can just directly feed the pandas DF to uchimata widget
    return (merged_table_bytes,)


@app.cell
def _(merged_df, pd):
    isinstance(merged_df, pd.DataFrame)
    return


@app.cell
def _(merged_table_bytes, uchi):
    vc = {
        # "color": "lightgreen",
        # "color": {
        #     "field": "x",
        #     "min": -1,
        #     "max": 1,
        #     "colorScale": "Spectral"
        # }, 
        "color": {
            "field": "count",
            "min": 0,
            "max": 395,
            "colorScale": "Viridis"
        }, 
        "scale": 0.005, "links": False, "mark": "sphere"
    }

    w3 = uchi.Widget(structure=merged_table_bytes, viewconfig=vc)
    w3
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
