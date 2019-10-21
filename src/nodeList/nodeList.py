from pydht.nodeList.node.Node import Node
from typing import List
import random
import numpy
import bisect

class nodeList:

    def __init__(self,n: int) -> None:
        self.__nodeList: List[Node] = []
        self.__masterNodeCapacities: int = 0
        self.keyCount: int = 0
        self.masterNodes: int = 0
        self.n: int = n
        self.size: int = (2**self.n)

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self) -> Node:
        if self.__current == len(self):
            raise StopIteration
        else:
            self.__current += 1
            return self.__nodeList[self.__current - 1]

    def __repr__(self) -> str:
        s = '['
        i = 0
        for x in self.__nodeList:
            s += str(x.id) + "(" + str(x.virtId) + ")"
            i += 1
            if i != len(self.__nodeList):
                s += ","
        return s + "]"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.__nodeList)

    def __inInterval(self, a: int, b: int, id: int) -> bool:
        return (numpy.mod(id-a,self.size) < numpy.mod(b-a,self.size))

    def findSuc(self, id) -> int:
        return (bisect.bisect_right(self.__nodeList, id)%len(self))

    def insert(self, n: Node) -> None:
        assert(type(n) == Node)
        bisect.insort(self.__nodeList, n)

    def getSpaceList(self) -> List[int]:
        if self.empty():
            return []
        maxId = len(self)
        if maxId == 1:
            return [self.size]

        i = 1
        realNodeList = {}
        realNodeList[self.getN(0).virtId] = self.getN(0).id + self.size - self.getN(maxId-1).id
        while i < maxId:
            n = self.getN(i)
            virtId = n.virtId
            space = self.getN(i).id - self.getN(i - 1).id
            if virtId in realNodeList:
                realNodeList[virtId] += space
            else:
                realNodeList[virtId] = space
            i += 1
        return list(realNodeList.values())

    def addNode(self, id: int, virtId: int = 0,capacity: int = 0,master: bool = True,additional={}) -> int:
        return self.add(Node(id, virtId=virtId, capacity=capacity, master = master, additional=additional))

    def add(self, node: Node) -> int:
        assert(type(node) == Node)
        self.insert(node)
        if node.master == True:
            self.__masterNodeCapacities += node.capacity
            self.masterNodes += 1
        return 0

    def addKey(self, n: int, k: int) -> int:
        assert (n < len(self))
        self.keyCount += 1
        return self.getN(n).addKey(k)

    def get(self, node) -> int:
        i = bisect.bisect_left(self.__nodeList, node)
        if i != len(self) and self.__nodeList[i] == node:
            return i
        else:
            assert(False)
            return - 1

    def getNode(self, node) -> Node:
        return self.__nodeList[self.get(node)]

    def __pop(self, id) -> Node:
        node = self.__nodeList[id]
        self.keyCount -= node.getKeyCount()
        if node.master == True:
            self.masterNodes -= 1
            self.__masterNodeCapacities -= node.capacity
        if id <= self.__current:
                    self.__current -= 1
        return self.__nodeList.pop(id)

    def __remove(self, node) -> Node:
        return self.__pop(self.get(node))

    def removeNodeWithVirt(self, virtId: int) -> int:
        i = 0
        for node in self.__nodeList:
            if node.virtId == virtId:
                self.__remove(node)
                i += 1
        return i

    def removeNodeList(self, ids: List[int]) -> int:
        for id in ids:
            self.__pop(self.get(id))
        return len(ids)

    def getKeyCount(self) -> int:
        return self.keyCount

    def flatKeyCount(self) -> List[int]:
        realNodeList = {}
        for i in self.__nodeList:
            virtId = i.virtId
            if virtId in realNodeList:
                realNodeList[virtId] += i.getKeyCount()
            else:
                realNodeList[virtId] = i.getKeyCount()

        return list(realNodeList.values())

    def getN(self, n: int) -> Node:
        return self.__nodeList[n]

    def getSpace(self, node) -> int:
        if len(self) == 1:
            return self.size
        space = 0
        index = self.get(node)
        indexPre = index-1
        if index == 0:
            space = (self.size-self.getN(indexPre).id) + self.getN(index).id
        else:
            space = self.getN(index).id - self.getN(indexPre).id
        return space

    def getSpaceWithVirtualNodes(self, node) -> int:
        if len(self) == 1:
            return self.size
        space = 0
        for x in self.__nodeList:
            if x.virtId == node.virtId:
                space += self.getSpace(x)
        return space

    def getSpaceNodeList(self, ids: List[int]) -> int:
        if len(self) == 1:
            return self.size
        space = 0
        for id in ids:
                space += self.getSpace(id)
        return space

    def virtIdExists(self, virtId: int) -> bool:
        for node in self.__nodeList:
            if node.virtId == virtId:
                return True
        return False

    def getShares(self) -> List[float]:
        shareList = []
        avgCap = self.getSumMasterCapacities() / self.getMasterNodeCount()
        for x in self.__nodeList:
            if x.master == True:
                cv = x.capacity / avgCap
                if ('nodeList' in x.additional):
                    space = self.getSpaceNodeList(x.additional['nodeList']) / self.size
                else:
                    space = self.getSpaceWithVirtualNodes(x) / self.size
                assert (space < self.size)
                share = space / (cv / self.getMasterNodeCount())
                shareList.append(share)
        return shareList

    def getMaxShareY0(self) -> float:
        max = -1
        maxid = -1
        avgCap = self.getSumMasterCapacities() / self.getMasterNodeCount()
        for x in self.__nodeList:
            if x.master == True:
                cv = x.capacity / avgCap
                if('nodeList' in x.additional):
                    space = self.getSpaceNodeList(x.additional['nodeList']) / self.size
                else:
                    space = self.getSpace(x) / self.size
                assert (space < self.size)
                share = space / (cv / self.getMasterNodeCount())
                if share > max:
                    max = share
        return max

    def getMasterNodeCount(self) -> int:
        return self.masterNodes

    def getVirtualNodeCount(self) -> int:
        return (len(self)-self.masterNodes)

    def __getById(self,list, nodeId, s, e):
        if e < s:
            return - 1
        m = (s + e) // 2
        if list[m].id == nodeId:
            return m
        elif list[m].id < nodeId:
            return self.__getById(list, nodeId, (m+1), e)
        else:
            return self.__getById(list, nodeId, s, (m-1))

    def getById(self, nodeId: int) -> int:
        return self.__getById(self.__nodeList, nodeId, 0, len(self)-1 )

    def getSumMasterCapacities(self) -> int:
        return self.__masterNodeCapacities

    def empty(self) -> bool:
        if len(self) == 0:
            return True
        return False

    def nodeExists(self, id: int) -> bool:
        if len(self) == 0:
            return False
        if self.getById(id) == -1:
            return False
        return True

    def getRandomNodes(self, num: int) -> List[Node]:
        assert(len(self) > 0)
        nodes = [self.__nodeList[self.findSuc(int(random.random()*self.size))]]
        index = self.get(nodes[0])
        to = (index + num)
        while index < to and self.__nodeList[(index+1) % len(self)].id != nodes[0].id:
            index += 1
            nodes.append(self.__nodeList[index % len(self)])
        return nodes

    def getSharedIdNodes(self, node: int, bits: int) -> List[Node]:
        ret = []
        maskLow = (self.size - (1 << (self.n - bits)))
        maskHi  = ((1<<((self.n - bits)))-1)
        last    = (self.findSuc((node.id & maskLow))-1)
        while (last < len(self)):
            e = self.__nodeList[last]
            if (e.id >= (node.id & maskLow)) and (e.id <= (node.id | maskHi)):
                ret.append(e)
            else:
                break
            last += 1

        return ret