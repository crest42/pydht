from pydht.nodeList.nodeList import nodeList
from pydht.nodeList.node.Node import Node
from typing import Tuple, List
import random
import numpy

class Dht:

    def __init__(self, name: str, bits: int, verbose: bool = False) -> None:
        self.verbose: bool = verbose
        self.n: int = bits
        self.size: int = (2 ** self.n)
        self.type: str = name
        self.nodeList: nodeList = nodeList(self.n)

    def __toStr(self) -> str:
        return "type: " + self.type + " size: " + str(self.size)

    def __repr__(self) -> str:
        return self.__toStr()

    def __str__(self) -> str:
        return self.__toStr()

    def addNode(self, id: int, virtId: int = 0, capacity: int = 0, master: bool = True, additional={}) -> int:
        return self.nodeList.addNode(id, virtId=virtId, capacity=capacity, master = master, additional=additional)

    def removeNodeWithVirt(self, id: int) -> int:
        return self.nodeList.removeNodeWithVirt(id)

    def removeNodeList(self, ids: List[int]) -> int:
        return self.nodeList.removeNodeList(ids)

    def addKey(self, ids: Tuple[int]) -> int:
        length = self.getNodeCount()
        targets = []
        for e in ids:
            targets.append(self.nodeList.findSuc(e))

        assert (len(targets) == len(ids))
        min = self.nodeList.getN(targets[0]).keyCount
        minid = 0
        for i in range(len(targets)):
            if self.nodeList.getN(targets[i]).keyCount < min:
                minid = i
                min = self.nodeList.getN(targets[i]).keyCount
        return self.nodeList.addKey(targets[minid],ids[minid])

    def addKeys(self, num: int, multiple: int = 1) -> int:
        i = 0
        for i in range(num):
            ids = []
            for i in range(multiple):
                ids.append(int(random.random() * self.size))
            i += self.addKey(ids)
        return i

    def getMaxIdSpace(self) -> Tuple[Node,int]:
        spaceList = self.getSpaceList()
        maxSpace = max(spaceList)
        maxId = spaceList.index(maxSpace)
        return (self.nodeList.getN(maxId).id,spaceList[maxId])

    def getMinIdSpace(self) -> Tuple[Node,int]:
        spaceList = self.getSpaceList()
        minSpace = min(spaceList)
        minId = spaceList.index(minSpace)
        return (self.nodeList.getN(minId).id,spaceList[minId])

    def getSpaceList(self) -> List[int]:
        return self.nodeList.getSpaceList()

    def getIdSpaceSum(self) -> int:
        return sum(self.getSpaceList())

    def getSpace(self, node: Node) -> int:
        return self.nodeList.getSpace(node)

    def getSpaceWithVirtualNodes(self, node) -> int:
        return self.nodeList.getSpaceWithVirtualNodes(node)

    def getNodeCount(self) -> int:
        return len(self.nodeList)

    def getMasterNodeCount(self) -> int:
        return self.nodeList.getMasterNodeCount()

    def getVirtualNodeCount(self) -> int:
        return self.nodeList.getVirtualNodeCount()

    def getKeyCount(self) -> int:
        return self.nodeList.getKeyCount()

    def flatKeyCount(self) -> List[int]:
        return self.nodeList.flatKeyCount()

    def getImbalance(self) -> float:
        return self.getMaxIdSpace()[1] / self.getMinIdSpace()[1]


    def getSharePercentile(self, percentile: int):
        shareList = self.nodeList.getShares()
        return numpy.percentile(shareList,percentile)

    def getMaxShareY0(self) -> float:
        return self.nodeList.getMaxShareY0()

    def getVirtualNodesAverage(self) -> float:
        return (self.getVirtualNodeCount()/self.getMasterNodeCount())

    def getVirtualNodesExtrema(self) -> float:
        min = self.size
        max = 0
        for x in self.nodeList:
            if x.master:
                vNodes = len(x.additional['nodeList'])-1
                if vNodes < min:
                    min = vNodes
                if vNodes > max:
                    max = vNodes
        return (min,max)

    def getKeyPercentile(self, percentile: int) -> numpy.ScalarType:
        return numpy.percentile(self.flatKeyCount(), percentile)

    def getAverageKeyPerNode(self) -> float:
        return (self.getKeyCount() / self.getMasterNodeCount())

    def nodeExists(self, id: int) -> bool:
        return self.nodeList.nodeExists(id)

    def getNode(self, node):
        return self.nodeList.getNode(node)