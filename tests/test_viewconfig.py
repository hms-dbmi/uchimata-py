import chromospyce as chs
import numpy as np
import pyarrow as pa

def test_no_viewconfig_supplied():
    positions = [np.array([0.0, 0.0, 0.0]),
                 np.array([1.0, 0.0, 0.0]),
                 np.array([2.0, 0.0, 0.0])]
    structure = np.array(positions)

    w = chs.Widget(structure=structure)
    assert isinstance(w, chs.Widget)
