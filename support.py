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

print(item_support) # absolute support