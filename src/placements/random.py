from pydht import Dht
import pydht.magic as magic
import random

class Random:

    def __init__(self, dht: Dht) -> None:
        self.dht = dht

    def __get(self) -> int:
        return int(random.random()*self.dht.size)

    def __str__(self) -> str:
        return "Random"

    def __repr__(self) -> str:
        return self.__str__()

    def get(self) -> int:
        return self.__get()