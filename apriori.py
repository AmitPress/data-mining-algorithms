from itertools import combinations
with open('chess.dat', 'r') as f:
    raw_text=f.read()

lines = raw_text.split('\n')

database = [list(map(int, line.strip().split(' '))) for line in lines]


total_items = set()

for trxn in database:
    total_items = total_items.union(trxn)

# print(total_items)

item_support = dict()

for item in total_items:
    cnt = 0
    for trxn in database:
        if item in trxn:
            cnt += 1
    item_support[item]=cnt

# apriori
MINIMUM_SUPPORT_THRESHOLD = 500

sorted_list = dict(sorted(item_support.items()))
c1 = sorted_list

l1 = dict()

for k,v in c1.items():
    if v>=MINIMUM_SUPPORT_THRESHOLD:
        l1[k]=v



c2 = list(combinations(l1.keys(), 2))
item_support = dict()
for item in c2:
    cnt = 0
    for trxn in database:
        if set(item).issubset(trxn):
            cnt += 1
    item_support[item]=cnt

l2 = dict()

for k,v in item_support.items():
    if v>=MINIMUM_SUPPORT_THRESHOLD:
        l2[k]=v

temp = []
keys = list(l2.keys())
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        if keys[i][0] == keys[j][0]:
            temp.append((keys[i][0], keys[i][1], keys[j][1]))

temp2 = []
for t in temp:
    cs = list(combinations(t, 2))
    cnt = 0
    for c in cs:
        if c in l2.keys():
            cnt += 1
    if cnt == 3:
        temp2.append(t)

c3 = temp2


item_support = dict()
for item in c3:
    cnt = 0
    for trxn in database:
        if set(item).issubset(trxn):
            cnt += 1
    item_support[item]=cnt

l3 = dict()
for k,v in item_support.items():
    if v>=MINIMUM_SUPPORT_THRESHOLD:
        l3[k]=v

print(l3)