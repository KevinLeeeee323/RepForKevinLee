import numpy as np

class Graph():
    def __init__(self, Vertices_id:list[int], Edges_weight:list[tuple[int, int]]):
        self.vertices=Vertices_id
        self.edges=Edges_weight

        self.verNum=len(Vertices_id)
        self.edgeNum=len(Edges_weight)

        self.adjM=self.build_adjacent_matrix()
    

    def build_adjacent_matrix(self)-> np.ndarray: # 构建邻接矩阵, 但是认为是有向带权图
        adjM=np.zeros((self.verNum, self.verNum))
        for pair in self.edges:
            adjM[pair[0], pair[1]]=self.edges
        return adjM
    

    def BFS(self):
        pass


    def DFS(self):
        pass
    

        