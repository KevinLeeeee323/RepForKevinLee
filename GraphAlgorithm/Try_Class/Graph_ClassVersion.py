import numpy as np
from collections import deque
from typing import Optional
from abc import ABCMeta, abstractmethod  # 用于定义抽象基类

'''
关于 BFS, DFS, 去看 No_Class_Code 那里面的写法, 统一了全局接口和指定顶点 DFS/BFS 的接口




'''


class Graph():
    """图的抽象基类，定义公共属性和接口，提取所有图的共性逻辑"""
    def __init__(self, Vertices_id:list[int], Edges:list[tuple[int, int]]):
        self.vertices=Vertices_id
        self.edges=Edges

        self.verNum=len(Vertices_id)
        self.edgeNum=len(Edges)

        self.adjM=self.build_adjacent_matrix()
    
    
    @abstractmethod
    def build_adjacent_matrix(self):
        """抽象方法:构建邻接结构(邻接矩阵/邻接表), 子类必须实现"""
        pass
   
    @abstractmethod
    def is_Directed(self)->bool:
        """抽象方法:判断图是否有向, 子类必须实现(True=有向, False=无向)"""
        pass
    

    @abstractmethod
    def get_edge_weight(self, u: int, v: int) -> float:
        """抽象方法：获取边(u,v)的权重, 子类必须实现(无权图返回1, 带权图返回实际权重)"""
        pass


    def BFS_from_certain_node(self, start_id):
        '''
            从某一个节点开始, 进行 BFS(广度优先) 搜索

            参数:
                start_id: 开始搜索的结点下标

            BFS的三个辅助数组:
                mark: 用于记录当前结点的访问情况.
                    mark[i]= 0:未访问, 1:在队列中, 2:已处理

                pred: pred[i]=j 表示在当前的BFS 搜索中, 是通过下标为 j 的结点找到了下标为 i 的结点.
                    对于 i=start_id, pred[start_id]=-1, 表示其没有前驱.

                dist: dist[i]=j, 表示当前点 BFS 搜索中, 下标为i 的结点到 start_id 的距离是 j.
                    因为这里是无向无权图, 可以证明, j 就是下标为i 的结点到 start_id 的最短距离.
        
            复杂度分析:(从 start_id 进行 BFS的复杂度, 不一定是全图 BFS复杂度, 因为搜不到start_id 不可达的结点)  
                详见 PPT 对应部分
                时间复杂度为:O(self.verNum + self.edgeNum)
                空间复杂度, 三个长度为 self.verNum 的数组, 空间复杂度 O(self.verNum)
        '''
        mark=np.full(shape=(self.verNum), fill_value=0)
        pred=np.full(shape=(self.verNum), fill_value=-1)
        dist=np.full(shape=(self.verNum), fill_value=np.inf)

        que=deque()
        que.append(start_id)
        mark[start_id]=1
        pred[start_id]=-1
        dist[start_id]=0

        while que:
            v=que.popleft()
            mark[v]=1

            yield v
            '''
            采用了生成器的方式.

            yield 类似于 return, 但不完全相同
            return:函数结束, 返回结果
            yield:暂停函数执行, 返回一个值, 下次调用时从暂停处继续执行

            这样就可以实现, BFS 每次搜索到一个节点, 就暂停, 返回当前搜索到的结点给外部使用. 
            外部调用结束后, 在从之前暂停的位置继续执行.
            '''
            
            # 遍历所有与v相邻, 且没有被添加到队列中(待处理)的结点
            for u in range(self.verNum):
                if self.adjM[v, u]==1 and mark[u]==0:
                    que.append(u)
                    mark[u]=1
                    dist[u]=dist[v]+1
                    pred[u]=v
            mark[v]=2 # 标志着对下标为v的结点处理完成
        
        print('color', mark)
        print('pred', pred)
        print('dist', dist)

        # print('\n')
    

    def DFS_from_certain_node(self, start_id):
        '''
            从某一个节点开始, 进行 DFS(广度优先) 搜索

            参数:
                start_id: 开始搜索的结点下标

            DFS的三个辅助数组:
                mark: 用于记录当前结点的访问情况.
                    mark[i]= 0:未访问, 1:在队列中, 2:已处理

                pred: pred[i]=j 表示在当前的DFS 搜索中, 是通过下标为 j 的结点找到了下标为 i 的结点.
                    对于 i=start_id, pred[start_id]=-1, 表示其没有前驱.

                d: d[i] = j 表示节点 i 的「发现时间」（首次被访问时的时间戳）
                f: f[i] = j 表示节点 i 的「完成时间」（所有邻接节点都处理完后的时间戳）
                    时间通过变量 time 管理, 初始时刻(还没开始第一次搜索)认为 time=0.
                
            复杂度分析:(从 start_id 进行 DFS的复杂度, 不一定是全图 DFS复杂度, 因为搜不到start_id 不可达的结点)
                详见 PPT 对应部分
                时间复杂度为:O(self.verNum + self.edgeNum)
                空间复杂度, 四个长度为 self.verNum 的数组, 空间复杂度 O(self.verNum)
        '''

        mark=np.full(shape=(self.verNum), fill_value=0)
        pred=np.full(shape=(self.verNum), fill_value=-1)
        d=np.full(shape=(self.verNum), fill_value=-1)
        f=np.full(shape=(self.verNum), fill_value=-1)

        time=0

        def DFS_visit_node(v):
            nonlocal time  # 关键：声明time是外层函数的局部变量，允许修改
            mark[v]=1
            time+=1
            d[v]=time
            yield v

            for u in range(self.verNum):
                if self.adjM[v, u]==1 and mark[u]==0:
                    pred[u]=v
                    yield from DFS_visit_node(u) # 递归访问子节点，并将子节点的生成器结果传递出去
            mark[v]=2 # 标记完成
            time+=1
            f[v]=time # 记录完成时间

        yield from DFS_visit_node(start_id) # 启动递归，并返回生成器（支持for循环迭代）

        '''
            yield from:
                把一个生成器的所有输出, 原封不动地传递给当前生成器的调用者, 还能自动处理递归 / 嵌套场景的迭代逻辑，不用手动写循环转发。
        '''
        print("mark", mark)
        print("pred", pred)
        print("d:", d)
        print("f:", f)

    '''
        上面考虑的都是一个连通图.
        对于不连通图, 一次 DFS 最多覆盖一个联通分量, 无法覆盖整张图.
        如果想要进行全局 DFS/BFS, 需要对所有节点做 DFS/BFS.
        具体做法, 开设一个全局 mark 数组. 
            for v in range(self.verNum):
                if mark[v]==0:
                    yield from DFS/BFS_from_certain_node(v) # 要加上yield from
    ''' 
   

