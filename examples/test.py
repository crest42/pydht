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
increments = magic.NODE_INCREMENTS
xAxis = []
experiment = Experiment('loadImbalanceBinMethod',bits,'loadImbalanceBinMethod.png')

for i in range(1):
        name = "Binary"
        experiment.addTask({'p': (name, bits, 'binReal', i, numNodes,(1,0),0,None,1,0)})

        name = "Binary Light"
        experiment.addTask({'p': (name, bits, 'bin', i, numNodes,(1,0),0,None,1,0)})

experiment.execute()

aggMap = {'share': ['mean', 'std']}
agg = experiment.data.filter(items=['name', '#nodes', 'share']).groupby(['name','#nodes']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['share_mean'],ascending = [0])
print(agg)