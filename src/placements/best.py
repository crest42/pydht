from pydht import Dht
import pydht.magic as magic

class Best:

    def __init__(self, dht: Dht) -> None:
        self.dht = dht

    def __str__(self) -> str:
        return "best"

    def __repr__(self) -> str:
        return self.__str__()

    def __get(self) -> int:
        if self.dht == None:
            return -1
        if self.dht.nodeList.empty():
            return self.dht.size // 2
        ret = -1
        m = self.dht.getMaxIdSpace()
        if m[0] == 0:
            ret = self.dht.size - (m[1] / 2)
        else:
            ret = m[0] - (m[1] / 2)
        assert (ret >= 0)
        return int(ret)

    def get(self) -> int:
        return self.__get()