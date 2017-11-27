from  math import  floor
from argparse import Namespace
import json
import numpy as np
VOWELS =  'aeiou'
class DNA:
    def __init__(self, data):
        self.__data = data[:]
        self.__score = 0

    @classmethod
    def Random(cls, length, hints):
        data = []
        values = [x for x in range(length) if x not in hints.values()]
        values = np.random.permutation(values).tolist()
        for i in range(length):
            if i not in hints:
                data.append(values.pop(0))
            else:
                data.append(hints[i])
        return cls(data)

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
        return DNA(param.__data)

    def __str__(self):
        return ' '.join(str(x) for x in self.__data)

    def CrossOver(self, other, mutationRate, hints):
        n = len(self.__data)
        #data = np.random.permutation(range(n)).tolist()
        ''''
        if other.GetScore() > self.__score:
            for i in range(n):
                data[i] = other.__data[i]
        else:
            for i in range(n):
                data[i] = self.__data[i]

        '''
        data = self.__data[:]
        if (self.__score + other.GetScore()) > 0:
            fromFirst = self.__score/ (self.__score + other.GetScore())
        else:
            fromFirst = 0.5
        fromFirst = 0.5
        visited = [False] * n
        pos = {}
        for i in range(n):
            if data[i] in pos:
                print('Not permutation !! : ', data[i])
                print(data)
                exit(-1)
            else:
                pos[data[i]] = i
        perm = np.random.permutation(range(n))
        elements = n*(1-fromFirst)
        cycles = []
        for i in perm:
            if (visited[i] == False):
                j = i
                cycle = []
                while True:
                    visited[j] = True
                    cycle.append(j)
                    j = pos[other.__data[j]]
                    if i == j:
                        break
                    if (elements > n):
                        print('Infinite loop')
                        exit(-1)
                if len(cycle) > 1:
                    cycles.append(cycle)
        cycles.sort(key = lambda s: len(s))
        for cycle in cycles:
            for i in cycle:
                data[i] = other.__data[i]
            elements -= len(cycle)
            if elements <= 0:
                break
        child = DNA(data)
        child.Mutate(mutationRate, hints)
        return child
    
    def Mutate(self, mutationRate, hints):
        n = len(self.__data)
        for i in range(n):
            if (np.random.rand() < mutationRate and (i not in hints)):
                while True:
                    j = floor(np.random.rand() * n)
                    if j not in hints:
                        break
                self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

    def decode(self, encoded):
        decoded = []
        for word in encoded:
            newWord = ''
            for value in word:
                newWord = newWord + chr(self.__data[ord(value) - ord('a')] + ord('a'))
            decoded.append(newWord)
        return decoded

    def GetScore(self):
        return self.__score

    def CalcFitness(self, encoded, totalLength, cost, wordsDict, bad, weights):
        score = 0
        totalLength = sum(len(word) for word in encoded)
        for i, word in enumerate(self.decode(encoded)):
            exist = False
            for vowel in VOWELS:
                if vowel in word:
                    exist = True
                    break
            if exist == True:
                if word in wordsDict:
                    score += (wordsDict[word]/len(word))*(len(word)/totalLength)*weights[i]*100
                else:
                    score -= bad*(len(word)/totalLength)*weights[i]*100
            else:
                score = 0
                break
        self.__score = pow(max(0, score), 1)

