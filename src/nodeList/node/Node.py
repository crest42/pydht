class Node:

    def __init__(self, id: int, virtId: int = 0, capacity: int = 100, master: bool = True, additional={}) -> None:
        assert(type(id) == int)
        self.id = id
        self.virtId = virtId
        self.capacity = capacity
        self.master = master
        self.keyCount = 0
        self.additional = additional

    def __lt__(self,other):
        return (self.id<other)

    def __le__(self,other):
        return(self.id<=other)

    def __gt__(self,other):
        return(self.id>other)

    def __ge__(self,other):
        return(self.id>=other)

    def __eq__(self,other):
        return (self.id==other)

    def __ne__(self,other):
        return not(self.__eq__(self,other))

    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return self.__repr__()

    def sort(self) -> int:
        return self.id

    def addKey(self,id: int) -> int:
        self.keyCount += 1
        return self.keyCount

    def removeKey(self,id: int) -> None:
        self.keyCount -= 1

    def getKeyCount(self) -> int:
        return self.keyCount
    def getCapacity(self) -> int:
        return self.capacity
