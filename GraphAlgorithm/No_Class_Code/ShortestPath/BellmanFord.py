def bellman_ford(start_id:int, verNum:int, edges:list[tuple[int, int, float]], is_directed=True, with_track_print=False)->list[float]:

    '''
    bellman_ford 算法, 用于处理有负权重边的最短路径.(已假设图上没有负环)

    bellman ford 算法不可以处理的场景: 
    图上存在一个环, 从一个起点绕这个环走一周, 所经路径的权重之和<0.
    在这种情况下, 不断绕着这个环走, 路径权重可以最终减到-\\inf, 没法定义最短路径.
    凡是经过这个环的路径, 无穷多次绕这个环之后再走出来, 最短路径都可以是负无穷.
    这样的环, 称为[负环].

    但是对于一个无向图, 如果其有一条负边: 比如, 结点 1 和 2 相连, 权重-1, 那么就有负环: 1->2->1
    因此, Bellman ford 算法如果想要用在无向图上, 就必须保证无向图没有负权重的边.


    生成 start_id 到图上其余所有点 v的最短路径
    所有节点的下标范围: 0, 1, 2, ... verNum-1. verNum 为总的节点数.

    param:
        start_id: 计算最短路径的源点.
        edges: 边的列表. 列表中每个元素(u, v, w)表示边(u, v), 带有权重w.
        is_directed: 是否为有向图. 是有向图, 标记为 True. 无向图为 False. 遍历的时候,(u, v, w)和(v, u, w)各遍历一遍.
    
    output: 
        dist 数组. dist[u]=d: start_id 到 u 最短路径长度 d.

    关于为什么算法最外面要有一个|V|-1 的循环?
    可以参考下面的视频 https://www.youtube.com/watch?v=9PHkk0UavIM
    其原因主要是, 在这张图上, 两点之间的最短路径最多有|V|-1 个边.
    假设有多于|V|-1 个边, 那么由于|V|-1 个边最多连接|V|个不同节点, 
    在这个长度>|V|-1的路径上, 一定有重复的顶点, 即, 有一个环.
    根据我们的假设, 这个环一定不是负环. 换而言之, 绕着这个环走一周, 路径权重会增大.
    那还不如不绕着这个环走. 不绕着环走, 可以获得更小的路径权重.
    因此, 最短路径一定不出现在有|V|-1个边的路径上, 
    也就是说, 最短路径已经是简单路径(不经过重复顶点)

    视频里说, 只要寻找|V|-1 次, 就一定能够找到两点之间的最短路径.
    是在考虑找最短路径的最差情况: u, v_1, v_2, ...v_{|V|-1}这个路径上依次经历了|V|个结点, |V|-1 条边.
    在这种情况下, 需要松弛操作|V|-1次, 才能让 dist[v_{|V|-1}]从正无穷松弛到一个正常的数.
    做完这|V|-1 轮松弛操作后,  该条路径上任意两点的最短路径也就确定了(可以反设存在更短的路径, 那这样的话u, v_1, v_2, ...v_{|V|-1}就不是最短的路径, )
    但根据AI:
        外层循环 verNum-1 次的原因:
        1. 两点间的最短路径(简单路径, 无环)最多包含 verNum-1 条边(verNum 个节点最多连 verNum-1 条边);
        2. 若路径超过 verNum-1 条边, 必然包含环, 非负环会增加路径权重, 可舍弃;
        3. 每轮循环至少确定一个节点的最短路径, verNum-1 轮可覆盖所有可达节点.

    下面的代码分为三部分: 初始化, 松弛|V|-1轮, 第|V|轮判断有无负环.
    各轮次复杂度分别为 O(|V|), O(|V||E|), O(|E|)
    因此, 总的复杂度 O(|V||E|)
    '''


    if not is_directed:
        for _, _, w in edges:
            if w<0:
                print('Bellman ford 算法不可以用在有负权重边的无向图中')
                return []
    
    dist=[float('inf') for _ in range(verNum)]
    dist[start_id]=0
    # 以上: 初始化. 复杂度O(|V|)

   
    # 初始化前驱数组:pred[v] 表示 v 在最短路径上的前驱节点, -1 表示无前驱
    pred=[-1 for _ in range(verNum)]

    # 核心松弛操作:最多 verNum-1 轮. 该部分复杂度:O(|V||E|)
    for _ in range(verNum-1):
        update=False # 标记本轮是否更新距离, 无更新则提前终止
        for u, v, w in edges: 
            if dist[u]!=float('inf') and dist[v]>dist[u]+w: # 处理正向边 u→v
                dist[v]=dist[u]+w
                pred[v]=u
                update=True

            
            if not is_directed: # 处理无向图的反向边 v→u
                if dist[v]!=float('inf') and dist[u]>dist[v]+w:
                    dist[u]=dist[v]+w
                    pred[u]=v
                    update=True
        
        if update==False: # 本轮若无更新则提前终止
            break

    # 检测负环: 该部分复杂度 O(|V|)
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[v] > dist[u] + w: # 检测 u->v 方向上的负环
            has_negative_cycle = True
            break

        '''
        对于无向图, 也需要检测 v->u 方向上的负环. 
        因为无向图时把每一个(u, v, w)当成两条边(u->v 方向)和(v->u方向)来处理.
        由于前面在无向图且有负边的时候early return 了, 那么这个时候, 
        如果图是无向图, 那么必然不会有负环(因为没有负权重的边)
        所以这里不再需要对 v->u 方向进行检查.
        if not is_directed and dist[v] != float('inf') and dist[u] > dist[v] + w:
            has_negative_cycle = True
            break
        '''

    if has_negative_cycle:
        print("图中存在负权环, 无法计算最短路径")
        return []

    # 路径回溯与打印. 该部分复杂度: O(|E|)
    if with_track_print:
        track=[[] for _ in range(verNum)]
        for v in range(verNum):
            if v==start_id:
                track[v]=[v]
                continue
            
            if pred[v]==-1:
                track[v]=[f'not reachable from {start_id}']
                continue

            path=[]
            u=v
            while not u==-1:
                path.append(u)
                u=pred[u]
            track[v]=path[::-1] # 反转路径
        print(track)

    return dist


# ------------------- 测试验证 -------------------
if __name__ == "__main__":
    # 测试1:有向图(带负权边, 无负环)
    print("--- 测试1:有向图(带负权边)---")
    verNum = 4
    start_id = 0
    edges = [(0,1,5.0), (0,2,10.0), (1,2,-3.0), (1,3,20.0), (2,3,4.0)]
    dist = bellman_ford(start_id, verNum, edges, is_directed=True, with_track_print=True)
    print("最短路径距离数组:", dist)
    print('\n')

    # 测试2:无向图(带负权边)
    print("--- 测试2:无向图(带负权边)---")
    verNum_undir = 4
    edges_undir = [(0,1,5.0), (1,2,-3.0), (2,3,4.0)]
    dist_undir = bellman_ford(start_id, verNum_undir, edges_undir, is_directed=False, with_track_print=True)
    print("最短路径距离数组:", dist_undir)
    print('\n')

    # 测试3:有向图, 负权环场景
    print("--- 测试3:负权环场景 ---")
    verNum_neg = 3
    edges_neg = [(0,1,1.0), (1,2,-3.0), (2,1,1.0)]  # 1→2→1 是负权环
    dist_neg = bellman_ford(0, verNum_neg, edges_neg, is_directed=True, with_track_print=True)
    print("负权环场景返回值:", dist_neg)