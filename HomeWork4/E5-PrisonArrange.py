def read_input():
    N, M=map(int, input().split())
    conf_list=[]
    conf_adjM=[[0 for _ in range(N+1)] for _ in range(N+1)]
    for _ in range(M):
        u, v, c=map(int, input().split())
        conf_list.append((u, v,c))
        conf_adjM[u][v]=conf_adjM[v][u]=c
    return N, conf_list, conf_adjM

def arrange(N, conf_list, conf_adjM): # assume conf already sorted
    conf_sorted=sorted(conf_list, key=lambda x:x[2], reverse=True)
    # print(conf_sorted)

    pri=[[], []]
    max_conf=[0, 0]
    # 下标 0, 1分别对应两个监狱

    arranged=[False for _ in range(N+1)]
    for u, v, w in conf_sorted:
        if arranged[u]==True and arranged[v]==True:
            return max(max_conf)
        '''
        insight:
        return 的时机应该是 max_conf 突然从[0, 0]变到其中一个非 0 或者两个都不是 0?
        理论上, 只要 max_conf 不等于 0, 那么之后的操作, 由于 conf_sorted 是降序排列好的, 那么
        之后一定不需要更新 max_conf
        换而言之, 更新 max_conf 只有在不等于 0 这个期间需要?
        那么接下来的问题就是, 如何维护 max_conf?
        
        ''' 
        if not arranged[u] and arranged[v]:
            




if __name__=='__main__':
    N, conf_list, conf_adjM=read_input()
    print(arrange(N, conf_list, conf_adjM))
