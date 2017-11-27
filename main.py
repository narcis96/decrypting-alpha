from DNA import DNA
import os, re, time, progressbar, json, itertools, random, threading
import numpy as np
#import plotly.plotly as py
#import plotly.graph_objs as go
#from datetime import datetime
#import pandas_datareader.data as web
from collections import Counter
from Population import Population
from  math import log2
ALPHA = 'abcdefghijklmnopqstuvwxyz'
from thread import ThreadPool
def UniqueWords(fromFile, toFile):
    with open(fromFile, 'r') as f:
        listWords = [line[:-1] for line in f]
    myFile = open(toFile, 'w')
    for word in list(set(listWords)):
        print(word,file = myFile)

def ParseFile(path):
    total = []
    with open(path, 'r', encoding = 'utf-8', errors='ignore') as content_file:
        sentences = re.split(r'[!?.]+',content_file.read())
        total = total + [''.join(list(filter(lambda x: str.isalpha(x) or x == ' ', str.lower(sentence)))) for sentence in sentences]
    return total

def SaveSenteses(path, toFile):
    total = []
    for file in os.listdir(path):
        if file.endswith('.r'):
            total = total + ParseFile(path + "/" + file)
    myFile = open(toFile, 'w')
    for sentence in total:
        print(sentence, file = myFile)
    
def decode(encode, path):
    with open(path) as file:
        data = [int(x) for x in file.read().split()]  # read first line
    decoded = ''
    for value in encoded:
        decoded = decoded + chr(data[ord(value)- ord('a')] + ord('a'))
    return  decoded

def ReadFile(file):
    with open(file, 'r') as f:
        lines = [line[:-1] for line in f]
    return lines

def GetWords(sentences):
    words = []
    for sentence in sentences:
        for word in sentence.split():
            words.append(word)
    return words

def SaveUniqueWords(sentences, toFile):
    words = set(GetWords(sentences))
    myFile = open(toFile, 'w')
    for word in words:
        print(word, file = myFile)

def GetHints(file):
    hints = {}
    with open(file, 'r') as f:
        for line in f:
            li = line.split()
            hints[ord(li[0]) - ord('a')] = ord(li[1]) - ord('a')
    return hints
def CreateDict(words, encoded):
    lengths = [len(word) for word in encoded]
    wordsDict = Counter(words)
    newDict, newCost, cost = {}, {}, {}
    print('Creating dict...')
    bar = progressbar.ProgressBar(maxval=len(wordsDict))
    #                for new in list(itertools.combinations([alpha for alpha in ALPHA if alpha not in word], k))[0:100]:
    for indx,word in enumerate(wordsDict):
        wordLen, wordCost = len(word), log2(len(word))
#        if wordLen not in lengths:
#            continue
        cost[word] = wordCost
        wordsDict[word] = wordLen
        for k in range(1, 4):
            for old in list(itertools.combinations(set(word), k)):
                permutedAlpha = [alpha for alpha in ALPHA if alpha not in word]
                to = list(itertools.combinations([alpha for alpha in ALPHA if alpha not in word], k))
                for new in to:
                    for j in range(k):
                        newWord = word.replace(old[j], new[j])
                        currentCost = 0
                        for i in range(wordLen):
                            x = abs(ord(newWord[i])  - ord(word[i]) + 1)
                            x = (26 - x) / 26
                            currentCost = currentCost + pow(x, 2)
                        if newWord not in newDict:
                            newDict[newWord] = currentCost
                            newCost[newWord] = wordCost
                        else:
                            newDict[newWord] = min(newDict[newWord], currentCost)
                            newCost[newWord] = min(newCost[newWord], wordCost)

        bar.update(indx + 1)
    bar.finish()
    for word in newDict:
        if word not in wordsDict:
            wordsDict[word] = newDict[word]
            cost[word] = newCost[word]
    print('dict created...')

    return wordsDict, cost

def work(x, y):
    print (x, y)
if __name__ == '__main__':
    th = ThreadPool(4)
    th.Start(work,[(1, 2),(3,4),(5,6),(7,8),(9,10),(5,6),(7,8),(9,10)])
    th.Join()
    th.Start(lambda x, y: print(x,y),[(1, 2),(3,4),(5,6),(7,8),(9,10),(5,6),(7,8),(9,10)])
    th.Join()

    #exit(0)
    with open('./param.json') as data_file:
        params = json.load(data_file)
    with open('wordsDict-most-used.json') as data_file:
        wordsDict = json.load(data_file)
    with open('wordsCost-most-used.json') as data_file:
        cost = json.load(data_file)
    #UniqueWords('./data/words-list.txt','./data/words-list-unique.txt')
    #SaveSenteses('./data/Newspapers', './data/sentences.txt')
    #SaveUniqueWords(sentences, './data/words-from-sentences-unique.txt')
    #SaveUniqueWords(total, './data/most-used.txt')
    mostused = ReadFile(params['most-1000']) + ReadFile(params['most-3000'])
    sentences = ReadFile('./data/sentences.txt')
    smallList = ReadFile(params['sentences-word-list'])
    bigList = ReadFile(params['word-list'])
    hints = GetHints(params['hints'])
    with open(params['encoded-file'], 'r') as file:
        encoded = (file.readline()[:-1]).split() 

    milliseconds = int(round(time.time()))
    np.random.seed(milliseconds)
    count, length, mutation = params['population'], params['length'], params['mutation']
    words = mostused# + smallList# + bigList
    words = [x for x in words if 'y' not in x and 'k' not in x]
    words = [word for word in words if len(word) >= 2 ]#and len(word) <= max(len(word) for word in encoded)]

    if params['create-dict']:
        wordsDict, cost = CreateDict(words, encoded)
    with open('wordsDict-most-used.json', 'w') as outfile:
        json.dump(wordsDict, outfile)
    with open('wordsCost-most-used.json', 'w') as outfile:
        json.dump(cost, outfile)
    #exit(0)


    for key in hints:
        print(chr(key+ord('a')), chr(hints[key]+ord('a')))
    print('encoded text :',encoded)
    print(len(words), 'words')
    print('len(dict):', len(wordsDict))
    print('population: ', count)
    print('length: ', length)
    print('mutation: ', mutation*100, '%')
    #print(wordsDict['finiwdid'])

    #exit(0)

#    decoded = ['afara', 'ninge', 'linistit']
    '''
    decoded = ['romanii', 'au', 'fost', 'simpli']
    score = 0
    for word in decoded:
        score += wordsDict[word] / len(word)
    score = pow(score, 2)
    print('score to rich :',score)
    for word in decoded:
        print(wordsDict[word], cost[word])
'''
    if params['random'] == True:
        print('Generate ', count, ' random samples')
        population = Population.Random(params['threads'], count, length, mutation, encoded, cost, wordsDict, hints)
    else:
        print ('continue with folder ', params['continue'])
        population = Population.FromFolder(params['threads'], params['continue'], count, length, mutation, encoded, cost, wordsDict, hints)
    
    while True:
        scores = population.CalcFitness()
        population.Print(params['print'], params['save-best'])
        population.NaturalSelection()
