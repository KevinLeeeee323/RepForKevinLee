'''
问题描述见 ./ProblemSet.md


输入输出:
    一个列表, 里面的元素是元组, 元组的第一个和第二个元素记录了这个活动的起始时间和终止时间.
    输出: 能够安排得开(不冲突)的最大活动数量, 以及对应的活动编号&起止时间.

暴力求解思路:
    对一个最终的选择方案, 这 N 个活动, 每个活动可能在方案中, 也可能不在方案中.
    这样就有 2^N 中初步方案--其中有些方案中, 会有活动相冲突, 对于这种, 是不可取的.
    剩下可取的中, 可以枚举, 遍历出对应的最大活动数量.

    因此, 暴力枚举思路: 枚举这 2^N 种情况(包括所有都不选的). 对于其中有活动冲突的, 不考虑; 对于无活动冲突的, 从中选出最大活动数量的.
    复杂度>=O(2^N).

贪心算法求解思路:
    下设计贪心算法求解: 优先考虑最先结束的活动, 这样可以证明能够取得最大大数量的不冲突活动
    
    先对所有活动按照结束时间从早到晚排序, 并维护一个选择活动的列表.

    将活动按照结束时间依次添加到列表中, 当然, 要看其是否和当前已经添加的活动冲突.
    判断方式: 
        显然这个列表中, 所有活动的结束时间也是递增的.
        那么只需判断, 当前待加入的活动的开始时间是否>=当前列表中最后一项的结束时间.
        如果是, 那就放进列表.
        如果不是, 那就不放进去

    算法的证明: https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=36

最终复杂度:
    排序部分, O(N*logN)
    遍历部分, O(N)

    因此, 最终复杂度O(N*logN)
'''

class Solution():
    def __init__(self, act_list:list[tuple]):
        self.len_act=len(act_list)

        ''' 
            依据 act_list进行排序. 
            将原始输入: (起始时间, 终止时间)tuple 写成(起始时间, 终止时间, 原始下标)tuple
            从而方便记录排序前的顺序
        '''
        self.act_list=[(act[0], act[1], idx) for idx, act in enumerate(act_list)]
        act_list_sorted=sorted(self.act_list, key=lambda x: x[1], reverse=False) # 依活动的完成时间升序排序活动
        ActivityNum=0

        self.Selected_act_List=[] # 记录最终选择的活动
        for act in act_list_sorted:
            if self.Selected_act_List==[]: # 空列表, 可以选入该活动
                self.Selected_act_List.append(act)
                ActivityNum+=1
            elif act[0]>=self.Selected_act_List[-1][1]:
                '''
                act[0]: 起始时间
                act[1]: 终止时间
                act[2]: 该活动的原始下标
                非空列表, 需要满足当前要选入的活动不和已经选入的活动冲突. 
                由于已按照完成时间升序排列(记录选入活动的列表的结束时间也是升序), 
                因此只需要判断当前要选入的活动的开始时间是否大于当前列表最后一个活动(self.Selected_act_List[-1])的结束时间即可判断是否冲突
                '''
                self.Selected_act_List.append(act)
                ActivityNum+=1
        
        self.MaxActivityNum=ActivityNum
        

if __name__=='__main__':
    actList=[(8, 12), (1, 4), (6, 10), (0, 6), (12, 16), (4, 7), (3, 9), (3, 5), (5, 9), (8, 11), (2, 14), ]
    ans=Solution(act_list=actList)
    print('选中活动的总数为:', ans.MaxActivityNum)
    print('选中的活动以及对应的起止时间为:')
    for act in ans.Selected_act_List:
        print('活动id(从 0 开始):', act[2], '  起止时间:', act[0], '~', act[1])
