import os
import struct
import numpy as np

output_filename = "matrix.bin"
legend_filename = "matrix.data"
directory = "fft_res"
metadata_filename = "meta.data"
size_dictionary = {}
x_dictionary = {}
z_dictionary = {}

def loadData(file):
    key = file.replace(".txt", ".wav")
    path = os.path.join(directory, file)
    input = open(path, "rb")
    data = input.read()
    input.close()
    size = int(size_dictionary[key])
    try:
        new_data = np.array(struct.unpack("f" * int(size), data))
    except MemoryError as error:
        print(error)
    return new_data

metafile = open(metadata_filename, "r")
for line in metafile:
    name = line[0:line.find(" --- ")]
    size = line[line.find(" --- ")+5:]
    x = int(size[0:size.find("x")])
    y = int(size[size.find("x")+1:size.rfind("x")])
    z = float(size[size.rfind("x")+1:size.find("\n")])
    size_dictionary[name] = x
    x_dictionary[name] = y
    z_dictionary[name] = z

files = os.listdir(directory)
count = 0

open(output_filename, "w").close()
open(legend_filename, "w").close()

tmp_out = open("tmp.csv", "w")

for file in files:
    count = count + 1
    ydata = loadData(file)
    res = []
    for com_file in files:
        if file != com_file:
            ycom_data = loadData(com_file)
            diff = np.abs(ydata-ycom_data) #rozróżnienie
            avgDiff = np.average(diff**2)/100
            res.append(avgDiff)
            tmp_out.write(file)
            tmp_out.write(";")
            tmp_out.write(com_file)
            tmp_out.write(";")
            tmp_out.write(str(avgDiff))
            tmp_out.write("\n")
    out = open(output_filename, "ab")
    for cell in res:
        out.write(struct.pack("f", cell))
    out.close()

tmp_out.close()

legend = open(legend_filename, "a")
for file in files:
    legend.write(file)
    legend.write("\n")
legend.close()

#20

#145