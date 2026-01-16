'''
这道题的正确解法思路
核心思路：二分答案 + 扩展域并查集
二分答案：我们要找「最大冲突的最小值」,可以二分这个最小值 mid,判断「是否存在一种分配方式,使得所有怨气值 > mid 的罪犯都被分到不同监狱」;
扩展域并查集：把每个罪犯 x 拆成两个节点 ——x（表示 x 在监狱 0）和 x+N（表示 x 在监狱 1）：
若罪犯 a 和 b 怨气值 > mid,说明 a 和 b 必须分在不同监狱：合并 a 和 b+N、合并 b 和 a+N;
若合并时发现 a 和 b 已经在同一集合（说明无法分开）,则 mid 不可行,需要增大 mid;
若所有怨气值 > mid 的罪犯都能分开,则 mid 可行,尝试减小 mid.
算法步骤
把所有仇恨对按怨气值降序排序;
二分范围：左边界 0,右边界 最大怨气值;
对每个二分的 mid,用扩展域并查集检查是否合法;
最终找到的最小可行 mid 就是答案.

时间复杂度 O(MlogC)（C 是最大怨气值）
'''



class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))  # 父节点数组
        self.rank = [1] * size           # 按秩合并优化
    
    def find(self, x): # 查找x的根节点
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y): # 合并x和y所在的集合
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False  # 已经在同一集合,合并失败
        # 按秩合并：把秩小的树合并到秩大的树下
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
        return True

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    idx = 0
    N = int(data[idx])
    idx += 1
    M = int(data[idx])
    idx += 1
    
    # 存储所有仇恨对 (a, b, c)
    hate_pairs = []
    max_c = 0
    for _ in range(M):
        a = int(data[idx])
        idx += 1
        b = int(data[idx])
        idx += 1
        c = int(data[idx])
        idx += 1
        hate_pairs.append((a, b, c))
        if c > max_c:
            max_c = c
    
    # 二分答案：找最小的最大冲突值
    left = 0
    right = max_c
    ans = 0
    
    while left <= right:
        mid = (left + right) // 2
        # 扩展域并查集：x表示在监狱0,x+N表示在监狱1
        uf = UnionFind(2 * N + 1)  # 编号1~2N
        valid = True
        
        for a, b, c in hate_pairs:
            if c <= mid:
                continue  # 怨气值<=mid,即使同监狱也不影响,无需处理
            # a和b分到不同监狱：a和b+N合并,b和a+N合并
            if uf.find(a) == uf.find(b):
                # a和b已经在同一集合,无法分开,mid不可行
                valid = False
                break
            uf.union(a, b + N)
            uf.union(b, a + N)
        
        if valid:
            # mid可行,尝试找更小的
            ans = mid
            right = mid - 1
        else:
            # mid不可行,需要增大
            left = mid + 1
    
    print(ans)

if __name__ == "__main__":
    solve()