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
for i in range(iterations//10):
        name = "Virtual Nodes"
        experiment.addTask({'p': (name, size, 'virtual', i, numNodes, (1, 1), 0, None, 1, magic.BITS)})

        name = "Random"
        experiment.addTask({'p': (name, size, 'random', i, numNodes, (1, 1), 0, None, 1, 0)})

        name = "Best"
        experiment.addTask({'p': (name, size, 'best', i, numNodes, (1, 1), 0, None, 1, 0)})

        name = "Binary"
        experiment.addTask({'p': (name, size, 'binReal', i, numNodes, (1, 1), 0, None, 1, 0)})

        name = "Binary Light"
        experiment.addTask({'p': (name, size, 'bin', i, numNodes, (1, 1), 0, None, 1,0)})

experiment.execute()

aggMap = {'share_0': ['mean'],
          'share_50': ['mean'],
          'share_100': ['mean'],
          'maxShareY0': ['mean']}

agg = experiment.data

agg = agg.filter(items=[ 'name', 'share_0', 'share_50','share_100','maxShareY0']).groupby(['name']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['share_50_mean'],ascending = [1])

x = [str(a) for a in agg.index.tolist()]
y = list(agg['share_50_mean'].values)

err = [[a_i - b_i for a_i, b_i in zip(y, [x for x in agg['share_0_mean']])],
       [a_i - b_i for a_i, b_i in zip([x for x in agg['share_100_mean']]  ,y)]]

experiment.setAxisLabel('Strategy','share')
plt = experiment.getPlt()
plt.bar(x, height=y, width=[0.5], yerr=err, capsize=2)

experiment.saveOrShow(False)
