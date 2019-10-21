from pydht import Dht
from pydht.nodeList.node import Node
from typing import Tuple, List
import pydht.magic as magic
import random
import numpy

class y0:

    def __init__(self, dht: Dht) -> None:
        self.dht: Dht = dht
        self.error: float = magic.ERROR
        return

    def __str__(self) -> str:
        return "y0"

    def __repr__(self) -> str:
        return self.__str__()

    def __getNewNodeId(self) -> int:
        return int(random.random() * self.dht.size)

    def getError(self) -> float:
        return self.error

    def applyError(self, n: float) -> int:
        bound = int(numpy.ceil(n * self.error))
        if bound == 0:
            return n
        return random.randrange(n-bound,n+bound)

    def y0Reselect(self, node: Node, n: int, cv: int, recurseCall: bool = False) -> None:
        self.dht.removeNodeList(node.additional['nodeList'])
        self.startNodesY0(1, parameter = (node.virtId,n,cv,node.capacity), recurseCall=recurseCall, pv=node.additional['pv'])

    def estimateN(self) -> int:
        return self.applyError(self.dht.getMasterNodeCount())

    def estimateCv(self,n) -> int:
        return 0 if (n == 0) else int(self.applyError(self.dht.nodeList.getSumMasterCapacities()) / n)

    def getEstimates(self) -> Tuple[int,int]:
        n = self.estimateN()
        return (n, self.estimateCv(n))

    def y0Periodic(self) -> int:
        numChanges = 0
        for node in self.dht.nodeList:
            if not node.master:
                continue
            n, estCv = self.getEstimates()
            if n  == 0 or estCv == 0:
                return 0
            cv = node.capacity / estCv
            change = False
            if cv >= (magic.Y0_RESELECT_FACTOR * node.additional['estCv']):
                change = True
            elif node.additional['spacing'] < (1 / (2 * n)) or node.additional['spacing'] > (2 / n):
                change = True
            if change:
                numChanges += 1
                self.y0Reselect(node, n, cv, recurseCall=True)
        return numChanges

    def getY0Initial(self, i: int) -> Tuple[int,int,int,int]:
        capacity = self.getRandomCapacity(magic.Y_0_CAP_HIGH, magic.Y_0_CAP_HIGH)
        n, cv = self.getEstimates()
        if (cv == 0):
            cv = 1
        else:
            cv = capacity / cv
        return (capacity, n, cv, i)

    def startNodesY0(self, num: int, parameter: Tuple = tuple(), pv: int = -1, recurseCall: int = False) -> None:
        for i in range(num):
            (capacity, n, cv, virt) = self.getY0Initial(i)
            assert (virt == i)
            if len(parameter) == 4:
                virt, n, cv, capacity = parameter
            log = numpy.log2(n) if n > 0 else 0
            spacing = numpy.power(2, -(numpy.floor(0.5 + log)))
            t = True
            while t:
                (nodeIDs, newPv) = self.y0GetVirtIds(n, cv, spacing, pv=pv)
                t = False
                if (cv != -1):
                    for n in nodeIDs:
                        if self.dht.nodeExists(n):
                            t = True
                            break
            master = True
            for i in nodeIDs:
                data = {'estCv': cv, 'estN': n, 'spacing': spacing, 'pv': newPv}
                if master:
                    data['nodeList'] = nodeIDs
                    data['numNodes'] = len(nodeIDs)
                self.dht.addNode(i, virtId=virt, capacity=capacity, additional=data, master=master)
                master = False

    def alpha(self, n: int) -> int:
        if (n == 0):
            return 0
        return numpy.ceil(2*numpy.log2(n))

    def y0GetVirtIds(self, n: int, cv: int, spacing: float,pv: int = -1 ) -> Tuple[List[int],int]:
        id = -1
        if pv != -1:
            id = pv
        else:
            id = self.__getNewNodeId()
            while self.dht.nodeExists(id):
                id = self.__getNewNodeId()
            pv = id
        assert(id >= 0)
        size = self.dht.size
        id = (id / size)
        if spacing < 0:
            start = (id // spacing) * spacing
        else:
            start = id

        m = int(numpy.floor(0.5 + (cv * self.alpha(n))))
        ids = []
        if (m == 0):
            ids.append(int(start*size))
        for i in range(1,m):
            ri = self.__getNewNodeId() / size
            id = start - ((i + ri) * spacing)
            id = int(id * size)
            ids.append(int(numpy.mod(id, size)))
        return (ids,pv)

    def getRandomCapacity(self, lower: int, upper: int) -> int:
        exp = lower + int(random.random() * (upper - lower))
        return (2 ** exp)