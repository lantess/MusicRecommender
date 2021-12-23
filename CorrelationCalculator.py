

_correlationFlattenedMatrix = []
_out_matrix = []
_size = -1
_matrix_iterator = -1


def initialize(matrix, size):
    _correlationFlattenedMatrix = matrix
    _matrix_iterator = 0
    _size = size

def compute_new_value(first: str, second: str):
    pass

def delete_value():
    pass

def delete_row():
    pass

def get_next_from_matrix():
    pass

def compute(first: str, second: str):
    f_tag = first[first.find('[')+1:first.find(']')]
    if f_tag == 'NEW':
        compute_new_value(first[first.find(']')+1], second[second.find(']')+1])
    elif f_tag == 'DEL':
        delete_row()
    else:
        s_tag = second[second.find('[')+1:second.find(']')]

    #s_tag = second[second.find('[') + 1:second.find(']')]

