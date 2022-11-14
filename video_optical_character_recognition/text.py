import logging

class Text():
    def __init__(self, case):
        self.case = case

    def confusionMatrix(self, ground_truth, mgm_output):
        logging.info("Generating confusion matrix")
        cmu = None
        if self.case == 'unique':
            ground_truth = self.uniqueTexts(ground_truth)
            mgm_output = self.uniqueTexts(mgm_output)
            tp = list(set(mgm_output) & set(ground_truth))
            #false positive is words in mgm not in gt
            fp = list(set(mgm_output) - set(ground_truth))
            #false negative is words in gt not in mgm
            fn = list(set(ground_truth) - set(mgm_output))
        else:
            ground_truth = self.text(ground_truth)
            mgm_output = self.text(mgm_output)
            tp = [item for item in mgm_output if item in ground_truth]
            #false positive is words in mgm not in gt
            fp = [item for item in mgm_output if item not in ground_truth]
            #false negative is words in gt not in mgm
            fn = [item for item in ground_truth if item not in mgm_output]
        
        combined = []
        for t in tp:
            tpc = {}
            tpc['text'] = t
            tpc['comparison'] = 'true positive'
            combined.append(tpc)
        for f in fp:
            fpc = {}
            fpc['text'] = f
            fpc['comparison'] = 'false positive'
            combined.append(fpc)
        for n in fn:
            fnc = {}
            fnc['text'] = n
            fnc['comparison'] = 'false negative'
            combined.append(fnc)
        cmu = {'tp': tp,
                'fp': fp,
                'fn': fn,
                'combined': combined}
        return cmu

    def uniqueTexts(self, data):
        unique = list(set([d['text'] for d in data]))
        return unique

    def text(self, data):
        return [d['text'] for d in data]