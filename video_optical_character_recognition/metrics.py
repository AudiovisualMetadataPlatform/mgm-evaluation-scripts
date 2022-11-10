import logging

class Metrics():

    def __init__(self):
        pass

    def precision(self, true_pos, false_pos):
        logging.info("Calculating precision")
        if isinstance(true_pos, list):
            true_pos = len(true_pos)
        false_pos = len(false_pos)
        precision = true_pos/(true_pos + false_pos) if (true_pos + false_pos) else 'N/A'
        return precision

    def recall(self, true_pos, false_neg):
        logging.info("Calculating recall")
        if isinstance(true_pos, list):
            true_pos = len(true_pos)
        false_neg = len(false_neg)
        recall = true_pos/(true_pos + false_neg) if (true_pos + false_neg) else 'N/A'
        return recall

    def f1(self, true_pos, false_pos, false_neg):
        logging.info("Calculating F1")
        p = self.precision(true_pos, false_pos)
        r = self.recall(true_pos, false_neg)
        if r == 0.0:
            r = 0
        f1 = 2*((p*r)/(p+r)) if p != 'N/A' and r != 'N/A' and (p+r) > 0 else 'N/A'
        return f1

    def accuracy(self, tp, gt):
        logging.info("Calculating accuracy")
        true_pos = len(tp)
        total = len(gt)
        accuracy = true_pos/total
        return accuracy