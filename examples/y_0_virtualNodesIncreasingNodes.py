import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pydht.magic as magic
from pydht.experiment import Experiment

nodeBase = 2
bits = magic.BITS
iterations = magic.ITERATIONS
experiment = Experiment('y_0_virtualNodesIncreasingNode', bits, 'y_0_virtualNodesIncreasingNode.png')
for i in range(iterations):
       for e in range(2, 9):
              numNodes = nodeBase ** e
              err = 0.1
              name = "2^" + str(e)
              experiment.addTask({'p': (name, bits, 'y0', i, numNodes,(1,0),err,None,1,i)})

experiment.execute()

aggMap = {'real/virt': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'real/virt']).groupby('name').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

x = agg.index.tolist()
y = agg['real/virt_mean'].values
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['real/virt_10-th percentile']))],
       [a_i - b_i for a_i, b_i in zip(list(agg['real/virt_90-th percentile']),y)]]

experiment.setAxisLabel('# of Nodes', 'Mean Number of Virtual Nodes/Real Node')
plt = experiment.getPlt()
plt.bar(x, height=y, width=[0.5], yerr=err, capsize=2)
#for i in range(len(x)):
#    plt.text(x=i - 0.05, y=y[i] + err[1][i] + 0.2, s=str(round(y[i], 2)), size=9)

experiment.saveOrShow(magic.SAVE_FILE)