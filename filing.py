# -----------------------------------------------------------
# This module contains helper functions related to file I/O.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import pickle
import re
from glob import glob


def load_python_object(filename):
    '''
    Load and return an object from `filename`.
    '''
    with open(filename, 'rb') as object_file:
        python_object = pickle.load(object_file)
    return python_object


def store_python_object(python_object, filename):
    '''
    Store `python_object` in `filename`.

    If `filename` exists, it will be overwritten.
    '''
    with open(filename, 'wb') as bin_file:
        pickle.dump(python_object, bin_file)


def read_docs_files(pathname, encoding = 'utf=8'):
    '''
    Return txt documents discovered in `pathname`.

    Two dictionaries are retuned as a tuple:
        first maps numeric IDs to file name.
        second maps numeric IDs to document body.
    '''
    documents   = {}    # numeric ID mapped to document body
    doc_ids     = {}    # numeric ID mapped to file name

    # discover txt files in pathname
    # and load into documents dictionary
    for file_name in glob(pathname):

        #get numeric ID from file name
        doc_id = int(re.search(r'\d+', file_name).group(0))
        doc_ids[doc_id] = file_name

        with open(file_name, 'r', encoding=encoding) as txt_file:
            _ = txt_file.readline()     #discard title
            document = txt_file.read()
            documents[doc_id] = document

    return (doc_ids, documents)


def read_stop_words(filename):
    '''
    Return a set of stop words present in `filename`.
    '''
    with open(filename, 'r') as txt_file:
        stop_words = set( txt_file.read().split() )
    return stop_words