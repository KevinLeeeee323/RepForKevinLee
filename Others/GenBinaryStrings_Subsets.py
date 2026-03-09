'''
生成所有长度为 n 的二进制码字符串.

e.g. n=4, 输出结果为:
'1110', '0111', '1001', '0101', '1010', '1111', '0110', '0010', 
'1000', '0001', '0100', '0011', '0000', '1011', '1100', '1101'

整体思路: BFS/DFS. 都是从空字符串开始, 不断增加字符串长度直到为 n 停止.
'''

from collections import deque
def gen_binary_strings_bfs(n:int)->set:
    bi_str=[""]
    bi_str=deque(bi_str)
    bi_set=set()

    while bi_str:
        cur=bi_str.popleft()

        if len(cur)==n:
            bi_set.add(cur)
            continue
        bi_str.append(cur+'0')
        bi_str.append(cur+'1')
    # print(len(bi_set))
    # print(bi_set)

    return bi_set


def gen_binary_strings_dfs(n:int)->set:
    bi_set=set()

    def dfs(cur_str:str):
        if len(cur_str)==n:
            bi_set.add(cur_str)
            return
        dfs(cur_str+'0')
        dfs(cur_str+'1')

    dfs('')
    return bi_set

'''


在 bi_set 二进制编码的基础上, 可以进一步做题: 生成一个集合的全部子集(幂集)
原序列中的每个数字 a_i 的状态可能有两种，即「在子集中」和「不在子集中」。
我们用 1 表示「在子集中」，0 表示不在子集中，那么每一个子集可以对应一个长度为 n 的 0/1 序列，
第 i 位表示 a_i​是否在子集中。例如，n=3 ，a={5,2,9} 时：

0/1序列| 子集 | 0/1 序列对应的二进制数
000	    {}	     0
001	    {9}	     1
010	    {2}	     2
011	    {2,9}	 3 
100	    {5}	     4
101	    {5,9}	 5
110	    {5,2}	 6
111	    {5,2,9}	 7
可以发现 0/1 序列对应的二进制数正好从 0 到 2^n−1.
我们可以枚举 mask∈[0,2^n−1]，mask 的二进制表示是一个 0/1 序列，我们可以按照这个 0/1 序列在原集合当中取数。
当我们枚举完所有 2^n个 mask，我们也就能构造出所有的子集。

def gen_subset(bi_set:list[list[int]]):
    subset_list=[]
    n=len(bi_set[0])
    for mark in bi_set:
        subset=[]
        for i in range(n):
            if mark[i]==1:
                subset.append(nums[i])
        subset_list.append(subset)
    
    return subset_list
'''

if __name__=='__main__':
    n=5

    # bfs
    binary_codes_bfs=gen_binary_strings_bfs(n)
    print(binary_codes_bfs)

    # dfs
    binary_codes_dfs=gen_binary_strings_dfs(n)
    print(binary_codes_dfs)


