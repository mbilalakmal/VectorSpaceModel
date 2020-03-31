# -----------------------------------------------------------
# This module creates an vsm index from the documents.
#
# The steps performed are summarized below:
# (1) Read all the documents.
# (2) Store Document IDs against their file names.
# (3) Create tokens from each document.
# (4) Preprocess (case-fold, stop-words removal, and lemmatize) tokens.
# (5) Create a vsm matrix with tf-idf as weighting scheme.
# (6) Store the vsm_index as a binary file.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import time

import nltk
import numpy as np

import filing
from preprocessing.token_normalizer import normalize_tokens
from preprocessing.tokenizer import tokenize

# download wordnet if not found
nltk.download('wordnet')


def _build_vsm_index(documents, stop_words):
    '''
    Build a vsm weighted matrix of features extracted from `documents`.

    `stop_words` are not considered as features.
    '''
    ndocs = len(documents)

    # each row is a doc | each column is a term (feature)
    vsm_matrix = np.zeros(shape=(ndocs, 0), dtype=float)

    # maps terms to their positions in the vsm_matrix
    term_positions = {}

    for item in documents.items():
        doc_id, document = item
        tokens = tokenize(document)
        terms = normalize_tokens(tokens, stop_words)

        for term in terms:
            if term not in term_positions.keys():
                # if term is not a dimension, add a dimension to the matrix
                position = len(term_positions)
                term_positions[term] = position

                term_frequencies = np.zeros(shape=(ndocs, 1), dtype=float)
                vsm_matrix = np.append(vsm_matrix, term_frequencies, axis=1)
            else:
                position = term_positions[term]

            # increment term frequency
            vsm_matrix[doc_id][position] += 1

    # document frequency for each term (column of vsm matrix)
    document_frequencies = np.count_nonzero(vsm_matrix, axis=0)
    # idf = log(N/df)
    idf_vector = np.log2(ndocs/document_frequencies)

    # multiply idf with tf
    vsm_matrix = np.multiply(vsm_matrix, idf_vector)

    vsm_index = {
        'term_positions': term_positions,
        'vsm_matrix': vsm_matrix,
        'idf_vector': idf_vector
    }
    return vsm_index


def generate_index_file():
    '''
    Create index file from the corpus.
    '''
    # Read all the document files
    pathname = r'resources\corpus\*.txt'
    doc_ids, documents = filing.read_docs_files(pathname)

    # Store doc_ids->filename dictionary
    filename = r'objects\doc_ids'
    filing.store_python_object(doc_ids, filename)

    # Read the stop words
    filename = r'resources\stopwords.txt'
    stop_words = filing.read_stop_words(filename)

    # Create the inverted index
    vsm_index = _build_vsm_index(documents, stop_words)

    # Store the inverted index
    filename = r'objects\vsm_index'
    filing.store_python_object(vsm_index, filename)


if __name__ == '__main__':
    start = time.time()
    generate_index_file()
    stop = time.time()
    print(f'Time: {stop-start}')