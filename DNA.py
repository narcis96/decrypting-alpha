from random import sample, random, randint
from math import floor
from argparse import Namespace
import json
class DNA:

    def __init__(self, data, separators):
        self.__data = data
        self.__score = 0
        self.__sep = separators
    
    @classmethod
    def Random(cls, length):
        separators = []
        return cls(sample(range(length), length), separators)

    def __ToJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)

    def WriteJson(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.__ToJson(), outfile)
    
    @staticmethod
    def json2obj(data):
        return json.loads(data, object_hook=lambda d: Namespace(**d))

    @staticmethod
    def ReadFromJson(path):
        with open(path) as data_file:
            param = DNA.json2obj(json.load(data_file))
        return DNA(param.__data, param.__sep)

    def __str__(self):
        return ' '.join(str(x) for x in self.__data)

    def CrossOver(self, other, mutationRate):
        data = self.__data
        if (self.__score + other.GetScore()) > 0:
            fromFirst = self.__score/ (self.__score + other.GetScore())
        else:
            fromFirst = 0.5
        n = len(data)
        pos = {}
        visited = [False] * n 
        for i in range(n):
            pos[data[i]] = i
        elements = 0
        for i in range(n):
            if (random() > fromFirst and visited[i] == False):
                j = i
                while True:
                    data[j] = other.__data[j]
                    j = pos[data[j]]
                    visited[j] = True
                    elements = elements + 1
                    if i == j:
                        break
                if elements > n * (1-fromFirst):
                    break
        for i in range(n):
            if random() < mutationRate:
                j = floor(random() * len(data))
                data[i], data[j] = data[j], data[i]
        separators = []
        return DNA(data, separators)

    def decode(self, encoded):
        decoded = ''
        for value in encoded:
            decoded = decoded + chr(self.__data[ord(value) - ord('a')] + ord('a'))
        return decoded

    def GetScore(self):
        return self.__score

    def CalcFitness(self, encoded, words):
        decoded = self.decode(encoded)
        score = 0
        for word in words:
            if word in decoded:
                score += len(word)
        self.__score = pow(score, 1)
