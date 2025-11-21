from collections import deque

def can_reach_plant(id, height)->set:
    """检查干旱城市(N-1, id)能覆盖哪些干旱城市"""
    q = deque()
    visited = [[False] * M for _ in range(N)]
    q.append((N-1, id))
    visited[N-1][id] = True
    reachable_plant=set()
    
    if N-1 == 0:
        reachable_plant.add(id)

    while q:
        x, y = q.popleft()
        
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
                if height[x][y] < height[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    if nx==0:
                        reachable_plant.add(ny)
    return reachable_plant

def SetCover_WithoutCost(universe: set, subsets: list[set]) -> tuple[int, int]:
    """
    集合覆盖贪心算法实现
    
    参数:
        universe: 全集U(待覆盖的所有元素集合)
        subsets: 子集族S(每个元素是一个子集,类型为set)
    
    返回:
        selected_subsets: 选中的子集组合(覆盖全集的最小近似解)
        covered_elements: 最终覆盖的元素集(若未完全覆盖,可查看未覆盖元素)
    """

    # 初始化:未覆盖元素 = 全集,选中子集为空,总成本为0
    uncovered = universe.copy()  # 避免修改原始全集
    selected_subsets = []

    # 贪心循环:直到所有元素被覆盖或无更多子集可选择
    while uncovered and subsets:
        # 计算每个子集的“覆盖当前未覆盖的元素的数量”(优先级指标)
        best_subset = None
        max_covered_cnt = -1  # 统计当前轮次中, 能覆盖最多为覆盖元素的子集

        for idx, subset in enumerate(subsets):
            # 该子集能覆盖的“未覆盖元素”数量
            covered_cnt = len(subset & uncovered)
            if covered_cnt == 0:
                continue  # 该子集无新覆盖元素,跳过

            # 选择覆盖未覆盖元素最多的子集
            if covered_cnt > max_covered_cnt:
                max_covered_cnt=covered_cnt
                best_subset = subset
                best_idx = idx  # 记录最优子集的索引,后续移除

        if best_subset is None: # 若没有找到能覆盖新元素的子集,退出循环(部分覆盖)
            break

        # 选中该子集:更新选中列表, 未覆盖元素
        selected_subsets.append(best_subset)
        uncovered -= best_subset  # 移除已覆盖的元素

        subsets.pop(best_idx) # 移除已选中的子集(避免重复选择), pop 方法传入要被移除的元素的id

    if not uncovered: # 没有未被覆盖的元素
        return 1, len(selected_subsets)
    else:
        return 0, len(uncovered)

if __name__=="__main__":
    N, M=map(int, input().split(sep=' '))
    height=[]
    for i in range(N):
        height.append(list(map(int, input().split(sep=' '))))

    unreachable_cnt=0 # 统计没有蓄水厂能修过去的干旱城市数量

    unreach_flag=0
    dry_to_plant=[]
    for j in range(M):
        reach=can_reach_plant(j, height)
        if not reach:
            un_flag=1
            unreachable_cnt+=1

        dry_to_plant.append(reach)

    if unreach_flag==1:
        print(0, unreachable_cnt, sep='\n')

    else:
        # 将存储每个干旱城市可达的蓄水站的数据转换成每个蓄水站可达的干旱城市的数据
        plant_to_dry=[set() for _ in range(M)]
        for dry_id in range(M):
            for plant_id in dry_to_plant[dry_id]:
                plant_to_dry[plant_id].add(dry_id)

        Universe=set([i for i in range(M)])
        flag,ans=SetCover_WithoutCost(Universe, plant_to_dry)
        print(flag, ans, sep='\n')   