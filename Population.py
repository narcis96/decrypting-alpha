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
        maxScore = max(dna.GetScore() for dna in self.__data)

        print(average, file = open(saveFolder + '/average.txt', 'w'))
        print('generation ', str(generation), ':average score = ', average)

        for dna  in self.__data:
            if dna.GetScore() == maxScore:
                print(dna.decode())
                print(dna.decode(), file=open(saveFolder + '/best.txt', 'w'))
                break

    def CalcFitness(self):
        for dna in self.__data:
            dna.CalcFitness()
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
            child = parent1.CrossOver(parent2)
            newGeneration.append(child)
        self.__data =  newGeneration

