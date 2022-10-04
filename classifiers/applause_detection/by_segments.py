from classifiers.audio_segmentation.by_segments import BySegments as ASBySegments

class BySegments(ASBySegments):
    def __init__(self):
        super().__init__('ApplauseDetection')
