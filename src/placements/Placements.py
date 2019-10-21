from pydht import Dht
from pydht.placements.bin import Bin
from pydht.placements.bin import binReal
from pydht.placements.random import Random
from pydht.placements.best import Best
from pydht.placements.y0 import y0
import pydht.magic as magic
import numpy as np
import random
from typing import Tuple

class Placements:

    range = -1
    dht = None
    name = ''
    strat = None

    def __init__(self, dht: Dht, pStrat: str, phi: None) -> int:
        self.name = pStrat
        if pStrat == 'virtual':
            self.strat = self.startNodesWithVirtualNodes
            self.generator = Random(dht)
        elif pStrat == 'y0':
            self.strat = self.startNodesY0
            self.generator = Random(dht)
        elif pStrat == 'best':
            self.strat = self.startNodes
            self.generator = Best(dht)
        elif pStrat == 'bin':
            self.strat = self.startNodes
            self.generator = Bin(dht)
        elif pStrat == 'binReal':
            self.strat = self.startNodes
            self.generator = binReal(dht,phi)
        elif pStrat == 'binWeighted':
            self.strat = self.startNodesBinWeighted
            self.generator = Bin(dht)
        elif pStrat == 'binRealWeighted':
            self.strat = self.startNodesBinWeighted
            self.generator = binReal(dht,phi)
        else:
            self.strat = self.startNodes
            self.generator = Random(dht)

        self.dht = dht
        return

    def __repr__(self) -> str:
        return (self.name)

    def __str__(self) -> int:
        return self.__repr__()

    def __getNewNodeId(self) -> int:
        return self.generator.get()

    def start(self, args: Tuple):
        assert (self.strat != None)
        assert (self.generator != None)
        return self.strat(*args)

    def periodic(self) -> bool:
        return self.__periodic()

    def startNodesY0(self, num: int, error: float = 0.1) -> None:
        self.y0 = y0(self.dht)
        self.y0.error = error
        self.__periodic = self.y0.y0Periodic
        self.y0.startNodesY0(num)
        i = 100
        while (i > 0):
            c = self.periodic()
            if c == 0:
                i = 0
            i -= 1

    def __startNodesWithVirtualNodes(self, num: int, virt: int, capacity: int = 1, vId=-1) -> None:
        for i in range(0, num):
            virtIds = []
            for v in range(0, virt):
                id = self.__getNewNodeId()
                #Check for already existing node
                while (self.dht.nodeExists(id) or id in virtIds):
                    id = self.__getNewNodeId()
                virtIds.append(id)
                master = True
                if v > 0:
                    master = False
                if vId == -1:
                    self.dht.addNode(id, virtId=i, master=master, capacity=capacity)
                else:
                    self.dht.addNode(id, virtId=vId, master=master, capacity=capacity)
            self.dht.getNode(virtIds[0]).additional = {'nodeList': virtIds}

    def __getRandomCapacity(self, factor = -1) -> int:
        minCap = 2 ** magic.Y_0_CAP_LOW
        if factor <= 0:
            factor = magic.Y_0_CAP_HIGH - magic.Y_0_CAP_LOW
        return minCap * random.randrange(1,factor+1)

    def startNodesWithVirtualNodes(self, num: int, virt: int) -> None:
        self.__startNodesWithVirtualNodes(num, virt + 1)

    def startNodes(self, num: int) -> None:
        self.__startNodesWithVirtualNodes(num, 1)

    def startNodesBinWeighted(self, num: int, factor: int) -> None:

        for x in range(1, (num + 1)):
            capacity = self.__getRandomCapacity(factor)
            numNodes = capacity // (2 ** magic.Y_0_CAP_LOW)
            self.__startNodesWithVirtualNodes(1,numNodes,capacity = capacity, vId = x)