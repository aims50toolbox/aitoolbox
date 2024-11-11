import numpy as np

class Image:
    def __init__(self, array) -> None:
        self.array = array

    def to_numpy(self):
        return np.asarray(self.array)
    
    def __str__(self):
        return f"{Image.__qualname__} {self.array.shape}"