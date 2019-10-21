import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import pydht.magic as magic
from pydht.experiment import Experiment
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

bits = 32

class Node:
  def __init__(self,level = -1,internal = True,c = 1):
    self.level = level
    self.c = c
    if internal == True:
      self.childs = 2
    else:
      self.childs = 0
    self.ancestor = None
    self.internal = internal
    self.left = None
    self.right = None
    self.size = 2**bits
    if self.level == 0:
      self.active = True
      self.left = Node(1,internal = False)
      self.left.id = 0
      self.left.ancestor = self
    else:
      self.active = False

  def __str__(self):
    if self.internal == True:
      type = "Internal"
      if self.active == True:
        type = type + " active"
      else:
        type = type + " inactive"
      appendix = ""
    else:
      type = "Leave"
      appendix = " with id " + str(self.id)

    return type + " node at level: " + str(self.level) + appendix

  def __repr__(self):
    return self.__str__()

  def __phi(self,l):
    if l == 0:
      phi = 0
    else:
      phi = np.max([0,l-np.ceil(np.log2(l))-self.c])
    return phi

  def getImbalance(self):
    x = [y.id for y in self.flattn()]
    space = [np.mod(a-x[x.index(a)-1],2**bits) for a in x]
    return np.max(space)/np.min(space)

  def flattn(self):
    l = []
    if self.left != None:
      r = self.left.flattn()
      if isinstance(r,list):
        for i in r:
          l.append(i)
      else:
        l.append(r)
    else:
      return self
    if self.right != None:
      r = self.right.flattn()
      if isinstance(r,list):
        for i in r:
          l.append(i)
      else:
        l.append(r)
    else:
      return self

    return l

  def getRightmost(self,node):
    while node.right != None:
      node = node.right
    return node

  def getLeftmost(self,node):
    while node.left != None:
      node = node.left
    return node

  def toBin(self):
    return bin(self.id)

  def getPre(self):
    a = self
    while a.ancestor != None and a.ancestor.left == self:
     a = a.ancestor
    return a.getRightmost(a.left)

  def getSuc(self):
    a = self
    while a.ancestor != None and a.ancestor.right == a:
     a = a.ancestor
    if a.ancestor == None:
      return a.getLeftmost(a)
    else:
      return a.getLeftmost(a.ancestor.right)

  def bulkInsert(self,num):
    for i in range(0,num):
      self.insert()

  def insert(self):
    if self.right == None and self.level == 0:
      node = Node(level = self.level +1, internal= False)
      node.id = self.size//2
      node.ancestor = self
      self.right = node
    else:
      r = self.getRandom()
      a = r.getActiveAncestor()
      s = a.getSplitNode()
      suc = s.getSuc()
      newInternal = Node(level = s.level,internal = True)
      newLeave    = Node(level = s.level+1,internal = False)
      newId = np.mod(s.id + (np.mod(suc.id-s.id,self.size)//2),self.size)
      newLeave.id = newId

      newInternal.ancestor = s.ancestor

      s.ancestor = newInternal
      newLeave.ancestor = newInternal

      newInternal.right = newLeave
      newInternal.left  = s

      s.level = newInternal.level+1
      if newInternal.ancestor.left == s:
        newInternal.ancestor.left = newInternal
      else:
        newInternal.ancestor.right = newInternal
      newInternal.incNodes()
      l = newLeave.level
      l_a = a.level

      if (a.left.internal == True and a.right.internal == True) and a.level != self.__phi(l+1):
        assert(a.left.internal == True and a.right.internal == True)
        a.active = False
        a.left.active = True
        a.right.active = True

  def checkLevel(self,leave):
    if leave.ancestor.left != None and leave.ancestor.right != None:
      return True
    else:
      return False

  def incNodes(self):
    a = self.ancestor
    while a != None:
      a.childs += 1
      a = a.ancestor

  def getSplitNode(self):
    if self.left == None and self.right != None:
      return self.right.getSplitNode()
    elif self.right == None and self.left != None:
      return self.left.getSplitNode()
    elif self.right != None and self.left != None:
      if self.right.childs <= self.left.childs:
        return self.right.getSplitNode()
      else:
        return self.left.getSplitNode()
    else:
      return self

  def getRandom(self):
    if self.left == None and self.right != None:
      return self.right.getRandom()
    elif self.right == None and self.left != None:
      return self.right.getRandom()
    elif self.left != None and self.right != None:
      if random.randint(1,2) == 1:
        return self.right.getRandom()
      else:
        return self.left.getRandom()
    else:
      return self

  def getActiveAncestor(self):
    assert(self.internal == False)
    n = self
    while n.ancestor.active == False:
      n = n.ancestor
    return n.ancestor

nodeBase = magic.NUMNODE_BASE
nodeExp = magic.NUMNODE_EXP
bits = magic.BITS
numNodes = nodeBase ** nodeExp
iterations = magic.ITERATIONS
increments = magic.NODE_INCREMENTS-2
xAxis = []
experiment = Experiment('loadImbalanceBinMethod',bits,'loadImbalanceBinMethod.png')

df = pd.DataFrame()
for i in range(iterations):
    for e in range(increments):
        numNodes = 2 ** e
        if str(numNodes) not in xAxis:
                xAxis.append(str(numNodes))

        name = "Virtual Nodes"
        experiment.addTask({'p': (name, bits, 'virtual', i, numNodes, (1, 0), 0, None, 1, bits)})

        name = "Binary Light"
        experiment.addTask({'p': (name, bits, 'bin', i, numNodes,(1,0),0,None,1,0)})

        for tmp in range(1,6):
          root = Node(level = 0,c = tmp)
          root.bulkInsert(numNodes)
          data = {
            'name': ["Binary c = " + str(tmp)],
            'root': root,
            'c': tmp,
            '#nodes': numNodes,
            'share': root.getImbalance()}
          df = df.append(pd.DataFrame(data), ignore_index=True)

experiment.execute()

aggMap = {'share': ['mean']}
agg = experiment.data.filter(items=['name', '#nodes', 'share']).groupby(['name','#nodes']).agg(aggMap)
agg.columns = ["_".join(x) for x in agg.columns.ravel()]

aggMap2 = {'share': ['mean']}
agg2 = df.filter(items=['name','#nodes','share']).groupby(['name', '#nodes']).agg(aggMap2)
agg2.columns = ["_".join(x) for x in agg2.columns.ravel()]

result = pd.concat([agg, agg2])
result = result.sort_values(['share_mean'],ascending = [0])
x = result.index.tolist()
y = result['share_mean'].values
legend = list(set([e[0] for e in x]))
legend.sort()
values = [result.loc[e].sort_values('#nodes') for e in legend]

experiment.setAxisLabel('# of Nodes', 'load imbalance')
experiment.getPlt().style.use('seaborn-whitegrid')

for k in values:
        experiment.getPlt().plot(xAxis, list(k['share_mean']))

experiment.getPlt().xticks(xAxis)
experiment.getPlt().legend(legend)
experiment.saveOrShow(magic.SAVE_FILE )