# -----------------------------------------------------------
# This module performs text normalization.
# Currently it applies:
# (1) Case folding
# (2) Stop-words removal
# (3) Lemmatization
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

from nltk.stem import WordNetLemmatizer


def normalize_tokens(tokens, stop_words=set()):
    '''
    Return case-folded and lemmatized `tokens`.

    `stop_words` are removed.
    '''
    folded_tokens = [token.lower() for token in tokens]

    folded_tokens = [token for token in folded_tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in folded_tokens]

    return lemmatized_tokens