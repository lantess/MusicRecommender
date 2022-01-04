import struct
import numpy as np

import Variables as var


def calculate_correlation(f_data: bytes, s_data: bytes, length: int = var.FFT_LEN) -> float:
    f_data = np.array(struct.unpack("f" * length, f_data))
    s_data = np.array(struct.unpack("f" * length, s_data))
    return np.average(np.abs(f_data - s_data) ** 2)


def _cut_mag(data, mag: float) -> np.array:
    maximum = max(data)
    res = data - maximum
    return np.array([x if x > 0.0 else 0.0 for x in res])


def calculate_correlation_from_mag(f_data, s_data, corr_f: float) -> float:
    f_data = _cut_mag(np.array(struct.unpack("f" * var.FFT_LEN, f_data)), corr_f)
    s_data = _cut_mag(np.array(struct.unpack("f" * var.FFT_LEN, s_data)), corr_f)
    return np.average(np.abs(f_data - s_data) ** 2)

def calculate_correlation_from_unpacked_data(f_data, s_data) -> float:
    f_data = np.array(f_data)
    s_data = np.array(s_data)
    return np.average(np.abs(f_data - s_data) ** 2)
