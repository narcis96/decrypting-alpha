import os, progressbar, threading, random
import numpy as np
import statistics as stats
from DNA import DNA
BAR_LENGTH = 5

def worker(data, encoded, cost, wordsDict):
    for dna in data:
        dna.CalcFitnessOld(encoded, cost, wordsDict)

class Population:
    def __init__(self, data, mutationRate, encoded, cost, wordsDict, hints):
        self.__data = data
        self.__matingPool = []
        self.__generation = 0
        self.__bestScore = 0
        self.__mutationRate = mutationRate
        self.__encoded = encoded
        self.__cost = cost
        self.__wordsDict = wordsDict
        self.__hints = hints

    @classmethod
    def Random(cls, count, length, mutationRate, encoded, cost, wordsDict, hints):
        data = [DNA.Random(length, hints) for i in range(count)]
        return cls(data, mutationRate, encoded, cost, wordsDict, hints)

    @classmethod
    def FromFolder(cls, path, count, length, mutationRate, encoded, cost, wordsDict, hints):
        data = []
        for file in os.listdir(path):
           if file.endswith('.json'):
               data.append(DNA.ReadFromJson(path + file))
        print('Loaded ', len(data), 'samples')
        if len(data) < count:
            count = count - len(data)
            print ('Adding ', count, 'random samples...')
            data = data + [DNA.Random(length, hints) for i in range(count)]
        return cls(data,  mutationRate, encoded, cost, wordsDict, hints)

    def Print(self, printAll):
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
            for i,dna in enumerate(self.__data):
                dna.WriteJson('./generation/best/' + str(i) + '.json')
        else:
            x = 1
            #print('Stopped!! Start again...')
            #os.system('python3 main.py') #hack
            #exit(0)
        for dna  in self.__data:
            if dna.GetScore() == maxScore:
                decoded = dna.decode(self.__encoded)
                print('best match: ',decoded)
                if printAll:
                    print(decoded, file=open(saveFolder + '/best.txt', 'w'))
                break
    
        print('generation: ', self.__generation, ' average score : ', average, ' max score: ', max(self.__scores))

    def CalcFitness(self, threadsCount):
        length = len(self.__data)
        threads = []
        for threadId in range(threadsCount):
            data = [self.__data[i] for i in range(length) if i % threadsCount == threadId]
            thread = threading.Thread(target=worker, args = (data, self.__encoded, self.__cost, self.__wordsDict, ))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        #bar = progressbar.ProgressBar(maxval=length)
        #show = [randint(0, BAR_LENGTH) for i in range(length)]
        #if show[indx] == 0:
        #   bar.update(indx + 1)
        #bar.finish()
        self.__scores = [dna.GetScore() for dna in self.__data]

    def __PickOne(self, mySum, length):
        index = 0
        value = np.random.rand() * mySum
        while True:
            value -= self.__scores[index]
            if value <= 0:
                return  index
            index += 1

    def NaturalSelection(self):
        length = len(self.__data)
        mySum = sum(self.__scores)
        newGeneration = []
        for i in range(length):
            parent1 = self.__data[self.__PickOne(mySum, length)]
            parent2 = self.__data[self.__PickOne(mySum, length)]
            child = parent1.CrossOver(parent2, self.__mutationRate, self.__hints)
            newGeneration.append(child)
        self.__data =  newGeneration

