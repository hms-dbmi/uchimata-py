import importlib.metadata
import pathlib

import anywidget
import traitlets

import numpy as np
import pandas as pd
import pyarrow as pa

try:
    __version__ = importlib.metadata.version("uchimata")
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

class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    # _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # 3D structure input: assumes Apache Arrow format
    structure = traitlets.Bytes().tag(sync=True)
    # ViewConfig: defines how the 3D structure will be shown
    viewconfig = traitlets.Dict().tag(sync=True)

    def __init__(self, structure, viewconfig={}):
        """
        What types of data we expect:
        - 2D numpy array: [[x, y, z], ...]
        - pandas dataframe: columns need to be 'x', 'y', 'z'
        """
        if isinstance(structure, np.ndarray):
            # is a numpy array
            super().__init__(structure=from_numpy(structure), viewconfig=viewconfig)
        elif isinstance(structure, pd.DataFrame):
            # is a pandas dataframe
            super().__init__(structure=from_pandas_dataframe(structure), viewconfig=viewconfig)
        else:
            # is something else (assume Arrow as Bytes)
            super().__init__(structure=structure, viewconfig=viewconfig)

