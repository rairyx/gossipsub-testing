import glob
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
# change this to your virtualenv path
sys.path.append('../../venv/gs-test/lib/python3.6/site-packages')

# %matplotlib inline

metricProps = {
    'messageID': '',
    'originatorHostID': '',
    'totalNanoTime': '',
    'lastDeliveryHop': '',
    'relativeMessageRedundancy': ''
}


class Metric(object):
    def __init__(self, props=metricProps):
        self.messageID = props['messageID']
        self.originatorHostID = props['originatorHostID']
        self.totalNanoTime = int(props['totalNanoTime'])
        self.lastDeliveryHop = float(props['lastDeliveryHop'])
        self.relativeMessageRedundancy = \
            float(props['relativeMessageRedundancy'])

def computeMetrics(algorithm='gossip', filename=None, fig=0):
    metrics = []
    nanoTimes = []
    ldh = []
    rmr = []

    if filename is None:
        pubsubAnalysisFiles = glob.glob('*.json')
    else:
        pubsubAnalysisFiles = glob.glob('{}'.format(filename))

    for pubsubAnalysisFile in pubsubAnalysisFiles:
        tmpMetrics = []

        with open(pubsubAnalysisFile) as json_file:
            data = json.load(json_file)
            for metric in data:
                m = Metric(metric)
                tmpMetrics.append(m)

                nanoTimes.append(m.totalNanoTime)
                ldh.append(m.lastDeliveryHop)
                rmr.append(m.relativeMessageRedundancy)

        metrics.append(tmpMetrics)

    plt.figure(fig)

    nanoTimesArr = np.asarray(nanoTimes)
    # a, b, c = plt.hist(nanoTimes, bins='auto', histtype='step',
    #                    cumulative=True)
    counts, bin_edges = np.histogram(nanoTimesArr, bins=2000, density=True)
    cdf = np.cumsum(counts)
    plt.plot(bin_edges[1:], cdf/cdf[-1])


    print(np.percentile(nanoTimesArr, 90))
    plt.title("{} - Total Nano Time Histogram".format(algorithm))
    plt.xlabel('Dissemination Time (ns)')
    plt.ylabel('Percent of Messages')

    nanoMean = np.mean(nanoTimes)
    nanoMedian = np.median(nanoTimes)
    nanoStd = np.std(nanoTimes)

    ldhMean = np.mean(ldh)
    ldhMedian = np.median(ldh)
    ldhStd = np.std(ldh)

    rmrMean = np.mean(rmr)
    rmrMedian = np.median(rmr)
    rmrStd = np.std(rmr)

    print('Messages published: {}'.format(len(nanoTimes)))
    print('Total Nano Times - mean: {}, median: {}, std: {}'.format(nanoMean, nanoMedian, nanoStd))
    print('Last Delivery Hop - mean: {}, median: {}, std: {}'.format(ldhMean, ldhMedian, ldhStd))
    print('Relative Message Redundancy - mean: {}, median: {}, std: {}'.format(rmrMean, rmrMedian, rmrStd))


num = 0
for file in glob.glob('final_json/analysis2b.json'):
    try:
        print("\n\nfile:" + file)
        computeMetrics('gossip', file, num)
    except KeyError:
        # not sure why this is happening
        print("relativeMessageRedundancy key error, skipping analysis")
    num += 1

plt.show()
