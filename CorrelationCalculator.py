import struct
import numpy as np

import Variables as var

def calculate_correlation(f_data, s_data) -> float:
   f_data = np.array(struct.unpack("f"*var.FFT_LEN, f_data))
   s_data = np.array(struct.unpack("f" * var.FFT_LEN, s_data))
   return np.average(np.abs(f_data - s_data))

def diff(f_data: list, s_data: list) -> float:
   return np.average(np.abs(np.array(f_data) - np.array(s_data)))

#20
#145