# convert query string to unit vector (tf-idf)

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

    for term in query_terms:
        # ignore terms that are not features of any doc
        if term not in term_positions.keys():
            continue

        # get position/dimension of feature
        position = term_positions[term]
        query_vector[position] += 1

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

    Returns a list of tuples in descending order of similarity.
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


def resolve_vsm_query(query: str):
    # convert to vector
    query_vector = parse_query(query)

    # calculate sim
    max_heap = calculate_cosine_sim(query_vector)

    return max_heap


if __name__ == '__main__':
    query = input('Enter query: ')
    max_heap = resolve_vsm_query(query)
    size = len(max_heap)
    count = 0
    
    for i in range(size):
        result = heapq.heappop(max_heap)
        sim, doc_id = result
        sim *= -1
        if sim < 0.0005:
            break
        count += 1
        print(f'Doc: {doc_id} | Sim: {sim}')

    print(f'Length: {count}')