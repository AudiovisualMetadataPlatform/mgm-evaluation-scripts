import jiwer, logging

class Metrics():

    def __init__(self):
        pass

    def wordErrorRate(self, gt, predicted):
        logging.info("Calculating word Error Rate")
        return jiwer.wer(gt, predicted)
    
    def matchErrorRate(self, gt, predicted):
        logging.info("Calculating match Error Rate")
        return jiwer.mer(gt, predicted)

    def wordInfoLoss(self, gt, predicted):
        logging.info("Calculating word Info Loss")
        return jiwer.wil(gt, predicted)

    def wordInfoProcessed(self, gt, predicted):
        logging.info("Calculating word Info Processed")
        return jiwer.wip(gt, predicted)

    def characterErrorRate(self, gt, predicted):
        logging.info("Calculating character Error Rate")
        return jiwer.cer(gt, predicted)

    def substitutionErrorRate(self, wer, substitution_prop):
        logging.info("Calculating Substitution Error Rate")
        return wer*substitution_prop

    def deletionErrorRate(self, wer, deletion_prop):
        logging.info("Calculating Deletion Error Rate")
        return wer*deletion_prop

    def insertionErrorRate(self, wer, insertion_prop):
        logging.info("Calculating Insertion Error Rate")
        return wer*insertion_prop