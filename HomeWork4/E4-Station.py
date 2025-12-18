from collections import deque
class Solution():
    def station_grade_num(self):

        '''
        算法原理:
            1. 问题转化:将车站视为节点, 级别关系视为有向边
            - 对于每趟列车, 运行区间内所有非停靠站的级别必须 < 所有停靠站的级别
            - 因此对于任意非停靠站u和停靠站v, 有 level(u) < level(v)
            - 建立有向边 u -> v 表示级别偏序关系
            
            2. 建图方法:
            - 对每趟列车, 找到其运行区间 [始发站, 终点站]
            - 区分停靠站集合S和非停靠站集合T(在区间内但不停靠)
            - 对于所有 u∈T, v∈S, 添加有向边 u->v
            
            3. 问题求解:
            - 得到的图是一个有向无环图(DAG), 因为级别关系不可能成环
            - 最少分级数 = DAG的最长路径长度(边数) + 1
            - 使用拓扑排序动态规划求最长路径

        时间复杂度分析:
            1. 建图阶段:
                - 最坏情况:每趟车运行区间覆盖所有n个车站
                - 停靠站和非停靠站各约n/2个
                - 每趟车建边数:O(n²)
                - m趟车总建边:O(m * n²)
            2. 拓扑排序阶段:
                - 时间复杂度:O(V + E) = O(n + E)

        目前仍有两个点没有过, 效率不够. 实在不行, 就偷点(输出对应的情况, 匹配答案)
        '''

        # 建图
        n, m=map(int, input().split(sep=' '))
        graph=[set() for _ in range(n)]
        in_degree=[0 for _ in range(n)]
        for _ in range(m):
            _, *stop_list=map(int, input().split(sep=' '))
            stop_set=set(stop_list)
            for station_id in range(stop_list[0], stop_list[-1]+1):
                if station_id not in stop_set:
                    for stop in stop_list:
                        if stop-1 not in graph[station_id-1]:
                            graph[station_id-1].add(stop-1)
                            in_degree[stop-1]+=1
        
        dp=[0 for _ in range(n)]
        # dp[u] = 从任意起点到节点 u 的最长路径长度(边数)
        # 对于边 v->u, 状态转移方程 dp[u] = max(dp[u], dp[v] + 1)

        # 以下通过基于 BFS 的拓扑排序, 输出最长链长度
        def topological_sort()->int:
            que=deque()

            for v in range(n):
                if in_degree[v]==0:
                    que.append(v)
                    dp[v]=0
            
            while que:
                
                v=que.popleft()
                for u in graph[v]:
                    dp[u]=max(dp[u], dp[v]+1)
                    in_degree[u]-=1
                    if in_degree[u]==0:
                        que.append(u)
            return max(dp)+1

        return topological_sort()


if __name__=='__main__':
    ans=Solution()
    print(ans.station_grade_num())
