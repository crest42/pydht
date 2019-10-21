from pydht import Dht
import pydht.magic as magic
import random
import numpy

class Bin:

    def __init__(self, dht: Dht) -> None:
        self.dht = dht

    def __str__(self) -> str:
        return "bin"

    def __repr__(self) -> str:
        return self.__str__()

    def __get(self) -> int:
        if self.dht == None:
            return
        if self.dht.nodeList.empty():
            return int(self.dht.size / 2)
        if len(self.dht.nodeList) == 1:
            return int(self.dht.nodeList.getN(0).id - (self.dht.getSpace(self.dht.nodeList.getN(0))/2))
        nodes = self.dht.nodeList.getRandomNodes(self.dht.n)
        i = 0
        max = 0
        maxId = None
        while i < len(nodes):
            space = self.dht.getSpace(nodes[i])
            if space > max:
                maxId = []
                maxId.append(i)
                max = space
            elif space == max:
                maxId.append(i)
            i += 1
        assert (maxId != [])
        maxId = random.choice(maxId)
        index = self.dht.nodeList.get(nodes[maxId])
        space = self.dht.getSpace(nodes[maxId])
        id = self.dht.nodeList.getN(index).id - (space / 2)
        return int(numpy.mod(id, self.dht.size))

    def get(self) -> int:
        return self.__get()


class binReal:

    def __init__(self, dht: Dht, phi = None) -> None:
        self.dht = dht
        self.phi = phi
        self.c = 1

    def __str__(self) -> str:
        return "binReal"

    def __repr__(self) -> str:
        return self.__str__()

    def __phi(self, l: int) -> int:
        if (self.phi != None):
            return self.phi
        return 2
        return numpy.max([0,l - int(numpy.ceil(numpy.log2(l))) - self.c])

    def __get(self) -> int:
        if self.dht == None:
            return
        if self.dht.nodeList.empty():
            return 0
        if (len(self.dht.nodeList) == 1):
                return int(self.dht.size // 2)

        l = self.dht.n
        r = self.dht.nodeList.getRandomNodes(1)[0]
        S_r = self.dht.nodeList.getSharedIdNodes(r, self.__phi(l))
        if (self.__phi(l) == self.dht.n):
            assert(len(S_r) == 0)

        if (len(S_r) >= 2 ** (l - self.__phi(l))) or len(S_r) == 0:
            return self.getIdHalve(r)
        else:
            return self.getIdHalveSelect(S_r)
        assert(False)

    def get(self) -> int:
        return self.__get()

    def getIdHalve(self, node) -> int:
        index = self.dht.nodeList.get(node)
        space = 0
        if index == 0:
            space = self.dht.size - self.dht.nodeList.getN(-1).id + node.id
        else:
            space = node.id - self.dht.nodeList.getN(index-1).id
        return int(numpy.mod((node.id-(space//2)),self.dht.size))

    def getIdHalveSelect(self, nodeList) -> int:
        i = 0
        max = 0
        maxId = None
        while i < len(nodeList):
            space = self.dht.getSpace(nodeList[i])
            if space > max:
                maxId = []
                maxId.append(i)
                max = space
            elif space == max:
                maxId.append(i)
            i += 1
        assert (maxId != [])
        maxId = random.choice(maxId)
        return self.getIdHalve(nodeList[maxId])