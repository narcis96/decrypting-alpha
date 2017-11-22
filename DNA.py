import random
from datetime import datetime
from argparse import Namespace
import json
local_random = random.Random()
local_random.seed(datetime.now())
class DNA:
    def __init__(self, data, separators):
        self.__data = data
        self.__score = 0
        self.__sep = separators

    @classmethod
    def Random(cls, length, hints):
        separators = []
        data = []
        values = [x for x in range(length) if x not in hints.values()]
        values = local_random.sample(values,len(values))
        for i in range(length):
            if i not in hints:
                data.append(values.pop(0))
            else:
                data.append(hints[i])
        return cls(data, separators)

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

    def CrossOver(self, other, mutationRate, hints):
        data = self.__data

        if (self.__score + other.GetScore()) > 0:
            fromFirst = self.__score/ (self.__score + other.GetScore())
        else:
            fromFirst = 0.5

        n = len(data)
        visited = [False] * n
        pos = {}
        for i in range(n):
            if data[i] in pos:
                print('Not permutation !! : ', data[i])
                print(data)
                exit(-1)
            else:
                pos[data[i]] = i

        elements = 0
        for i in range(n):
            if (local_random.random() > fromFirst and visited[i] == False):
                j = i
                cycle = [j]
                while True:
                    visited[j] = True
                    data[j] = other.__data[j]
                    j = pos[data[j]]
                    elements = elements + 1
                    cycle.append(j)
                    if i == j:
                        break
                    if (elements > n):
                        print('Infinite loop')
                        exit(0)

                if elements > n * (1-fromFirst):
                    break

        for i in range(n):
            if (local_random.random() < mutationRate and (i not in hints)):
                while True:
                    j = local_random.randint(0, n - 1)
                    if j not in hints:
                        break
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
        for word, coef in words:
            wordLen = len(word)
            if word in decoded:
                maxScore = len(word)
            else:
                #length = len(decoded)
                maxScore = 0
                #substrings = [decoded[i:i + wordLen] for i in range(length - wordLen + 1)]
                #maxScore = max(len([i for i, j in zip(substring, decoded) if i == j]) for substring in substrings)
            if maxScore > wordLen/2:
                score += maxScore * coef
        self.__score = pow(score, 2)
