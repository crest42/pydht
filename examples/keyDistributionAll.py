import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from pydht.experiment import Experiment
import pydht.magic as magic

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
numNodes = nodeBase ** nodeExp
size = magic.BITS
iterations = magic.ITERATIONS

maxHashes = 17
runs = iterations*maxHashes


experiment = Experiment('keyDistributionAll', size, 'keyDistributionAll.png')
aliveCount = 0
for i in range(iterations):
        name = "Virtual Nodes"
        experiment.addTask({'p': (name, size, 'virtual', i, numNodes, (1, 10000), 0, None, 1, magic.BITS)})

        name = "log(N) Hashes"
        experiment.addTask({'p': (name, size, 'random', i, numNodes, (1, 10000), 0, None, magic.BITS, 0)})

        name = "Random"
        experiment.addTask({'p': (name, size, 'random', i, numNodes, (1, 10000), 0, None, 1, 0)})

        name = "Binary Light"
        experiment.addTask({'p': (name, size, 'bin', i, numNodes, (1, 10000), 0, None, 1,0)})

        name = "Y_0"
        experiment.addTask({'p': (name, size, 'y0', i, numNodes, (1, 10000), 0, None, 1,0)})

experiment.execute()

aggMap = {'keys/node': ['mean', 'std'],
          'keys/node_0': ['mean'],
          'keys/node_10': ['mean'],
          'keys/node_50': ['mean', 'std'],
          'keys/node_90': ['mean'],
          'keys/node_100': ['mean'],
          '#nodes': ['mean']}

agg = experiment.data

agg = agg.filter(items=[ 'name', '#nodes', 'keys/node','keys/node_0','keys/node_100','keys/node_50', 'keys/node_10','keys/node_90']).groupby(['name']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['keys/node_50_mean'],ascending = [1])

x = [str(a) for a in agg.index.tolist()]
y = list(agg['keys/node_50_mean'].values)

err = [[a_i - b_i for a_i, b_i in zip(y, [x for x in agg['keys/node_0_mean']])],
       [a_i - b_i for a_i, b_i in zip([x for x in agg['keys/node_100_mean']]  ,y)]]

experiment.setAxisLabel('Strategy','Keys/Node')
plt = experiment.getPlt()
plt.bar(x, height=y, width=[0.5], yerr=err, capsize=2)

experiment.saveOrShow(magic.SAVE_FILE)
