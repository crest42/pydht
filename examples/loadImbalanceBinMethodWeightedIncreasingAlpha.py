import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pydht.magic as magic
from pydht.experiment import Experiment
import numpy as np

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
bits = magic.BITS
numNodes = nodeBase ** nodeExp
iterations = magic.ITERATIONS
increments = magic.NODE_INCREMENTS
xAxis = []
experiment = Experiment('virtualNodesBinMethodWeightedIncreasingAlpha',bits,'virtualNodesBinMethodWeightedIncreasingAlpha.png')

for i in range(iterations):
        for e in range(0, magic.BITS+1):
                name = str(e)
                experiment.addTask({'p': (name, bits, 'binReal', i, numNodes,(1,0),0,e,1,0)})


experiment.execute()

aggMap = {'share': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'share']).groupby('name').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg.index = agg.index.astype(int)
agg = agg.sort_index()
x = agg.index.tolist()
y = agg['share_mean'].values
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['share_10-th percentile']))],
       [a_i - b_i for a_i, b_i in zip(list(agg['share_90-th percentile']), y)]]

experiment.setAxisLabel('Strategy', 'Imbalance')
experiment.getPlt().plot(x, list(y))
experiment.getPlt().xticks(x)
#for i in range(len(x)):
#    plt.text(x=i - 0.05, y=y[i] + err[1][i] + 0.2, s=str(round(y[i], 2)), size=9)

experiment.saveOrShow(False)