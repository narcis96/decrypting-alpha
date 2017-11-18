import os
from math import floor
import statistics as stats
from random import sample, random, randint
from DNA import DNA

class Population:
    def __init__(self, data, count, length, mutationRate, encoded, words):
        self.__data = data
        self.__matingPool = []

    @classmethod
    def Random(cls, count, length, mutationRate, encoded, words):
        data = [DNA.Random(length, mutationRate, encoded, words) for i in range(count)]
        return cls(data, count, length, mutationRate, encoded, words)

    @classmethod
    def FromFile(cls, path ,count, length, mutationRate, encoded, words):
        data = []
        data = [DNA.FromFile(path + '/' + str(i) + '.txt',length, mutationRate, encoded, words) for i in range(count)]
        return cls(data, count, length, mutationRate, encoded, words)

    def Print(self, generation):
        saveFolder = './generation/' + str(generation)
        os.makedirs(saveFolder, exist_ok = True)

        #scoresFile = open(saveFolder + '/scores.txt', 'w')
        #for i,dna in enumerate(self.__data):
        #    print(i, dna.GetScore(), file = scoresFile)

        for i,dna in enumerate(self.__data):
            dna.Print(saveFolder + '/' + str(i) + '.txt')

        average = stats.mean([dna.GetScore() for dna in self.__data])

        print(average, file = open(saveFolder + '/average.txt', 'w'))
        print('generation ', str(generation), ':average score = ', average)

    def CalcFitness(self):
        for dna in self.__data:
            dna.CalcFitness()

    def MatingPool(self):
        maxScore = max(dna.GetScore() for dna in self.__data)
        self.__matingPool = []
        for i, dna in enumerate(self.__data):
            score = dna.GetScore()/maxScore
            n = floor(score) * 100
            for j in range(n):
                self.__matingPool.append(dna)

    def NaturalSelection(self):
        length = len(self.__data)
        self.__data = []
        for i in range(length):
            index1 = floor(random() * len(self.__matingPool))
            index2 = floor(random() * len(self.__matingPool))
            parent1 = self.__matingPool[index1]
            parent2 = self.__matingPool[index2]
            child = parent1.CrossOver(0.5, parent2)
            self.__data.append(child)


