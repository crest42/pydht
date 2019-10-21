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
experiment = Experiment('virtualNodesBinMethodWeightedIncreasingSpread',bits,'virtualNodesBinMethodWeightedIncreasingSpread.png')

for i in range(iterations):
        name = "Virtual Nodes"
        experiment.addTask({'p': (name, bits, 'virtual', i, numNodes, (1, 0), 0, None, 1, bits)})

        for e in range(1, 20+1):
                if str(e) not in xAxis:
                        xAxis.append(str(e))

                name = "Binary Light Weighted"
                experiment.addTask({'p': (name, bits, 'binWeighted', i, numNodes,(1,0),0,None,1,e)})

                name = "Binary Weighted"
                experiment.addTask({'p': (name, bits, 'binRealWeighted', i, numNodes,(1,0),0,None,1,e)})


experiment.execute()

aggMap = {'real/virt': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'real/virt','#nodes','virtNodes']).groupby(['name','virtNodes']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['real/virt_mean'],ascending = [0])

x = agg.index.tolist()
y = agg['real/virt_mean'].values
legend = list(set([e[0] for e in x])) 
values = [agg.loc[e].sort_values('virtNodes') for e in legend]

experiment.setAxisLabel('Spread', 'Virtual Nodes/Real Node')
experiment.getPlt().style.use('seaborn-whitegrid')

for k in values:
        if k.index.tolist() == [32]:
                tmp = k
                #nasty hack
                for i in range(19):
                        k = k.append(tmp)
        experiment.getPlt().plot(xAxis, list(k['real/virt_mean']))

experiment.getPlt().xticks(xAxis)
experiment.getPlt().legend(legend)
experiment.saveOrShow(magic.SAVE_FILE)
