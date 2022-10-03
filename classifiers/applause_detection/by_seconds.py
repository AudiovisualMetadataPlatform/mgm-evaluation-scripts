from classifiers.audio_segmentation.by_seconds import BySeconds as ASBySeconds

class BySeconds(ASBySeconds):
    def __init__(self):
        super().__init__('seconds', ['applause', 'non-applause'])
