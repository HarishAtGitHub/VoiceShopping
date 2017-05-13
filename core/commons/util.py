import time

from constants import ROOT_DIR
import os
import pickle

def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        print(func.__name__)
        print("elapsed time: %f" % (end_ts - beg_ts))
        return retval
    return wrapper

"""
To convert object to serialized form and store in file given

@param obj the object to be serialized
@param file_location this is file location with respect to root directory (base dir of project)

@return None
"""
def serialize(obj, file_location):
    extract_file = os.path.join(ROOT_DIR , file_location)
    with open(extract_file, 'wb') as storage_file:
        pickle.dump(obj, storage_file)

"""
To convert object to serialized form and store in file given

@param file_location this is file location with respect to root directory (base dir of project)

@return deserialized object
"""
def deserialize(file_location):
    extract_file = os.path.join(ROOT_DIR, file_location)
    with open(extract_file, 'rb') as storage_file:
        obj = pickle.load(storage_file)
    return obj
