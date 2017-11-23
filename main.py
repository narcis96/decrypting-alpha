from DNA import DNA
import os, re, time
import json, time
import numpy as np
#import plotly.plotly as py
#import plotly.graph_objs as go
#from datetime import datetime
#import pandas_datareader.data as web
from collections import Counter
from Population import Population
from  math import log2
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

if __name__ == '__main__':
    with open('./param.json') as data_file:
        params = json.load(data_file)
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
        encoded = file.readline()[:-1]

    milliseconds = int(round(time.time()))
    np.random.seed(milliseconds)
    count = params['population']
    length = params['length']
    mutation = params['mutation']

    words = mostused + smallList + bigList
    words = [word for word in words if len(word) >= 3]
    wordsDict = Counter(words)
    cost = {}
    newDict = {}
    for word in wordsDict:
        cost[word] = log2(wordsDict[word] + 1)
        wordsDict[word] = len(word)
        for i in range(len(word)):
            newDict[word[0:i+1]] = 1
    for word in wordsDict:
        newDict[word] = 2

    for key in hints:
        print(chr(key+ord('a')), chr(hints[key]+ord('a')))
    print('encoded text :',encoded)
    print(len(words), 'words')
    print('population: ', count)
    print('length: ', length)
    print('mutation: ', mutation*100, '%')

    decoded = 'afaraningelinistit'
    score = 0
    length = len(decoded)
    substrings = [decoded[i: j + 1] for i in range(length - 1) for j in range(i + 1, min(i + 8,length))]
    for substring in substrings:
        if substring in wordsDict:
            score += wordsDict[substring] * cost[substring]

    print('score to rich :',score)
    print(wordsDict['afara'],cost['afara'])
    print(wordsDict['ninge'], cost['ninge'])
    print(wordsDict['linistit'],cost['linistit'])

    '''
    wordsDict = newDict
    #print(max([val] for i,val in words))
    #decoded = 'ucujuoaoidbaoaesas'

    length = len(decoded)
    score = 0
    word = ''
    for i in range(length):
        word = word + decoded[i]
        print(word)
        if word in wordsDict:
            if wordsDict[word] == 2:
                score = i
                word = ''
        else:
            if wordsDict[word[:-1]] != 2:
                break
            word = decoded[i]
        
    print('score:',score)
    print(wordsDict['narcis'])
    exit(0)
    '''

    if params['random'] == True:
        print('Generate ', count, ' random samples')
        population = Population.Random(count, length, mutation, encoded, cost, wordsDict, hints)
    else:
        print ('continue with folder ', params['continue'])
        population = Population.FromFolder(params['continue'], count, length, mutation, encoded, cost, wordsDict, hints)
    
    while True:
        scores = population.CalcFitness(params['threads'])
        population.Print(params['print'])
        population.NaturalSelection()
