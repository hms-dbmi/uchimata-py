import importlib.metadata
import pathlib

import anywidget
import traitlets

import numpy as np
import pandas as pd
import pyarrow as pa

import re
import duckdb

try:
    __version__ = importlib.metadata.version("chromospyce")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


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

def select(_model, _query):
    # convert arrow Bytes to Table
    reader = pa.ipc.open_file(_model)
    struct_table = reader.read_all()
    # separate query into "chromosome:starCoord-endCoord"
    if ":" in _query:
        match = re.match(r"([^\:]+):(\d+)-(\d+)", _query)
        if match:
            chrom, start, end = match.groups()
            sqlQuery = f'SELECT * FROM struct_table WHERE chr = \'{chrom}\' AND coord >= {start} AND coord <= {end}'
        else:
            print("Pattern does not match.")
            return
    else:
        sqlQuery = f'SELECT * FROM struct_table WHERE chr = \'{_query}\''
    
    con = duckdb.connect()
    print(sqlQuery)
    new_table = con.execute(sqlQuery).arrow()
    print(new_table)
    # new_table
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, new_table.schema)
    writer.write_table(new_table)
    writer.close()

    # Get the bytes
    arrow_bytes = sink.getvalue().to_pybytes()

    vc2 = {
        "color": "lightgreen",
        "scale": 0.01, 
        "links": True, 
        "mark": "sphere"
    }

    # return chromospyce.Widget(structure=arrow_bytes, viewconfig=vc2)
    return Widget(structure=arrow_bytes, viewconfig=vc2)

class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # 3D structure input: assumes Apache Arrow format
    structure = traitlets.Bytes().tag(sync=True)
    # ViewConfig: defines how the 3D structure will be shown
    viewconfig = traitlets.Dict().tag(sync=True)
    selection_query = traitlets.Unicode("").tag(sync=True)

    def __init__(self, structure, viewconfig={}, query=""):
        """
        What types of data we expect:
        - 2D numpy array: [[x, y, z], ...]
        - pandas dataframe: columns need to be 'x', 'y', 'z'
        """
        if isinstance(structure, np.ndarray):
            # is a numpy array
            super().__init__(structure=from_numpy(structure), viewconfig=viewconfig, selection_query=query)
        elif isinstance(structure, pd.DataFrame):
            # is a pandas dataframe
            super().__init__(structure=from_pandas_dataframe(structure), viewconfig=viewconfig, selection_query=query)
        else:
            # is something else (assume Arrow as Bytes)
            super().__init__(structure=structure, viewconfig=viewconfig, selection_query=query)

    def get_data(self, format="arrow"):
        """Returns the data displayed in the Widget. 

        The idea is to allow specifying which format to return the data in
        (arrow, numpy, pandas).
        Arrow is the default option for now."""
        if format == "numpy":
            return self.as_numpy()
        elif format == "arrow":
            return self.as_arrow()
        else:
            return self.as_arrow()

    def as_arrow(self):
        # TODO: take into account selection_query
        return self.structure

    def as_numpy(self):
        # TODO: take into account selection_query
        reader = pa.ipc.open_file(self.structure)
        table = reader.read_all()
        # Only output the coordinates:
        only_coords_table = table.select(["x", "y", "z"])
        numpy_arr = only_coords_table .to_pandas().to_numpy()
        return numpy_arr

