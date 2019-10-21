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
experiment = Experiment('loadImbalanceBinMethodWeighted',bits,'loadImbalanceBinMethodWeighted.png')

for i in range(iterations):
    for e in range(increments):
        numNodes = 2 ** e
        if str(numNodes) not in xAxis:
                xAxis.append(str(numNodes))
        name = "Virtual Nodes"
        experiment.addTask({'p': (name, bits, 'virtual', i, numNodes, (1, 0), 0, None, 1, bits)})

        name = "Binary Light"
        experiment.addTask({'p': (name, bits, 'bin', i, numNodes,(1,0),0,None,1,0)})

        name = "Binary Light Weighted"
        experiment.addTask({'p': (name, bits, 'binWeighted', i, numNodes,(1,0),0,None,1,0)})

experiment.execute()

aggMap = {'maxShareY0': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'maxShareY0','#nodes']).groupby(['name','#nodes']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

x = agg.index.tolist()
y = agg['maxShareY0_mean'].values
legend = list(set([e[0] for e in x])) 
values = [agg.loc[e].sort_values('#nodes') for e in legend]

experiment.setAxisLabel('# of Nodes', 'Max Share')
experiment.getPlt().style.use('seaborn-whitegrid')

for k in values:
        experiment.getPlt().plot(xAxis, list(k['maxShareY0_mean']))

experiment.getPlt().xticks(xAxis)
experiment.getPlt().legend(legend)
experiment.saveOrShow(magic.SAVE_FILE)
