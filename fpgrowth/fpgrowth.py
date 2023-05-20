import time
from collections import defaultdict
from csv import reader
from itertools import chain, combinations

class Node:
    def __init__(self, itemName, frequency, parentNode):
        self.itemName = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, frequency):
        self.count += frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind+1)

def getFromFile(fname):
    itemSetList = []
    frequency = []
    
    with open(fname, 'r') as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None, line))
            itemSetList.append(line)
            frequency.append(1)

    return itemSetList, frequency

def constructTree(itemSetList, frequency, minSup):
    headerTable = defaultdict(int)
    for idx, itemSet in enumerate(itemSetList):
        for item in itemSet:
            headerTable[item] += frequency[idx]

    headerTable = dict((item, sup) for item, sup in headerTable.items() if sup >= minSup)
    if(len(headerTable) == 0):
        return None, None

    for item in headerTable:
        headerTable[item] = [headerTable[item], None]

    fpTree = Node('Null', 1, None)
    for idx, itemSet in enumerate(itemSetList):
        itemSet = [item for item in itemSet if item in headerTable]
        itemSet.sort(key=lambda item: headerTable[item][0], reverse=True)
        currentNode = fpTree
        for item in itemSet:
            currentNode = updateTree(item, currentNode, headerTable, frequency[idx])

    return fpTree, headerTable

def updateHeaderTable(item, targetNode, headerTable):
    if(headerTable[item][1] == None):
        headerTable[item][1] = targetNode
    else:
        currentNode = headerTable[item][1]
        while currentNode.next != None:
            currentNode = currentNode.next
        currentNode.next = targetNode

def updateTree(item, treeNode, headerTable, frequency):
    if item in treeNode.children:
        treeNode.children[item].increment(frequency)
    else:
        newItemNode = Node(item, frequency, treeNode)
        treeNode.children[item] = newItemNode
        updateHeaderTable(item, newItemNode, headerTable)

    return treeNode.children[item]

def ascendFPtree(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.itemName)
        ascendFPtree(node.parent, prefixPath)

def findPrefixPath(basePat, headerTable):
    treeNode = headerTable[basePat][1]
    condPats = []
    frequency = []
    while treeNode != None:
        prefixPath = []
        ascendFPtree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats.append(prefixPath[1:])
            frequency.append(treeNode.count)
        treeNode = treeNode.next

    return condPats, frequency

def mineTree(headerTable, minSup, preFix, freqItemList):
    sortedItemList = [item[0] for item in sorted(headerTable.items(), key=lambda p: p[1][0])]
    for item in sortedItemList:
        newFreqSet = preFix.copy()
        newFreqSet.add(item)
        freqItemList.append(newFreqSet)
        condPattBases, frequency = findPrefixPath(item, headerTable)
        conditionalTree, newHeaderTable = constructTree(condPattBases, frequency, minSup)
        if newHeaderTable != None:
            mineTree(newHeaderTable, minSup, newFreqSet, freqItemList)

def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count

def associationRule(freqItemSet, itemSetList, minConf):
    rules = []
    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        itemSetSup = getSupport(itemSet, itemSetList)
        for s in subsets:
            confidence = itemSetSup / getSupport(s, itemSetList)
            if confidence >= minConf:
                rules.append((s, tuple(set(itemSet) - set(s)), confidence))
    return rules

def getFrequencyFromList(itemSetList):
    frequency = defaultdict(int)
    for itemSet in itemSetList:
        for item in itemSet:
            frequency[item] += 1
    return dict(frequency)

def fpgrowth(itemSetList, minSupRatio, minConf):
    frequency = getFrequencyFromList(itemSetList)
    minSup = len(itemSetList) * minSup

def fpgrowthFromFile(fname, minSupRatio, minConf):
    itemSetList, frequency = getFromFile(fname)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        rules = associationRule(freqItems, itemSetList, minConf)
        return freqItems, rules

if __name__ == "__main__":
    inputFile = "inputfile.text"
    minSup = 0.9
    minConf = 0.9

    start_time = time.time()
    try:
        freqItemSet, rules = fpgrowthFromFile(inputFile, minSup, minConf)
    except:
        print("Execution Stopped...")
        exit(1)
    end_time = time.time()
    print("Time Elapsed: ", end_time-start_time)
    print()
    print("Frequent Item Sets:")
    for itemSet in freqItemSet:
        print(", ".join(itemSet))
    print("\n\n\n\n\n")
    # Print rules
    print("Association Rules:")
    for rule in rules:
        antecedent = ", ".join(rule[0])
        consequent = ", ".join(rule[1])
        confidence = rule[2]
        print(f"{{{antecedent}}} -> {{{consequent}}}: {confidence}")
