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

    n=4
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


if __name__=='__main__':
    n=4

    # bfs
    binary_codes_bfs=gen_binary_strings_bfs(n)
    print(binary_codes_bfs)

    # dfs
    binary_codes_dfs=gen_binary_strings_dfs(n)
    print(binary_codes_dfs)


