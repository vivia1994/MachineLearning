from numpy import *


def loadDataSet():
    postingList = [['I', 'got', 'free', 'two', 'movie', 'ticket', 'from', 'your', 'boy', 'friend'],
                   ['free', 'coupon', 'from', 'xx.com'],
                   ['watch', 'free', 'new', 'movie', 'from', 'freemovie.com'],
                   ['best', 'deal', 'promo', 'code', 'here'],
                   ['there', 'will', 'be', 'free', 'pizza', 'during', 'the', 'meeting'],
                   ['scheduled', 'meeting', 'tomorrow'],
                   ['can', 'we', 'have', 'lunch', 'today'],
                   ['I', 'miss', 'you'],
                   ['thanks', 'my', 'friend'],
                   ['it', 'was', 'good', 'to', 'see', 'you', 'today'],
                   ['free', 'coupon', 'last', 'deal'],
                   ['free', 'massage', 'coupon'],
                   ['I', 'sent', 'the', 'coupon', 'you', 'asked', 'it', 'is', 'not', 'free'],
                   ['coupon', 'promo', 'code', 'here']]
    classVec = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1]  # 1 is spam, 0 not
    return postingList, classVec


def createVocabList(dataSet):   #创建词汇表
    vocabSet = set([])  # create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # union of the two sets创建并集
    print("vocabSet：",vocabSet)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):    #根据词汇表，将句子转化为向量
    returnVec = [0] * len(vocabList)
    print("returnVec_origin: ",returnVec)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    print("returnVec_result: ", returnVec)
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    print("trainMatrix:", trainMatrix)
    print("trainCategory:",trainCategory)
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pSpam = sum(trainCategory) / float(numTrainDocs)
    print("numTrainDocs:",numTrainDocs,numWords,sum(trainCategory),pSpam,trainMatrix[0])
    p0Num = ones(numWords);#计算频数初始化为1
    p1Num = ones(numWords)
    print("p0Num:",p0Num)
    p0Denom = 2.0;  #即拉普拉斯平滑
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)
    #print("p1Vect:",p1Vect)
    #print("p0Vect:",p0Vect)
    return p0Vect, p1Vect, pSpam#返回各类对应特征的条件概率向量
                                 #和各类的先验概率


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)  # element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    # print(str(trainMat))
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(listClasses))

    testEntry = ['I', 'pizza', 'coupon']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    if classifyNB(thisDoc, p0V, p1V, pSpam) == 1:
        print(testEntry, 'classified this is a spam')
    else:
        print(testEntry, 'classified this is not a spam')

    testEntry = ['I', 'will', 'miss', 'free', 'pizza']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    if classifyNB(thisDoc, p0V, p1V, pSpam) == 1:
        print(testEntry, 'classified this is a spam')
    else:
        print(testEntry, 'classified this is not a spam')


def textParse(bigString):  # input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]


def spamTest():
    docList = [];
    classList = [];
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)  # create vocabulary
    trainingSet = range(50);
    testSet = []  # create test set
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = [];
    trainClasses = []
    for docIndex in trainingSet:  # train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:  # classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
            print("classification error", docList[docIndex])
    print('the error rate is: ', float(errorCount) / len(testSet))
    # return vocabList,fullText


def calcMostFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]


def localWords(feed1, feed0):
    import feedparser
    docList = [];
    classList = [];
    fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)  # NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)  # create vocabulary
    top30Words = calcMostFreq(vocabList, fullText)  # remove top 30 words
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2 * minLen);
    testSet = []  # create test set
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = [];
    trainClasses = []
    for docIndex in trainingSet:  # train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:  # classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1

    print('the error rate is: ', float(errorCount) / len(testSet))
    return vocabList, p0V, p1V


def getTopWords(ny, sf):
    import operator
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = [];
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0: topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0: topNY.append((vocabList[i], p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**")
    for item in sortedSF:
        print(item[0])
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)

testingNB()