from utils.helper import *
import jiwer

class Metrics():

    def __init__(self):
        pass

    def precision(self, true_pos, false_pos):
        logger.info("Calculating precision")
        true_pos = len(true_pos)
        false_pos = len(false_pos)
        precision = true_pos/(true_pos + false_pos) if (true_pos + false_pos) else 'N/A'
        return precision

    def recall(self, true_pos, false_neg):
        logger.info("Calculating recall")
        true_pos = len(true_pos)
        false_neg = len(false_neg)
        recall = true_pos/(true_pos + false_neg) if (true_pos + false_neg) else 'N/A'
        return recall

    def f1(self, true_pos, false_pos, false_neg):
        logger.info("Calculating F1")
        p = self.precision(true_pos, false_pos)
        r = self.recall(true_pos, false_neg)
        if r == 0.0:
            r = 0
        f1 = 2*((p*r)/(p+r)) if p != 'N/A' and r != 'N/A' and (p+r) > 0 else 'N/A'
        return f1

    def accuracy(self, tp, gt):
        logger.info("Calculating accuracy")
        true_pos = len(tp)
        total = len(gt)
        accuracy = true_pos/total
        return accuracy

    def wordErrorRate(self, gt, predicted):
        logger.info("Calculating word Error Rate")
        return jiwer.wer(gt, predicted)
    
    def matchErrorRate(self, gt, predicted):
        logger.info("Calculating match Error Rate")
        return jiwer.mer(gt, predicted)

    def wordInfoLoss(self, gt, predicted):
        logger.info("Calculating word Info Loss")
        return jiwer.wil(gt, predicted)

    def wordInfoProcessed(self, gt, predicted):
        logger.info("Calculating word Info Processed")
        return jiwer.wip(gt, predicted)

    def characterErrorRate(self, gt, predicted):
        logger.info("Calculating character Error Rate")
        return jiwer.cer(gt, predicted)

    def substitutionErrorRate(self, wer, substitution_prop):
        logger.info("Calculating Substitution Error Rate")
        return wer*substitution_prop

    def deletionErrorRate(self, wer, deletion_prop):
        logger.info("Calculating Deletion Error Rate")
        return wer*deletion_prop

    def insertionErrorRate(self, wer, insertion_prop):
        logger.info("Calculating Insertion Error Rate")
        return wer*insertion_prop