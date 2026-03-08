'''
生成 1-n这 n 个数组成的全排列, 并以任意顺序返回答案
e.g. n=3, 答案为:
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
'''


def gen_full_permutation(n:int)->list[list[int]]:
    permutation=[]

    def dfs(cur_list):
        if len(cur_list)==n:
            permutation.append(cur_list)
            return
        for num in range(1, n+1):
            if num not in cur_list:
                dfs(cur_list+[num])
    
    dfs([])
    return permutation

'''
全排列问题中，核心约束是：同一个位置的元素不能在同一个排列中重复使用
上面的代码中, 用 if num not in cur_list 来检查, 这虽然是对的，但在计算机底层，它其实做了一件很费劲的事：
每到一个新数字，程序都要把 cur_list 从头到尾扫一遍，看看这个数字在不在里面。
如果列表很长，这个扫描过程会越来越慢。
used 数组的作用就是把这个“扫描”过程变成“一眼扫过”：
我们开辟一块和 nums 同样长度的空间(used 数组)，专门记录哪个位置被占了。
见下方gen_full_permutation_modified()函数
'''


def gen_full_permutation_modified(n:int)->list[list[int]]:
    permutation=[]
    used=[False for _ in range(n)]
    path=[]

    def dfs():
        if len(path)==n:
            permutation.append(path[:])
            return
        for num in range(1, n+1):
            if used[num-1]==False:
                used[num-1]=True
                path.append(num)
                dfs()
                path.pop()
                used[num-1]=False

    dfs()
    return permutation


if __name__=='__main__':
    n=4
    permutation=gen_full_permutation(n)
    print(permutation, len(permutation))

    permutation=gen_full_permutation_modified(n)
    print(permutation)


