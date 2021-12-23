import os

import SoundTransformer as st

_correlationFlattenedMatrix = []
_out_matrix = []
_size = -1
_matrix_iterator = -1


def initialize(matrix, size):
    _correlationFlattenedMatrix = matrix
    _matrix_iterator = 0
    _size = size

def compute_new_value(first: str, second: str):
    f_key = os.path.join(st.FFT_DIR, first.replace('.wav', '.bin'))
    s_key = os.path.join(st.FFT_DIR, second.replace('.wav', '.bin'))
    print('DEBUG: new value')

def delete_value():
    print('DEBUG: deleted value')

def delete_row():
    print('DEBUG: deleted row')

def get_next_from_matrix():
    print('DEBUG: next value from matrix')

def compute(first: str, second: str):
    f_tag = first[first.find('[')+1:first.find(']')]
    if f_tag == 'NEW':
        compute_new_value(first[first.find(']')+1], second[second.find(']')+1])
    elif f_tag == 'DEL':
        delete_row()
    else:
        s_tag = second[second.find('[')+1:second.find(']')]
        if s_tag == 'NEW':
            compute_new_value(first[first.find(']')+1], second[second.find(']')+1])
        elif s_tag == 'DEL':
            delete_value()
        else:
            get_next_from_matrix()