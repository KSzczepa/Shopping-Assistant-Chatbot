import librosa
import numpy as np
from python_speech_features import fbank

from .constants import SAMPLE_RATE, NUM_FBANKS, NUM_FRAMES


def read_audio(path, sample_rate):
    return librosa.load(path, sr=sample_rate)[0]


def get_mfcc(audio, sample_rate):
    audio_voice_only = audio

    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]
    audio_voice_only = audio[offsets[0]:offsets[-1]]

    mfcc = mfcc_fbank(audio_voice_only, sample_rate)

    return mfcc


def read_mfcc(path, sample_rate):
    audio = read_audio(path, sample_rate)
    return get_mfcc(audio, sample_rate)

def pad_mfcc(mfcc, max_length):  # num_frames, nfilt=64.
    if len(mfcc) < max_length:
        mfcc = np.vstack(
            (mfcc, np.tile(np.zeros(mfcc.shape[1]), (max_length - len(mfcc), 1))))
    return mfcc


def mfcc_fbank(signal: np.array, sample_rate: int):  # 1D signal array.
    # Returns MFCC with shape (num_frames, n_filters, 3).
    filter_banks, energies = fbank(
        signal, samplerate=sample_rate, nfilt=NUM_FBANKS)

    frames_features = normalize_frames(filter_banks)
    # delta_1 = delta(filter_banks, N=1)
    # delta_2 = delta(delta_1, N=1)
    # frames_features = np.transpose(np.stack([filter_banks, delta_1, delta_2]), (1, 2, 0))
    # Float32 precision is enough here.
    return np.array(frames_features, dtype=np.float32)


def normalize_frames(m, epsilon=1e-12):
    return [(v - np.mean(v)) / max(np.std(v), epsilon) for v in m]
