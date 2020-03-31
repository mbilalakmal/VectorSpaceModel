# -----------------------------------------------------------
# This module converts a sequence into tokens.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import re


def tokenize(document):
    '''
    Return tokens from `document`.
    '''
    pattern = r'\W+'
    tokens = re.split(pattern, document)
    return tokens