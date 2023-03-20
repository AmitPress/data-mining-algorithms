with open('values.txt', 'r') as f:
  inp = list(map(int, f.read().split('\n')))

inp = sorted(inp)
size = 3
n_buckets = len(inp)//size
bucket = [[0 for _ in range(size)] for _ in range(n_buckets)]

inp = iter(inp)
for i in range(n_buckets):
    for j in range(size):
      bucket[i][j] = next(inp)

for i in range(n_buckets):
    sum = 0
    for j in range(size):
      sum += bucket[i][j]
    avg = sum/3
    for j in range(size):
      bucket[i][j] = avg

print(bucket)