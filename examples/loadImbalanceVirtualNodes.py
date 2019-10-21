import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pydht.magic as magic
from pydht.experiment import Experiment

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
bits = magic.BITS
numNodes = nodeBase ** nodeExp
iterations = magic.ITERATIONS
experiment = Experiment('loadImbalanceVirtualNodes',bits,'loadImbalanceVirtualNodes.png')

for e in range(iterations):
    for i in range(1,17):
        name = str(i)
        experiment.addTask({'p': (name, bits, 'virtual', e, numNodes,(1,numNodes * 100),0,None,1,i)})

experiment.execute()

aggMap = {'keys/node': ['mean', 'std'],
          'keys/node_10': ['mean'],
          'keys/node_50': ['mean', 'std'],
          'keys/node_90': ['mean'],
          '#nodes': ['mean']}

agg = experiment.data

agg = agg.filter(items=[ 'name', '#nodes', 'keys/node','keys/node_50', 'keys/node_10','keys/node_90']).groupby(['name']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg.index = agg.index.astype(int)
agg = agg.sort_index()
x = [str(a) for a in agg.index.tolist()]
y = list(agg['keys/node_50_mean'].values)

err = [[a_i - b_i for a_i, b_i in zip(y, [x for x in agg['keys/node_10_mean']])],
       [a_i - b_i for a_i, b_i in zip([x for x in agg['keys/node_90_mean']]  ,y)]]

experiment.setAxisLabel('# Virtual Nodes/Real Node', 'Average #Keys/Node')
experiment.getPlt().errorbar(x, y, err, fmt='-k')
experiment.saveOrShow(magic.SAVE_FILE)