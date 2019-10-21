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
experiment = Experiment('y_0_loadImblanceIncreasingError', bits, 'y_0_loadImblanceIncreasingError.png')

for i in range(iterations):
       for e in range(0, 8):
              err = e/10
              name = str(err)
              experiment.addTask({'p': (name, bits, 'y0', i, numNodes,(1,0),err,None,1,0)})

experiment.execute()

aggMap = {'share': ['mean', 'std', experiment.percentile(10), experiment.percentile(90)]}
agg = experiment.data.filter(items=['name', 'iteration', '#nodes','share']).groupby('name').agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

x = agg.index.tolist()
y = agg['share_mean'].values
err = [[a_i - b_i for a_i, b_i in zip(y, list(agg['share_10-th percentile']))],
       [a_i - b_i for a_i, b_i in zip(list(agg['share_90-th percentile']),y)]]
fig1, ax1 = experiment.getPlt().subplots()
ax1.plot(x, y)
ax1.set_ylabel('loadImbalance')
ax1.set_xlabel('Error')
ax1.set_xticks(x)
experiment.saveOrShow(magic.SAVE_FILE)