class Unweighted_Graph(Graph):
    def __init__(self, Vertices_id: list[int], Edges: list[tuple[int, int]]):
       super().__init__(Vertices_id, Edges)


class Weighted_Graph(Graph):
    def __init__(self, Vertices_id: list[int], Edges: list[tuple[int, int]], Edge_Weights:list[int]):
        super().__init__(Vertices_id, Edges)
    '''也许这里在__init__时, 需要多一个 EdgesWeights 参数传进来???'''



class Simple_Undirected_Unweighted_Graph(Graph): 
    '''
        简单无向无权图.
        简单: 每两个节点之间只有一条边(单向/双向)
        无向: (u, v)之间有一条边, 则 u 可到 v, v 可到 u.
        无权: 所有边的权值都为 1, 或者一个相同的值.

        要求:
        一个有 n个结点的简单无向无权图, 结点 id 范围 0, 1, 2... n-1.
        边通过 Edges 数组存储, 每个元素是一个数组(u, v), 表示下标为u, v 结点之间存在一条无向无权边.
    '''

    def __init__(self, Vertices_id:list[int], Edges:list[tuple[int, int]]):
        
        self.vertices=Vertices_id
        self.edges=Edges

        self.verNum=len(Vertices_id)
        self.edgeNum=len(Edges)

        self.adjM=self.build_adjacent_matrix()
    

    def build_adjacent_matrix(self)-> np.ndarray: # 构建邻接矩阵
        adjM=np.zeros((self.verNum, self.verNum))
        for pair in self.edges:
            adjM[pair[0], pair[1]]=1
            adjM[pair[1], pair[0]]=1
        return adjM
    

class Simple_Directed_Unweighted_Graph(Unweighted_Graph):
    def __init__(self, Vertices_id: list[int], Edges: list[tuple[int, int]]):
        super().__init__(Vertices_id, Edges)

 

    
  


if __name__=='__main__':
    n=8
    Vertices_id=[i for i in range(8)]
    Edges=[(0, 4), (0, 1), (1, 5), (2, 5), (5, 6), (2, 6), (2, 3), (3, 6), (6, 7), (3, 7)]
    test_graph=Simple_Undirected_Unweighted_Graph(Vertices_id, Edges)
    my_start_id=1

    for vertex_id in test_graph.BFS_from_certain_node(my_start_id):
        print(vertex_id, end=' ')

    for vertex_id in test_graph.DFS_from_certain_node(0):
        print(vertex_id, end=' ')