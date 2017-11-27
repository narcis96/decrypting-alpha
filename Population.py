import os, progressbar, threading, random, time, bisect
import numpy as np
import statistics as stats
from thread import ThreadPool
from DNA import DNA
BAR_LENGTH = 5
def worker(data, encoded, cost, wordsDict):
    for dna in data:
        dna.CalcFitness(encoded, cost, wordsDict)

class Population:
    def __init__(self, threadsCount,data, mutationRate, encoded, cost, wordsDict, hints):
        self.__data = data
        self.__matingPool = []
        self.__generation = 0
        self.__bestScore = 0
        self.__mutationRate = mutationRate
        self.__encoded = encoded
        self.__cost = cost
        self.__wordsDict = wordsDict
        self.__hints = hints
        self.__threadPool = ThreadPool(threadsCount)
        self.__threadsCount = threadsCount
        self.__consecutiveScores = 0
        self.__lastScore = -1
        self.__weights = [1 for i in range(len(encoded))]

    @classmethod
    def Random(cls, threadsCount, count, length, mutationRate, encoded, cost, wordsDict, hints):
        data = [DNA.Random(length, hints) for i in range(count)]
        return cls(threadsCount, data, mutationRate, encoded, cost, wordsDict, hints)

    @classmethod
    def FromFolder(cls, threadsCount, path, count, length, mutationRate, encoded, cost, wordsDict, hints):
        data = []
        for file in os.listdir(path):
           if file.endswith('.json'):
               data.append(DNA.ReadFromJson(path + file))
        print('Loaded ', len(data), 'samples')
        if len(data) < count:
            count = count - len(data)
            print ('Adding ', count, 'random samples...')
            data = data + [DNA.Random(length, hints) for i in range(count)]
        return cls(threadsCount, data,  mutationRate, encoded, cost, wordsDict, hints)

    def Print(self, printAll, saveBest):
        average = stats.mean(self.__scores)
        maxScore = max(self.__scores)
        self.__generation = self.__generation + 1

        os.makedirs('./generation/best/', exist_ok = True)
        if printAll:
            saveFolder = './generation/' + str(self.__generation)
            os.makedirs(saveFolder, exist_ok = True)
            scoresFile = open(saveFolder + '/scores.txt', 'w')
            for i,dna in enumerate(self.__data):
                print(i, dna.GetScore(), file = scoresFile)
            for i,dna in enumerate(self.__data):
                dna.WriteJson(saveFolder + '/' + str(i) + '.json')
            print(average, file = open(saveFolder + '/average.txt', 'w'))

        if average > self.__bestScore:
            self.__bestScore = average
            if saveBest:
                for i,dna in enumerate(self.__data):
                    dna.WriteJson('./generation/best/' + str(i) + '.json')

        for dna  in self.__data:
            if dna.GetScore() == maxScore:
                decoded = dna.decode(self.__encoded)
                print('best match: ',decoded)
                if printAll:
                    print(decoded, file=open(saveFolder + '/best.txt', 'w'))
                #break
    
        print('generation: ', self.__generation, ' average score : ', average, ' max score: ', max(self.__scores),'\n')
        '''
        print('in Print')
        for dna in self.__data:
            print(dna)
        print('\n')
        '''
    def CalcFitness(self):
        startTime = time.time()
        bad = 0.4
        for dna in self.__data:
           dna.CalcFitness(self.__encoded, len(self.__encoded), self.__cost, self.__wordsDict, bad, self.__weights)
        length = len(self.__data)
#        self.__threadPool.Start(lambda dna, encoded, cost, wordsDict: dna.CalcFitness(encoded, cost, wordsDict), list(zip(self.__data, [self.__encoded] * length, [self.__cost]*length, [self.__wordsDict]*length)))
 #       self.__threadPool.Join()
        '''
        threads = []
        for threadId in range(self.__threadsCount):
            data = [self.__data[i] for i in range(length) if i % self.__threadsCount == threadId]
            thread = threading.Thread(target=worker, args = (data, self.__encoded, self.__cost, self.__wordsDict, ))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        '''
        #bar = progressbar.ProgressBar(maxval=length)
        #show = [randint(0, BAR_LENGTH) for i in range(length)]
        #if show[indx] == 0:
        #   bar.update(indx + 1)
        #bar.finish()
        print("%s seconds elpased" % (time.time() - startTime))
        self.__scores = [dna.GetScore() for dna in self.__data]

    def __PickOne(self, cumulativeSums, maxSum):
        index = 0
        value = np.random.rand() * maxSum
        return bisect.bisect_left(cumulativeSums, value)

    def Stuck(self, maxScore):
        if maxScore == self.__lastScore:
            self.__consecutiveScores = self.__consecutiveScores + 1
        else:
            self.__consecutiveScores = 1
        
        self.__lastScore = maxScore
        if self.__consecutiveScores == 10:
           return True
        return False

    def NaturalSelection(self):
        length = len(self.__data)
        maxScore = max(self.__scores)
        if self.Stuck(maxScore):
            for dna in self.__data:
                if(dna.GetScore() == maxScore):
                    mutation = 1
                else:
                    mutation = 0.5
                dna.Mutate(mutation, self.__hints)
            
            print ('Forced mutations was did...')
            randNumbers = [np.random.random() for i in range(len(self.__encoded))]
            randSum = sum(randNumbers)
            length = len(self.__encoded)
            for i in range(length):
                self.__weights[i] = randNumbers[i]/randSum*length
            return None
    
        cumulativeSums = np.array(self.__scores).cumsum().tolist()
        maxSum = cumulativeSums[-1]
        newGeneration = []
        currentMutation = self.__mutationRate# + (self.__generation/1000)
        print ('mutation:', currentMutation*100, '%')
        for i in range(length):
            parent1 = self.__data[self.__PickOne(cumulativeSums, maxSum)]
            parent2 = self.__data[self.__PickOne(cumulativeSums, maxSum)]
            child = parent1.CrossOver(parent2, currentMutation, self.__hints)
            newGeneration.append(child)

        self.__data = newGeneration


