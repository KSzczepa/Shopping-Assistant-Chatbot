from .conv_models import DeepSpeakerModel

def get_deep_speaker(weights_path):
    model = DeepSpeakerModel()
    model.m.load_weights(weights_path, by_name=True)

    return model.m