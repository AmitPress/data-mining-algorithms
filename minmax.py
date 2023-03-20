with open('values.txt', 'r') as f:
  inp = list(map(int, f.read().split('\n')))

inp = sorted(inp)

# size = 3
# n_buckets = len(inp)//size
# bucket = [[0 for _ in range(size)] for _ in range(n_buckets)]

# inp = iter(inp)
# for i in range(n_buckets):
#     for j in range(size):
#       bucket[i][j] = next(inp)
# print(bucket)

# for i in range(n_buckets):
#     first = bucket[i][0]
#     last = bucket[i][size-1]
#     for j in range(1, size-1):
#       if abs(bucket[i][j]-first)<abs(bucket[i][j]-last):
#         bucket[i][j] = first
#       else:
#         bucket[i][j] = last

data = inp
minimum = min(inp)
maximum = max(inp)
newmax = 1
newmin = 0

for i in range(len(inp)):
  v = (((data[i] - minimum)/(maximum-minimum))*(newmax-newmin))+newmin
  data[i] = v
  
print(data)