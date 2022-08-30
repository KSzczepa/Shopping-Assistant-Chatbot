from tqdm import tqdm
import numpy as np


def embedd(X, y, ths, model, preprocess_input=None):
    '''This function creates a dictionary containing the embedding of
        X: List containing the raw files
        y: List containing the names relative to each identity
        ths: List containing the threshold relative to each identity
        model: Embedding CNN
        preprocessing_input: callable which returns a preprocessed iput for the model
    '''

    out = {
        'ths': ths,
        'y': y,
        'embeddings': []
    }

    for i in tqdm(range(len(X))):
        x_p = preprocess_input(
            X[i]) if preprocess_input is not None else X[i]

        if x_p is None:
            print("error i=%d, name=%s" % (i, y[i]))
            continue

        emb = model.predict(x_p)[0]

        out['embeddings'].append(emb)

    out['embeddings'] = np.array(out['embeddings'])

    return out
