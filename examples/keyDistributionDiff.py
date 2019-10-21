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

experiment = Experiment('loadImbalance', bits, 'loadImbalance.png')

for i in range(iterations):

    name = "Random"
    experiment.addTask({'p': (name, bits, 'random', i, numNodes,(1,10000),0,None,1,0)})

    name = "Hash"
    experiment.addTask({'p': (name, bits, 'random', i, numNodes,(1,10000),0,None,bits,0)})

    name = "Virtual Nodes"
    experiment.addTask({'p': (name, bits, 'virtual', i, numNodes,(1,10000),0,None,1,bits)})

    name = "Y0"
    experiment.addTask({'p': (name, bits, 'y0', i, numNodes,(1,10000),0,None,1,0)})

    name = "Binary"
    experiment.addTask({'p': (name, bits, 'binReal', i, numNodes,(1,10000),0,None,1,0)})

    name = "Binary Light"
    experiment.addTask({'p': (name, bits, 'bin', i, numNodes,(1,10000),0,None,1,0)})

    name = "Binary Weighted"
    experiment.addTask({'p': (name, bits, 'binRealWeighted', i, numNodes,(1,10000),0,None,1,0)})

    name = "Binary Light Weighted"
    experiment.addTask({'p': (name, bits, 'binWeighted', i, numNodes,(1,10000),0,None,1,0)})

experiment.execute()
aggMap = {'keys/node': ['mean'],
        'keys/node_0': ['mean'],
        'keys/node_50': ['mean'],
        'keys/node_100': ['mean'],
        '#nodes' : ['mean']}
agg = experiment.data.filter(items=['name', '#nodes', 'keys/node','keys/node_0','keys/node_50','keys/node_100']).groupby(['name','#nodes']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
print(agg)
