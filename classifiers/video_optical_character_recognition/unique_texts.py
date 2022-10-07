from utils.helper import logger

class UniqueText():
    def confusionMatrix(self, ground_truth_file, mgm_output_file):
        logger.info("Generating confusion matrix")
        cmu = None
        tp = list(set(mgm_output_file) & set(ground_truth_file))
        #false positive is words in mgm not in gt
        fp = list(set(mgm_output_file) - set(ground_truth_file))
        #false negative is words in gt not in mgm
        fn = list(set(ground_truth_file) - set(mgm_output_file))
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