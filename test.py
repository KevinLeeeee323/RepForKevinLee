from collections import deque
import heapq

ans=[11, 2, 43, 94, 6]
# heapq.heapify(ans)
h=[]
for value in ans:
    heapq.heappush(h, value)
while h:
    tmp=heapq.heappop(h)
    
    # heapq.heappush(ans, tmp+5)
    # tmp2=heapq.heappop(ans)
    print(tmp)



p=[1, 2, 3, 4, 5, 6, 7, 8, 9]
v=[10, 9, 8, 7, 6, 5, 4, 3, 2]

for idx, value in enumerate(v):
    print(idx, value)

n=len(p)

my_list=[(x, y) for x, y in zip(p, v)]

my_list.sort(key=lambda x: x[0]/x[1], reverse=True)
print(my_list)