'''
问题描述见 ./ProblemSet.md
下设计动态规划算法求解

输入输出:
    一个列表, 里面的元素是元组, 元组的第一个和第二个元素记录了这个活动的起始时间和终止时间, 第三个元素记录了这个活动的租金.
    输出: 能够安排得开(不冲突)的活动的最大租金之和, 以及对应活动的(编号, 起止时间, 租金).

问题求解:
   
    贪心算法无法求解, 因此使用动态规划算法.

    这里为了方便叙述, 认为这 N 个活动下标从 1 开始, 为 a_1, a_2, ... a_N.
    原因: 
        该问题具有局部最优解性质. 
        当在看a_i 所在时间段, 是否选 a_i对最大租金收入带来的影响时, 应该让 a_i 之前的时段, 租金收入已经处于最大.
    
    先将这些活动按照结束时间从早到晚排序.
    为了方便下面使用, 新增 2 个活动:
    a_0: 结束时间早于排序后的活动中, a_1 的起始时间. 因此, a_0 的结束时间最早. a_0 收益为 0.
    a_(N+1): 起始时间晚于排序后的活动中, a_N的结束时间. 因此, a_(N+1)的结束时间最晚. a_(N+1)收益为 0
    由于 a_0, a_(N+1)的时间设置, 因此可以把他们直接放到排序后的活动的最前头(a_0)和最后头(a_(N+1))而不影响.

    可以设一维动态规划数组 dp[N+1], dp[i]=M表示排序后的{a_0, a_1, a_2, ..., a_i}中不冲突活动的最大收益为 M. 

    然后另外维护一个数组 p, p[i]=j表示在活动 a_i 开始前, 结束时间最晚的活动为 a_j.
    这一块可以通过二分查找实现: a_i的开始时间作为(key), 待查找的数组是活动的结束时间构成的.之前已经排好序了, 所以可以用二分查找.

    根据这样, 可以写出递推公式:
    dp[i]=max(dp[p[i]]+w_i, dp[i-1])
    理解: 对于取得排序后的{a_0, a_1, a_2, ..., a_i}中不冲突活动的最大收益为, a_i 有两种状态:
    1. 当选了 a_i, 那就要求 a_i 前面的这些活动收益最大, 也就是{a_0, a_1, a_2, ..., a_p[i]}中不冲突活动有最大收益(根据 p[i]=j 的定义), 对应于 dp[p[i]].
        然后加上 a_i 自身的活动租金收益 w_i, 得到 dp[i]=dp[p[i]]+w_i.

    2. 如果 a_i 没有选, 由于活动 a_(i-1)的结束时间早于 a_i, 且此时必有p[i]<=i-1, 为要求a_i 前面的这些活动收益最大, dp[i]=dp[i-1].

    dp[i]取以上的较大值. 可以用另一个数组 Selected[], 来记录较大值时对应的状况, 即到底选没选 a_i. 选了 Selected[i]=1, 反之为零.

    
    特别的, dp[0]=0.
    最终, 整个问题的答案为 dp[N]. 

    在取得最终结果后, 根据 Selected[]的情况进行回溯, 即可确定最大租金收益时, 选择了哪些活动.

复杂度分析:
    首先进行按照结束时间从早到晚将活动排序,复杂度 O(N*logN)
    随后为了生成 p数组, 对每个元素进行了二分查找(每一次查找复杂度 O(logN), 共 N 个元素(不算补的 a_0, 因为没进行对其的二分查找), 故复杂度 O(N*logN)
    随后进行动态规划, 外层循环 1~N, 复杂度 O(N)
    随后进行回溯, 复杂度小于 O(N)
    因此, 最终总的复杂度 O(N*logN)


    关于这部分的更多内容, 参考: https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=37 
'''

class Solution():
    def __init__(self, act_time_list:list[tuple], act_rent_list:list):
        self.len_act=len(act_time_list)

        ''' 
            依据 act_list进行排序. 
            原始输入有两个List:
                act_time_list: (起始时间, 终止时间)tuple 
                act_rent_list: 记录了每个活动的租金

            将其写成((起始时间, 终止时间), 租金, 原始下标) tuple 所组成的 List, 
            从而方便记录排序前的顺序
        '''

        self.act_list=[(act_time, act_rent, idx) for idx, (act_time, act_rent) in enumerate(zip(act_time_list, act_rent_list))]
        act_list_sorted=sorted(self.act_list, key=lambda x: x[0][1], reverse=False) # 依活动的完成时间升序排序活动
        act_list_sorted=[((0, 0), 0, 0)] + act_list_sorted # 添加 活动a_0
    
        def BinarySearch(key): # 二分查找, 查找递增的活动时间结束序列中, 结束时间<=key(a_i 的开始时间)的最后一个活动
            left=0
            right=self.len_act
            res=0 # 可能是的正确答案
            while left<=right:
                mid=left+(right-left)//2 # 不同于C语言int除法会取整. 这里应该用'//'进行取整
                if act_list_sorted[mid][0][1]<=key:
                    res=mid
                    left=mid+1
                else:
                    right=mid-1
            return res

        p = [0] * (self.len_act + 1)  # p[0] = 0（a_0 的前置活动）
        for i in range(1, self.len_act + 1):
            key = act_list_sorted[i][0][0]
            p[i] = BinarySearch(key)  # 传入排序后的列表供查找
            
        # 以下: 进行动态规划
        dp=[0 for i in range(self.len_act+1)]
        self.act_select_status=[0 for i in range(self.len_act+1)] # 记录第 i 个活动是否被选了
        self.act_selected_list=[]

        for i in range(1, self.len_act+1):
            tmp1=dp[i-1]
            tmp2=dp[p[i]]+act_list_sorted[i][1]
            if tmp1>tmp2: # 不选a_i
                dp[i]=tmp1 
                
            else:
                dp[i]=tmp2 # 选a_i
                self.act_select_status[i]=1

        # 通过回溯, 找出最终选了什么
        def Retrieve():
            i=self.len_act
            while i>0:
                if self.act_select_status[i]==1:
                    self.act_selected_list.append(act_list_sorted[i]) # 这个活动被选中, 存储其下标
                    i=p[i]
                else:
                    i-=1 # a_i 没被选, 往前看 a_(i-1). 

            self.act_selected_list=sorted(self.act_selected_list, key=lambda x:x[2], reverse=False) # 调整成原始下标从小到大的方式输出
        
        Retrieve() # 进行回溯,
        self.MaxActivityNum=len(self.act_selected_list)
        self.MaxIncome=sum(act[1] for act in self.act_selected_list)
        
        
if __name__=='__main__':
    act_time_List=[ (1, 4), (3, 5), (0, 6), (4, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14)]
    act_rent_List=[1, 6, 4, 7, 3, 12, 2, 9, 11, 8]

    ans=Solution(act_time_list=act_time_List, act_rent_list=act_rent_List)
    print('选中活动的总金额为:', ans.MaxIncome)
    print('选中活动的总数为:', ans.MaxActivityNum)
    print('具体活动选取情况为:')
    for act in ans.act_selected_list:
        print('活动id(下标最小值从1开始):', act[2]+1, '  起止时间:', act[0][0], '~', act[0][1], '租金:', act[1])
    
