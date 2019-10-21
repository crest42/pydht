import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pydht.magic as magic
from pydht.experiment import Experiment

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
numNodes = nodeBase ** nodeExp
bits = magic.BITS
iterations = magic.ITERATIONS

experiment = Experiment('y_0_virtualNodesIncreasingError', bits, 'y_0_virtualNodesIncreasingError.png')
for i in range(iterations):
       for e in range(0, 8):
              err = (e/10)
              name = str(err)
              experiment.addTask({'p': (name, bits, 'y0', i, numNodes,(1,0),err,None,1,i)})

experiment.execute()

aggMap = {'real/virt': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'real/virt']).groupby('name').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

x = agg.index.tolist()
y = list(agg['real/virt_mean'].values)
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['real/virt_10-th percentile']))],
       [a_i - b_i for a_i, b_i in zip(list(agg['real/virt_90-th percentile']),y)]]

experiment.setAxisLabel('Symetric Error Bound', 'Mean Number of Virtual Nodes/Real Node')

plt = experiment.getPlt()
plt.bar(x, height=y, yerr=list(err), capsize=2)

#for i in range(len(x)):
#       plt.text(x=i - 0.05, y=y[i] + err[1][i] + 0.2, s=str(round(y[i], 2)), size=9)
experiment.saveOrShow(magic.SAVE_FILE)
