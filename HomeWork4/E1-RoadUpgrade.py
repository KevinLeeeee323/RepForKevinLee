

def build_adj(verNum:int, edges:list[tuple[int, int, int]]):
    # vertex id:1~verNum
    # in graph we have vertex id 0~verNum-1

    adj=[[] for _ in range(verNum)]
    for u, v, w in edges:
        adj[u-1].append((v-1, w))
        adj[v-1].append((u-1, w)) # Undirected Graph

    return adj

def dfs(verNum, adj:list, start_id:int):

    # vertex id: 0~verNum-1
    visited=[0 for _ in range(verNum)]
    
    routes=[]

    def _dfs(start_id, cur_route:list[int]):
        visited[start_id]=1
        cur_route.append(start_id)

        for v, _ in adj[start_id]:
            if not visited[v]:
                _dfs(v, cur_route)
            
        routes.append(cur_route)
            
    _dfs(start_id, [])

    print(routes)


if __name__=='__main__':
    verNum=9
    edges=[(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), 
           (4, 6, 1), (6, 7, 1), (4, 8, 1), (2, 9, 1)]
    adj=build_adj(verNum, edges)
    dfs(verNum, adj, 0)



