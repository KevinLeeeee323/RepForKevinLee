import heapq
from sys import stdin
def Prim_PriQue()->int:

    data = list(map(int, stdin.read().split()))
    ptr = 0
    verNum = data[ptr]
    edgesNum = data[ptr+1]
    ptr += 2

    adj_list=[[] for _ in range(verNum)]
    for _ in range(edgesNum):
        u=data[ptr]-1
        v=data[ptr+1]-1
        w=data[ptr+2]
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))
        ptr+=3

    MAX_DIST=float('inf')

    selected=[False for _ in range(verNum)]
    dist=[MAX_DIST for _ in range(verNum)]
    pred=[-1 for _ in range(verNum)] 
        
    # minimum_spanning_tree=set() # MST
    mst_total_weight=0 # MST所有边权重之和

    pq=[] # 最小堆

    dist[0]=0
    pred[0]=-1
    
    heapq.heappush(pq, (dist[0], 0))
   
    while pq:
        current_dist, u_key=heapq.heappop(pq)

        if selected[u_key] == True or current_dist>dist[u_key]: 
            continue

        if pred[u_key] != -1:
            # minimum_spanning_tree.add((pred[u_key], u_key))
            mst_total_weight += current_dist

        selected[u_key]=True

        for u, w in adj_list[u_key]:
            if not selected[u] and w<dist[u]:
                dist[u]=w
                pred[u]=u_key
                heapq.heappush(pq, (dist[u], u))

    return mst_total_weight 

if __name__=='__main__':
    ans=Prim_PriQue()
    print(ans)