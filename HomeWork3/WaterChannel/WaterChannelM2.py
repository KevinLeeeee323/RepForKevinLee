from collections import deque, defaultdict

def preprocess_reachable_plants(N, M, height):
    """
    反向BFS(从第一行所有蓄水厂出发,向下遍历可达的沙漠城市)
    时间复杂度O(N*M),仅需一次遍历,替代原逐个沙漠城市BFS
    返回:
        dry_to_plant: 每个沙漠城市可达的蓄水厂集合
        unreachable_cnt: 不可达的沙漠城市数量
    """
    # 反向建图:记录每个城市能到达的蓄水厂
    dry_to_plant = [set() for _ in range(M)]
    # 反向BFS:从第一行所有蓄水厂出发,向下遍历
    visited = [[set() for _ in range(M)] for __ in range(N)]  # 记录每个城市已访问过的蓄水厂,避免重复
    q = deque()
    
    # 初始化:第一行所有蓄水厂入队
    for plant_id in range(M):
        q.append((0, plant_id))
        visited[0][plant_id].add(plant_id)  # 第一行自身就是蓄水厂
    
    # 四个方向(上下左右,重点向下/左右)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while q:
        x, y = q.popleft()
        current_plants = visited[x][y]  # 当前城市能到达的蓄水厂集合
        
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            # 边界检查
            if 0 <= nx < N and 0 <= ny < M:
                # 反向BFS核心:从高到低流(当前城市海拔 > 下一个城市海拔)
                if height[x][y] > height[nx][ny]:
                    # 计算新能到达的蓄水厂(未被记录的)
                    new_plants = current_plants - visited[nx][ny]
                    if new_plants:
                        # 合并已访问的蓄水厂集合
                        visited[nx][ny].update(new_plants)
                        q.append((nx, ny))
    
    # 统计沙漠行(N-1行)的结果
    unreachable_cnt = 0
    for dry_id in range(M):
        reachable = visited[N-1][dry_id]
        dry_to_plant[dry_id] = reachable
        if not reachable:
            unreachable_cnt += 1
    
    return dry_to_plant, unreachable_cnt

def set_cover(universe: set, subsets: list[set]) -> tuple[int, int]:
    """集合覆盖"""

    # 过滤空子集(无覆盖能力)
    subsets = [s for s in subsets if s]
    if not subsets and universe:
        return 0, len(universe)
    
    uncovered = universe.copy()
    selected = 0
    
    # 预处理子集字典:key=子集索引,value=子集内容
    subset_dict = {i: s for i, s in enumerate(subsets)}
    
    while uncovered and subset_dict:
        best_idx = -1
        max_cover = -1
        
        # 遍历所有剩余子集,找覆盖最多未覆盖元素的
        for idx in list(subset_dict.keys()):
            s = subset_dict[idx]
            cover = len(s & uncovered)
            if cover == 0:
                # 该子集无覆盖能力,移除
                del subset_dict[idx]
                continue
            if cover > max_cover:
                max_cover = cover
                best_idx = idx
        
        if best_idx == -1:
            break  # 无可用子集
        
        # 选中最优子集,更新未覆盖集合
        selected += 1
        best_subset = subset_dict[best_idx]
        uncovered -= best_subset
        del subset_dict[best_idx]
    
    if not uncovered:
        return 1, selected
    else:
        return 0, len(uncovered)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    N = int(input[ptr])
    ptr += 1
    M = int(input[ptr])
    ptr += 1
    
    height = []
    for _ in range(N):
        row = list(map(int, input[ptr:ptr+M]))
        ptr += M
        height.append(row)
    
    # 反向BFS预处理所有沙漠城市可达的蓄水厂
    dry_to_plant, unreachable_cnt = preprocess_reachable_plants(N, M, height)
    
    if unreachable_cnt > 0:
        print(0)
        print(unreachable_cnt)
    else:
        # 转换为每个蓄水厂能覆盖的沙漠城市集合
        plant_to_dry = defaultdict(set)
        for dry_id in range(M):
            for plant_id in dry_to_plant[dry_id]:
                plant_to_dry[plant_id].add(dry_id)
        plant_to_dry_list = [plant_to_dry.get(i, set()) for i in range(M)]
        
        # 集合覆盖
        universe = set(range(M))
        flag, ans = set_cover(universe, plant_to_dry_list)
        print(flag)
        print(ans)