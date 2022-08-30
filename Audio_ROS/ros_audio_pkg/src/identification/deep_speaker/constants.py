# Constants.
SAMPLE_RATE = 16000  # not higher than that otherwise we may have errors when computing the fbanks.
# Input to the model will be a 4D image: (batch_size, num_frames, num_fbanks, 3)
# Where the 3 channels are: FBANK, DIFF(FBANK), DIFF(DIFF(FBANK)).
NUM_FRAMES = 160  # 1 second ~ 100 frames with default params winlen=0.025,winstep=0.01
NUM_FBANKS = 64
