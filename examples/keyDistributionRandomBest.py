import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from pydht.experiment import Experiment
import pydht.magic as magic

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
numNodes = nodeBase ** (nodeExp+2)
size = magic.BITS
iterations = magic.ITERATIONS

maxHashes = 17
runs = iterations*maxHashes


experiment = Experiment('keyDistributionRandomBest', size, 'keyDistributionRandomBest.png')
aliveCount = 0
for i in range(iterations):
        name = "Random"
        experiment.addTask({'p': (name, size, 'random', i, numNodes, (1, 100000), 0, None, 1, 0)})

        name = "Optimal"
        experiment.addTask({'p': (name, size, 'best', i, numNodes, (1, 100000), 0, None, 1, 0)})

experiment.execute()

aggMap = {'keys/node': ['mean', 'std'],
          'keys/node_10': ['mean'],
          'keys/node_50': ['mean', 'std'],
          'keys/node_90': ['mean'],
          '#nodes': ['mean']}

agg = experiment.data

agg = agg.filter(items=[ 'name', '#nodes', 'keys/node','keys/node_50', 'keys/node_10','keys/node_90']).groupby(['name']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['keys/node_50_mean'],ascending = [1])

x = [str(a) for a in agg.index.tolist()]
y = list(agg['keys/node_50_mean'].values)

err = [[a_i - b_i for a_i, b_i in zip(y, [x for x in agg['keys/node_10_mean']])],
       [a_i - b_i for a_i, b_i in zip([x for x in agg['keys/node_90_mean']]  ,y)]]

experiment.setAxisLabel('Placement Strategy','Keys/Node')
plt = experiment.getPlt()
plt.bar(x, height=y, width=[0.5], yerr=err, capsize=2)

experiment.saveOrShow(magic.SAVE_FILE)
