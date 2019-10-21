import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from pydht.experiment import Experiment
import pydht.magic as magic
import time
import numpy as np

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
numNodes = nodeBase ** nodeExp
bits = magic.BITS
iterations = magic.ITERATIONS
experiment = Experiment('keyDistributionBest', bits, 'keyDistributionBest.png')

for i in range(iterations):
    name = "chord_best"
    experiment.addTask({'p': (name, bits, 'best', i, numNodes,(100, 100),0,None,1,0)})

experiment.execute()
aggMap = {'keys/node': ['mean', 'std'],
          '#nodes': ['mean'],
          'keys/node_10': ['mean'],
          'keys/node_90': ['mean']}
agg = experiment.data.filter(items=['name', '#nodes', 'keys/node', 'keys', 'keys/node_10', 'keys/node_90']).groupby('keys').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

x = agg.index.tolist()
y = list(agg['keys/node_mean'].values)
err = [[a_i - b_i for a_i, b_i in zip(y, [x for x in agg['keys/node_10_mean']])],
       [a_i - b_i for a_i, b_i in zip([x for x in agg['keys/node_90_mean']]  ,y)]]


experiment.setAxisLabel('Keys Inserted','Avg Keys/Node')
plt = experiment.getPlt()
plt.errorbar(x, y, yerr=err, fmt='.k')
experiment.saveOrShow(magic.SAVE_FILE)