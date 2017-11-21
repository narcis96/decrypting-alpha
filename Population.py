import os
from math import floor
import statistics as stats
from random import sample, random, randint
from DNA import DNA

class Population:
    def __init__(self, data, mutationRate, encoded, words):
        self.__data = data
        self.__matingPool = []
        self.__generation = 0
        self.__bestScore = 0
        self.__mutationRate = mutationRate
        self.__encoded = encoded
        self.__words = words

    @classmethod
    def Random(cls, count, length, mutationRate, encoded, words):
        data = [DNA.Random(length) for i in range(count)]
        return cls(data, mutationRate, encoded, words)

    @classmethod
    def FromFolder(cls, path ,count, length, mutationRate, encoded, words):
        data = []
        for file in os.listdir(path):
           if file.endswith('.json'):
               data.append(DNA.ReadFromJson(path + file))
        return cls(data,  mutationRate, encoded, words)

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
                dna.WriteJson(saveFolder + '/' + str(i) + '.txt')
            print(average, file = open(saveFolder + '/average.txt', 'w'))

        if average > self.__bestScore:
            self.__bestScore = average
            for i,dna in enumerate(self.__data):
                dna.WriteJson('./generation/best/' + str(i) + '.json')

        for dna  in self.__data:
            if dna.GetScore() == maxScore:
                decoded = dna.decode(self.__encoded)
                print(decoded)
                if printAll:
                    print(decoded, file=open(saveFolder + '/best.txt', 'w'))
                break
    
        print('generation: ', self.__generation, ' average score : ', average)

    def CalcFitness(self):
        for dna in self.__data:
            dna.CalcFitness(self.__encoded, self.__words)
        self.__scores = [dna.GetScore() for dna in self.__data]

    def __PickOne(self, mySum, length):
        index = 0
        value = random()*mySum
        while True:
            value -= self.__scores[index]
            if value <= 0:
                return  index
            index += 1

    def NaturalSelection(self):
        length = len(self.__data)
        mySum = sum(self.__scores)
        maxScore = max(self.__scores)
        newGeneration = []
        for i in range(length):
            parent1 = self.__data[self.__PickOne(mySum, length)]
            parent2 = self.__data[self.__PickOne(mySum, length)]
            child = parent1.CrossOver(parent2, self.__mutationRate)
            newGeneration.append(child)
        self.__data =  newGeneration

