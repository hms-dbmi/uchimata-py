import chromospyce as chs
import numpy as np
import pandas as pd
import pyarrow as pa

def test_numpy_simple():
    positions = [np.array([0.0, 0.0, 0.0]),
                 np.array([1.0, 0.0, 0.0]),
                 np.array([2.0, 0.0, 0.0])]
    structure = np.array(positions)

    vc = {
        "color": "purple",
        "scale": 0.01, 
        "links": True, 
        "mark": "sphere"
    }
    w = chs.Widget(structure=structure, viewconfig=vc)
    assert isinstance(w, chs.Widget)

def test_pandas_simple():
    df = pd.DataFrame({"x": [0.0, 1.0, 2.0],
                       "y": [0.0, 0.0, 0.0],
                       "z": [0.0, 0.0, 0.0]})
    vc = {
        "color": "purple",
        "scale": 0.01, 
        "links": True, 
        "mark": "sphere"
    }
    w = chs.Widget(structure=df, viewconfig=vc)
    assert isinstance(w, chs.Widget)

def test_arrow_simple():
    x_positions = np.array([0.0, 1.0, 2.0])
    y_positions = np.array([0.0, 0.0, 0.0])
    z_positions = np.array([0.0, 0.0, 0.0])

    pa.array(x_positions)

    table = pa.Table.from_arrays([x_positions, y_positions, z_positions], names=["x", "y", "z"])

    output_stream = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(output_stream, table.schema) as writer:
        writer.write_table(table)

    table_as_bytes = output_stream.getvalue().to_pybytes()

    vc = {
        "color": "purple",
        "scale": 0.01, 
        "links": True, 
        "mark": "sphere"
    }
    w = chs.Widget(structure=table_as_bytes, viewconfig=vc)
    assert isinstance(w, chs.Widget)
