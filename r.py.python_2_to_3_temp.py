

from pyflann.exceptions import FLANNException
import binary_dataset
import dat_dataset
import npy_dataset
import hdf5_dataset

import os.path
from numpy import float32

dataset_formats = { 
    'bin' : binary_dataset, 
    'dat' : dat_dataset, 
    'npy' : npy_dataset,
    'hdf5' : hdf5_dataset 
}


def load(filename, rows = -1, cols = -1, dtype = float32, **kwargs):
    
    for format in list(dataset_formats.values()):
        if format.check(filename):
            return format.load(filename, rows, cols, dtype, **kwargs)
    raise FLANNException("Error: Unknown dataset format")
    
    
def save(dataset, filename, format = None, **kwargs):    
    try:
        if format is None:
            basename,extension = os.path.splitext(filename)
            format = extension[1:]
        handler = dataset_formats[format]
        handler.save(dataset, filename, **kwargs)
    except Exception as e:
        raise FLANNException(e)