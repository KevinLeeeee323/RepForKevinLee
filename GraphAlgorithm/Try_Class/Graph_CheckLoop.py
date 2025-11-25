import numpy as np
from collections import deque

'''
    [问题描述]
        检查有向图中是否有环. 有环返回True, 没有返回 False

        [具体描述]
            简单有向无权图.
            简单: 每两个节点之间只有一条边(单向/双向)
            无向: (u, v)只说明了 u 可到 v, 
            无权: 所有边的权值都为 1, 或者一个相同的值.

            要求:
            一个有 n个结点的简单无向无权图, 结点 id 范围 0, 1, 2... n-1.
            边通过 Edges 数组存储, 每个元素是一个数组(u, v), 表示下标为u, v 结点之间存在一条有向无权边.
            
    
    [解决方案]
        整体方法基于 DFS.

        运用了一个性质: 有向图存在环路 充分必要条件是 搜索时出现后向边

    [复杂度分析]
        基于 DFS 方法, 只是在其上略作修改. 故同 DFS.
'''

def build_adjacent_matrix(verNum, edges): # 构建邻接矩阵
    adjM = [[0 for _ in range(verNum)] for _ in range(verNum)]
    for pair in edges:
        adjM[pair[0]][pair[1]]=1
    return adjM


def DFS_checkLoop(adjM, verNum):

    '''
        有环: 输出 True
        无环: 输出 False
    '''
    mark=[0]*(verNum)

    def DFS_visit_node(v)->bool:
        mark[v]=1   
        for u in range(verNum):
            if adjM[v][u]==1:
                if mark[u]==1:
                    return True
                elif mark[u]==0:
                    if DFS_visit_node(u)==True:
                        return True
        mark[v]=2 # 标记完成
        return False

    for v in range(verNum):
        if mark[v]==0:
            if DFS_visit_node(v)==True:
                return True
    return False

'''
    上面考虑的都是一个连通图.
    对于不连通图, 一次 DFS 最多覆盖一个联通分量, 无法覆盖整张图.
    如果想要进行全局 DFS/BFS, 需要对所有节点做 DFS/BFS.
    具体做法, 开设一个全局 mark 数组. 
        for v in range(self.verNum):
            if mark[v]==0:
                yield from DFS/BFS_from_certain_node(v) # 要加上yield from
''' 
  

# 测试样例: 详见 LeetCode207 题"课程表": https://leetcode.cn/problems/course-schedule/
    



    