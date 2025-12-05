import numpy as np

# 强化学习PPT P20

def initR(mat_size, edges):

    mat=np.full((mat_size, mat_size), fill_value=-1, dtype=np.int16)
    edges=np.array(edges, dtype=np.int16)
    for (i, j, k) in edges:
        if k==0:
            mat[i, j]=mat[j, i]=k
        else:
            mat[i, j]=k
    return mat


def recurseQ(matQ, matR, cnt:int, gamma:float, goal_id:int):  # 迭代

    if cnt<0:
        print(f'wrong input of cnt as cnt=={cnt} < 0')
        return None
    
    mat_size=np.shape(matQ)[0]

    for i in range(0, cnt):

        # 随机选择一组(x, y), 满足:
        #  x!=goad_id(x 不是目标点, 若是的话没必要迭代) 
        #  x!=y(不是自己原地绕圈)
        #  matR[x, y]!=-1 (x到 y 有路径)

        while True:
            x = np.random.randint(0, mat_size)
            y = np.random.randint(0, mat_size)
            if x!=goal_id and x != y and matR[x, y] != -1:
                break

        # 对其进行初始化
        edge_list=[]
        for z in range(0, mat_size):
            if matR[y, z]>=0:
                edge_list.append(matQ[y, z])
        if len(edge_list)>0: # 有 y->z 的路径, 且满足上满选 x, y 的条件才迭代
            edge_list=np.array(edge_list)   
            matQ[x, y] = matR[x, y]+ gamma * np.max(edge_list)


def main():
    
    size=8
    edges=[(0, 4, 0), (4, 5, 0), (5, 6, 0), (1, 5, 0), (1, 2, 0), (2, 6, 0), (2, 3,0), (6, 7, 0), (2, 3, 100), (3, 3, 100)] 
    # 元素是三元数组(i,j,k), 分别记录了房间 i 到 j 的权值 k

    mat_Reward=initR(size, edges)

    cnt=500
    gamma=0.8

    mat_Q=np.zeros((size, size), dtype=np.float32)
    # print(mat_Q)
    recurseQ(mat_Q, mat_Reward, cnt, gamma, goal_id=3)

    np.set_printoptions(
        precision=3,          # 保留2位小数（可根据需求调整为1或3）
        linewidth=1000,       # 单行最大宽度（设大些，避免自动换行）
        suppress=True         # 禁用科学计数法（避免出现1.2e+02这类格式）
    )

    print(mat_Q)


if __name__=='__main__':
    main()

