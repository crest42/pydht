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
    experiment.addTask({'p': (name, bits, 'random', i, numNodes,(1,0),0,None,1,0)})

    name = "Optimal"
    experiment.addTask({'p': (name, bits, 'best', i, numNodes,(1,0),0,None,1,0)})

    name = "Y0"
    experiment.addTask({'p': (name, bits, 'y0', i, numNodes,(1,0),0,None,1,0)})

    name = "Virtual Nodes"
    experiment.addTask({'p': (name, bits, 'virtual', i, numNodes,(1,0),0,None,1,bits)})

    name = "Binary Light"
    experiment.addTask({'p': (name, bits, 'bin', i, numNodes,(1,0),0,None,1,bits)})

experiment.execute()

aggMap = {'share_0': ['mean'],
          'share_50': ['mean'],
          'share_100': ['mean']}
agg = experiment.data.filter(items=['name', 'share_0','share_50','share_100']).groupby('name').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]
agg = agg.sort_values(['share_50_mean'],ascending = [0])    
x = agg.index.tolist()
y = agg['share_50_mean'].values
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['share_0_mean']))],
       [a_i - b_i for a_i, b_i in zip(list(agg['share_100_mean']), y)]]

experiment.setAxisLabel('Strategy', 'share(v)')
plt = experiment.getPlt()
plt.bar(x, height=y , width=[0.5], yerr=err, capsize=2)
#for i in range(len(x)):
#    plt.text(x=i - 0.05, y=y[i] + err[1][i] + 0.2, s=str(round(y[i], 2)), size=9)

experiment.saveOrShow(magic.SAVE_FILE)
