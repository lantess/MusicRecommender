class SoundData:
    def __init__(self):
        self.tempo = -1
        self.fft_len = -1


_dict = {}


def put(name: str):
    _dict[name] = SoundData()


def get(name: str) -> SoundData:
    return _dict[name]


def get_names():
    return _dict.keys()
