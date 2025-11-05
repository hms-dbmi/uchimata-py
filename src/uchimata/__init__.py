import importlib.metadata
import pathlib

import anywidget
import traitlets

import numpy as np
import pandas as pd
import pyarrow as pa

import duckdb
import re
import bioframe

try:
    __version__ = importlib.metadata.version("uchimata")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

def select_bioframe(model, df):
    # convert arrow Bytes to Table
    reader = pa.ipc.open_file(model)
    struct_table = reader.read_all()

    if not bioframe.is_bedframe(df):
        # This makes sure that there are 'chrom', 'start', 'end' columns in the dataframe
        raise ValueError("DataFrame is not a valid bedframe.")

    sqlQuery = f'SELECT * FROM struct_table WHERE '
    for index, row in df.iterrows():
        chrom = row['chrom']
        start = row['start']
        end = row['end']
        if index > 0:
            sqlQuery += ' OR '
        sqlQuery += f'(chr = \'{chrom}\' AND coord >= {start} AND coord <= {end})'

    con = duckdb.connect()
    new_table = con.execute(sqlQuery).arrow()
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, new_table.schema)
    writer.write_table(new_table)
    writer.close()

    # Get the bytes
    arrow_bytes = sink.getvalue().to_pybytes()
    return arrow_bytes

def cut(model):
    # convert arrow Bytes to Table
    buf = pa.BufferReader(model)
    reader = pa.ipc.RecordBatchStreamReader(buf)

    # table = reader.read_all()
    struct_table = reader.read_all()

    sqlQuery = f'SELECT * FROM struct_table WHERE x > 0'
    
    con = duckdb.connect()
    new_table = con.execute(sqlQuery).arrow()
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, new_table.schema)
    writer.write_table(new_table)
    writer.close()

    # Get the bytes
    arrow_bytes = sink.getvalue().to_pybytes()
    return arrow_bytes

def select(_model, _query):
    # convert arrow Bytes to Table
    reader = pa.ipc.open_file(_model)
    struct_table = reader.read_all()
    # separate query into "chromosome:starCoord-endCoord"
    if ":" in _query:
        # means it should have a start-end range
        match = re.match(r"([^\:]+):(\d+)-(\d+)", _query)
        if match:
            chrom, start, end = match.groups()
            sqlQuery = f'SELECT * FROM struct_table WHERE chr = \'{chrom}\' AND coord >= {start} AND coord <= {end}'
        else:
            print("Pattern does not match.")
            return
    else:
        # otherwise let's assume that it's a chromosome name
        sqlQuery = f'SELECT * FROM struct_table WHERE chr = \'{_query}\''

    con = duckdb.connect()
    new_table = con.execute(sqlQuery).arrow()
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, new_table.schema)
    writer.write_table(new_table)
    writer.close()

    # Get the bytes
    arrow_bytes = sink.getvalue().to_pybytes()
    return arrow_bytes

    # vc2 = {
    #     "color": "lightgreen",
    #     "scale": 0.01, 
    #     "links": True, 
    #     "mark": "sphere"
    # }
    #
    # return Widget(structure=arrow_bytes, viewconfig=vc2)

def from_numpy(nparr):
    """
    This assumes `nparr` is a two-dimensional numpy array with xyz coordinates: [[x,y,z], ...]
    """
    xyz = nparr.astype(np.float32)
    # Convert numpy array to pandas dataframe
    xyzDF = pd.DataFrame({'x': xyz[:, 0], 'y': xyz[:, 1], 'z': xyz[:, 2]})

    return from_pandas_dataframe(xyzDF)

def from_pandas_dataframe(df):
    # Convert pandas DF to Arrow Table
    xyzArrowTable = pa.Table.from_pandas(df)
    # Convert the Table to bytes
    output_stream = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(output_stream, xyzArrowTable.schema) as writer:
        writer.write_table(xyzArrowTable)

    # Get the table as Bytes
    table_bytes = output_stream.getvalue().to_pybytes()
    return table_bytes

class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    # 3D structure input: assumes Apache Arrow format
    structures = traitlets.List().tag(sync=True)
    # ViewConfig: defines how the 3D structure will be shown
    viewconfigs = traitlets.List().tag(sync=True)

    def __init__(self, *structures, viewconfigs=None):
        """
        Create a widget with one or more 3D structures.

        Args:
            *structures: One or more structure inputs. Each can be:
                - 2D numpy array: [[x, y, z], ...]
                - pandas dataframe: columns need to be 'x', 'y', 'z'
                - Apache Arrow bytes
            viewconfigs: Optional viewconfig(s). Can be:
                - None: uses default empty viewconfig for all structures
                - dict: same viewconfig applied to all structures
                - list of dicts: each structure gets corresponding viewconfig
                  (if fewer viewconfigs than structures, cycles through them)

        Examples:
            Widget(structure1)
            Widget(structure1, viewconfigs={'color': 'red'})
            Widget(structure1, structure2, structure3)
            Widget(structure1, structure2, viewconfigs={'color': 'red'})
            Widget(s1, s2, s3, viewconfigs=[vc1, vc2, vc3])
            Widget(s1, s2, s3, viewconfigs=[vc1])  # vc1 used for all three
        """
        if not structures:
            raise ValueError("At least one structure must be provided")

        # Normalize viewconfigs to a list
        if viewconfigs is None:
            viewconfigs_list = [{}]
        elif isinstance(viewconfigs, dict):
            viewconfigs_list = [viewconfigs]
        else:
            viewconfigs_list = list(viewconfigs)

        # Convert all structures to Arrow bytes
        processed_structures = []
        for structure in structures:
            if isinstance(structure, np.ndarray):
                processed_structures.append(from_numpy(structure))
            elif isinstance(structure, pd.DataFrame):
                processed_structures.append(from_pandas_dataframe(structure))
            else:
                # Assume Arrow as Bytes
                processed_structures.append(structure)

        # Match structures with viewconfigs (cycle through viewconfigs if needed)
        matched_viewconfigs = []
        for i in range(len(processed_structures)):
            # Cycle through viewconfigs if there are fewer than structures
            vc_index = i % len(viewconfigs_list)
            matched_viewconfigs.append(viewconfigs_list[vc_index])

        super().__init__(structures=processed_structures, viewconfigs=matched_viewconfigs)

