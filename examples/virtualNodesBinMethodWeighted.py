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
experiment = Experiment('virtualNodesBinMethodWeighted',bits,'virtualNodesBinMethodWeighted.png')

for i in range(iterations):
        name = "Virtual Nodes"
        experiment.addTask({'p': (name, bits, 'virtual', i, numNodes, (1, 0), 0, None, 1, bits)})

        name = "Binary Light Weighted"
        experiment.addTask({'p': (name, bits, 'binWeighted', i, numNodes,(1,0),0,None,1,0)})

        name = "Binary Weighted"
        experiment.addTask({'p': (name, bits, 'binRealWeighted', i, numNodes,(1,0),0,None,1,0)})


experiment.execute()

aggMap = {'real/virt': ['mean'],
          'real/virt_min': ['mean'],
          'real/virt_max': ['mean']}
agg = experiment.data.filter(items=['name', 'real/virt','#nodes','real/virt_min','real/virt_max']).groupby(['name']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['real/virt_mean'],ascending = [0])

x = agg.index.tolist()
y = agg['real/virt_mean'].values
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['real/virt_min_mean'].values))],
       [a_i - b_i for a_i, b_i in zip(list(agg['real/virt_max_mean'].values),y)]]

experiment.setAxisLabel('# of Nodes', 'virtual nodes/real node')
plt = experiment.getPlt()
plt.bar(x, height=y, width=[0.5], yerr=err, capsize=2)

experiment.saveOrShow(magic.SAVE_FILE)