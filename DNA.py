from random import sample, random, randint
from math import floor

class DNA:

    def __init__(self, data, mutationRate, encoded, words):
        self.__data = data
        self.__mutationRate = mutationRate
        self.__score = 0
        self.__encoded = encoded
        self.__words = words

    @classmethod
    def Random(cls, length, mutationRate, encoded, words):
        return cls(sample(range(length), length), mutationRate, encoded, words)

    @classmethod
    def FromFile(cls, path, length, mutationRate, encoded, words):
        with open(path) as file:
            data = [int(x) for x in file.read().split()]  # read first line
        return cls(data, mutationRate, encoded, words)

    def __str__(self):
        return ' '.join(str(x) for x in self.__data)

    def Print(self, path):
        file = open(path, 'w')
        file.write(str(self))
        file.close()

    def CrossOver(self, other):
        data = self.__data
        if (self.__score + other.GetScore()) > 0:
            fromFirst = self.__score/ (self.__score + other.GetScore())
        else:
            fromFirst = 1/2
#        if random() > fromFirst:
        for i,value in enumerate(self.__data):
            if random() > fromFirst:
                data[i] = other.__data[i]
        if random() < self.__mutationRate:
            i = floor(random() * len(data))
            j = floor(random() * len(data))
            data[i], data[j] = data[j], data[i]

        return DNA(data, self.__mutationRate, self.__encoded, self.__words)

    def decode(self):
        decoded = ''
        for value in self.__encoded:
            decoded = decoded + chr(self.__data[ord(value) - ord('a')] + ord('a'))
        return decoded

    def GetScore(self):
        return self.__score

    def CalcFitness(self):
        decoded = self.decode()
        score = 0
        for word in self.__words:
            if word in decoded:
                score += pow(len(word), 3)
        self.__score = pow(score, 2)
