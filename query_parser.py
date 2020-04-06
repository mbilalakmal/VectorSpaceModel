# -----------------------------------------------------------
# This module calculates and returns cosine similarity
# between a user query and the indexed documents.
#
# The steps performed are summarized below:
# (1) The query is converted to a unit vector (TF-IDF weighting).
# (2) Load VSM matrix containing document vectors.
# (3) Calculate cosine similarity of each document.
# (4) Sort documents in order of similarity.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import heapq

import numpy as np

import filing
from preprocessing.token_normalizer import normalize_tokens
from preprocessing.tokenizer import tokenize


def parse_query(query: str):
    '''
    Convert `query` to query_vector.

    TF-IDF = log(tf+1) * log(N/df)
    '''
    vsm_index = filing.load_python_object(r'objects/vsm_index')

    term_positions = vsm_index['term_positions']
    idf_vector = vsm_index['idf_vector']

    # convert to tokens and normalize the tokens
    query_terms = normalize_tokens(tokenize(query))

    nterms = len(term_positions)
    query_vector = np.zeros(shape=(nterms,), dtype=float)

    # if query magnitude == 0 | query contains no features
    contains_no_features = True

    for term in query_terms:
        # ignore terms that are not features of any doc
        if term not in term_positions.keys():
            continue

        contains_no_features = False

        # get position/dimension of feature
        position = term_positions[term]
        query_vector[position] += 1

    if contains_no_features:
        return query_vector # return as it is

    # TF = log(tf+1)
    query_vector += 1
    query_vector = np.log(query_vector)

    # TF-IDF = TF * IDF
    query_vector = np.multiply(query_vector, idf_vector)

    # convert to unit vector
    magnitude = (query_vector**2).sum(keepdims=True) ** (0.5)

    query_vector = query_vector / magnitude

    return query_vector


def calculate_cosine_sim(query_vector):
    '''
    Calculate and return cosine similarity of a `query_vector`.

    Returns a maxheap of tuples in order of similarity.
    '''
    vsm_index = filing.load_python_object(r'objects/vsm_index')
    vsm_matrix = vsm_index['vsm_matrix']

    max_heap = [] # store (-sim, doc_id) tuples

    for doc_id in range(vsm_matrix.shape[0]):
        sim = np.dot(query_vector, vsm_matrix[doc_id])
        negative_sim = -1 * sim
        #insert in max_heap | -VE beacuse heapq is actually minheap
        item = (negative_sim, doc_id)
        heapq.heappush(max_heap, item)

    return max_heap


def resolve_vsm_query(query: str, alpha: float=0.0005):
    '''
    Returns a list of tuples in descending order of similarity.

    Doc_ids are converted to string for displaying.
    '''
    # convert to vector
    query_vector = parse_query(query)

    # calculate sim
    max_heap = calculate_cosine_sim(query_vector)

    results = []

    while max_heap:
        result = heapq.heappop(max_heap)
        sim, doc_id = result
        doc_id = str(doc_id)
        sim *= -1
        if sim < alpha:
            break
        results.append(doc_id)

    return results


if __name__ == '__main__':
    query = input('Enter query: ')
    results = resolve_vsm_query(query)
    size = len(results)
    
    print(f'Relevant speeches: {results}')
    print(f'Number of relevant documents: {size}')