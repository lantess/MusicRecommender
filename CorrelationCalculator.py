import struct
import numpy as np

import Variables as var


def calculate_correlation(f_data, s_data) -> float:
    f_data = np.array(struct.unpack("f" * var.FFT_LEN, f_data))
    s_data = np.array(struct.unpack("f" * var.FFT_LEN, s_data))
    return np.average(np.abs(f_data - s_data) ** 2)


def diff(f_data: list, s_data: list) -> float:
    return np.average(np.abs(np.array(f_data) - np.array(s_data)) ** 2)


def correlation(f_data: list, s_data: list):
    return np.correlate(f_data, s_data, mode='full')


def convolution(f_data: list, s_data: list):
    return np.convolve(f_data, s_data)


def my_own_fucking_correlation(f_data: list, s_data: list) -> float:
    max = min(len(f_data), len(s_data))
    res_counter = 0
    for i in range(1, max):
        f = f_data[i] - f_data[i - 1]
        f = 1 if f > 0 else (0 if f == 0 else -1)
        s = s_data[i] - s_data[i - 1]
        s = 1 if s > 0 else (0 if s == 0 else -1)
        if f == s:
            res_counter += 1
    return res_counter / (max - 1)


def second_my_own_fucking_corr(f_data: list, s_data: list) -> float:
    f_data = list(f_data)
    s_data = list(s_data)
    dif = len(f_data) - len(s_data)
    if dif < 0:
        f_data += [0] * -dif
    else:
        s_data += [0] * dif
    return diff(f_data, s_data)
# 20
# 145
