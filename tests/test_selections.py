import chromospyce as chs
import numpy as np
import pyarrow as pa
import pytest
import requests

@pytest.fixture
def test_model():
    url = "https://pub-5c3f8ce35c924114a178c6e929fc3ac7.r2.dev/Tan-2018_GSM3271347_gm12878_01.arrow"
    response = requests.get(url)
    if (response.status_code == 200):
        file = response.content
        return file
    else:
        print("Error fetching the remote file")
        return None

def is_arrow_ipc(bytes_obj):
    """Checks if a bytes object is an Apache Arrow IPC representation."""
    try:
        # Try reading the bytes as an Arrow IPC Stream
        with pa.ipc.open_stream(bytes_obj) as reader:
            reader.schema  # Access schema to ensure it's a valid Arrow object
        return True
    except pa.ArrowInvalid:
        return False

def test_select_chromosome_string_is_not_none(test_model):
    d = chs.select(test_model, "1(mat)")
    assert d is not None

def test_select_chromosome_string_is_bytes(test_model):
    d = chs.select(test_model, "1(mat)")
    assert isinstance(d, bytes)

def test_select_chromosome_string_is_arrow_ipc(test_model):
    d = chs.select(test_model, "1(mat)")
    assert is_arrow_ipc(d)
