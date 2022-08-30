import numpy as np
import librosa


# io utils

class ReadAudio:
    def __init__(self, sr=None, mono=True, res_type='kaiser_best'):
        '''
            Read img
            sr: float. None for native sampling rate
            mono : bool. Convert signal to mono
            res_type: str. resampy resampling mode.
        '''
        self.sr = sr
        self.mono = mono
        self.res_type = res_type

    def __call__(self, audio_path):
        '''
            Read img
            audio_path: string. Path to the file
        '''
        return librosa.load(audio_path, sr=self.sr, mono=self.mono, res_type=self.res_type)

# Operation utils


def batch_cosine_similarity(x1, x2):
    '''
        x1,x2 must be l2 normalized
    '''

    # https://en.wikipedia.org/wiki/Cosine_similarity
    # 1 = equal direction ; -1 = opposite direction
    mul = np.multiply(x1, x2)
    s = np.sum(mul, axis=1)

    # l1 = np.sum(np.multiply(x1, x1),axis=1)
    # l2 = np.sum(np.multiply(x2, x2), axis=1)
    # as values have have length 1, we don't need to divide by norm (as it is 1)
    return s


def dist2id(distance, y, ths, norm=False, mode='avg', filter_under_th=True):
    d = distance.copy()
    ths = np.array([ths]*len(y))
    y = np.array(y)

    # remove elements under the threshold
    if filter_under_th:
        idx = d >= ths
        d = d[idx]
        y = y[idx]
        ths = ths[idx]

        if d.shape[0] == 0:
            return None

    if norm:
        # norm in case of different thresholds
        d = (d - ths)/(1-ths)

    ids = list(set(y.tolist()))

    ids_prob = []
    for i in ids:
        if mode == 'max':
            ids_prob.append(np.max(d[y == i]))
        if mode == 'avg':
            ids_prob.append(np.mean(d[y == i]))
        if mode == 'min':
            ids_prob.append(np.min(d[y == i]))

    ids_prob = np.array(ids_prob)
    return ids[np.argmax(ids_prob)]
