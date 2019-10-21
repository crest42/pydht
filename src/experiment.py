
from pydht.Dht import Dht
from pydht.placements.Placements import Placements
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import multiprocessing as mp

class Experiment:

    baseDir = './experiments/results/'
    filename = ''
    name = ''

    def __init__(self, name, size, filename):
        plt.style.use('seaborn-whitegrid')
        self.filename = filename
        self.data = pd.DataFrame()
        self.lastStart = 0
        self.collectTime = []
        self.execTimes = []
        self.runCount = 0
        self.workers = []
        self.tasks = []

    def __addDhtAndStart(self, name, bits, placementStrategie, iteration, numNodes, keys, error, phi, multiple, virt):
        start = time.process_time()
        df = pd.DataFrame()
        dht = Dht(name, bits, verbose=False)
        p = Placements(dht, placementStrategie,phi)
        if placementStrategie == 'y0':
            p.start((numNodes,error))
        elif placementStrategie == 'virtual':
            p.start((numNodes, virt))
        elif placementStrategie == 'binWeighted' or placementStrategie == 'binRealWeighted':
            p.start((numNodes,virt))
        else:
            p.start((numNodes,))
        for i in range(0, keys[0]):

            dht.addKeys(keys[1], multiple=multiple)
            flatKeyCount = dht.flatKeyCount()
            shareList = dht.nodeList.getShares()
            vNodeMinMax =  dht.getVirtualNodesExtrema()
            data = {'name': [name],
                    'iteration': iteration,
                    '#nodes': dht.getMasterNodeCount(),
                    'virtNodes': virt,
                    'keys': dht.getKeyCount()+keys[1],
                    'share': dht.getImbalance(),
                    'share_min': dht.getMinIdSpace()[1],
                    'share_max': dht.getMaxIdSpace()[1],
                    'keys/node': dht.getAverageKeyPerNode(),
                    'keys/node_0': np.percentile(flatKeyCount,0),
                    'keys/node_10': np.percentile(flatKeyCount,10),
                    'keys/node_50': np.percentile(flatKeyCount,50),
                    'keys/node_90': np.percentile(flatKeyCount,90),
                    'keys/node_100':np.percentile(flatKeyCount,100),
                    'real/virt': dht.getVirtualNodesAverage(),
                    'real/virt_min': vNodeMinMax[0],
                    'real/virt_max': vNodeMinMax[1],
                    'share_0': np.percentile(shareList,0),
                    'share_100': np.percentile(shareList,100),
                    'share_50': np.percentile(shareList,50),
                    'maxShareY0': np.percentile(shareList, 100),
                    'time': time.process_time()-start}
            df = df.append(pd.DataFrame(data), ignore_index=True)

        end = time.process_time()
        return (df,  end -start)

    def __collect(self, result):
        aE = time.time()
        self.data = self.data.append(result[0], ignore_index=True)
        self.collectTime.append(time.time()-aE)
        self.runCount += 1
        self.execTimes.append(result[1])
        if self.runCount % (self.sumRuns / 10) == 0:
            self.lastEnd = time.time()
            tpn = (self.lastEnd-self.lastStart)/(self.sumRuns // 10)
            print("done: " + str(self.runCount) + "/" + str(self.sumRuns) + " (" + str((100 / (self.sumRuns)) * self.runCount) + "%) in " +
                   str(self.lastEnd - self.lastStart) + " s (" + str((self.sumRuns - self.runCount) * tpn) + " remaining) collect: " + str(sum(self.collectTime)))
            print("avarage exec time: " + str(sum(self.execTimes)/len(self.execTimes)))
            self.lastStart = time.time()
            self.collectTime = []

    def __worker(self, inQueue, outQueue):
        tA = []
        done = 0
        start = time.time()
        while (True):
            args = inQueue.get()
            if args == None:
                break
            done += 1
            (df, t) = self.__addDhtAndStart(*args)
            tA.append(t)
            outQueue.put((df, t))
        print("Worker done " + str(done) + " tasks in " + str(time.time() - start) + " Seconds " + str(sum(tA)) + " was execution")
        outQueue.put(None)

    def execute(self, processes=mp.cpu_count()):
        inQueue = mp.Queue()
        outQueues = []
        self.sumRuns = len(self.tasks)
        self.lastStart = time.time()
        for x in self.tasks:
            args = x['p']
            inQueue.put(args)

        for i in range(processes):
            inQueue.put(None)

        for i in range(processes):
            outQueues.append(mp.Queue())
            self.workers.append(mp.Process(target=self.__worker,args = (inQueue,outQueues[-1])))
            self.workers[-1].start()

        while (self.runCount < self.sumRuns):
            for x in outQueues:
                val = x.get()
                if val != None:
                    self.__collect(val)
                else:
                    outQueues.remove(x)

        for x in self.workers:
            x.join()

        assert(self.runCount > 0)
        print("exec time total: " + str(sum(self.execTimes)) + " s\navg exec time/task: " + str(sum(self.execTimes) / len(self.execTimes)) + " s\nruns: " + str(self.runCount))
        return self.data

    def addTask(self, task):
        self.tasks.append(task)

    def percentile(self,n):
        def _percentile(x):
            return np.percentile(x, n)
        _percentile.__name__ = '{}-th percentile'.format(n)
        return _percentile

    def getPlt(self):
        return plt

    def setAxisLabel(self, xLabel, yLabel):
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)

    def saveOrShow(self, save):
        if (save):
            plt.savefig(self.baseDir + self.filename)
        else:
            plt.show()