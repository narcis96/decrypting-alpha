from DNA import DNA
import os, re, sys
import json
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

    words = mostused + smallList
    freq = Counter(words)
    

    words = list(set(words))
    words = [word for word in words if len(word) >= 2]
    scores = [log2(freq[word]+1) for word in words]
    words = list(zip(words, scores))

    #print(max([val] for i,val in words))
    print(len(words))

    hints = GetHints(params['hints'])
    for key in hints:
        print(chr(key+ord('a')), chr(hints[key]+ord('a')))

    with open(params['encoded-file'], 'r') as file:
        encoded = file.read()[:-1]
    print(encoded)

    #exit(0)

    mutation = params['mutation']
    if params['random'] == True:
        count = params['population']
        length = params['length']
        print('population: ', count)
        print('length: ', length)
        print('mutation: ', mutation)
        population = Population.Random(count, length, mutation, encoded, words, hints)
    else:
        print ('continue with folder ', params['continue'])
        population = Population.FromFolder(params['continue'], mutation, encoded, words, hints)
    
    while True:
        scores = population.CalcFitness(params['threads'])
        population.Print(params['print'])
        population.NaturalSelection()
