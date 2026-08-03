'''
链接 486题: https://leetcode.cn/problems/predict-the-winner/description/
给你一个整数数组 nums 。玩家 1 和玩家 2 基于这个数组设计了一个游戏。
玩家 1 和玩家 2 轮流进行自己的回合，玩家 1 先手。
开始时，两个玩家的初始分值都是 0 。
每一回合，玩家从数组的任意一端取一个数字（即，nums[0] 或 nums[nums.length - 1]），
取到的数字将会从数组中移除（数组长度减 1 ）。
玩家选中的数字将会加到他的得分上。当数组中没有剩余数字可取时，游戏结束。
如果玩家 1 能成为赢家，返回 true 。
如果两个玩家得分相等，同样认为玩家 1 是游戏的赢家，也返回 true 。
你可以假设每个玩家的玩法都会使他的分数最大化。

与之高度相似的877题: https://leetcode.cn/problems/stone-game/description/
'''
from typing import List

'''
解法一: 我自己想的. 通过递归, 模拟比赛的种种情况.
    tmp 表示当前剩下的数组.
    turn==1 表示轮到 player1 的回合(p1)
    turn==2 表示轮到 player2 的回合(p1)
    然后分别讨论取当前数组第一个(下标 0)和最后一个的情况.
    赢的话, 要注意逻辑是 or 还是 and

    复杂度: O(2*n), 容易超时
'''

def predictTheWinner_v1(nums: List[int]) -> bool:
    def one_round(p1_score, p2_score, turn, tmp):
        if len(tmp)==1:
            if turn==1:
                return p1_score+tmp[0]>=p2_score
            else:
                return p1_score>=tmp[0]+p2_score
        if turn==1:
            ans1=one_round(p1_score+tmp[0], p2_score, 2, tmp[1:]) 
            ans2=one_round(p1_score+tmp[-1], p2_score, 2, tmp[:-1]) 
            return ans1 or ans2
        else: # turn==2
            ans1=one_round(p1_score, p2_score+tmp[0], 1, tmp[1:]) 
            ans2=one_round(p1_score, p2_score+tmp[-1], 1, tmp[:-1])
            return ans1 and ans2
            '''
            p2 手握两个选择（拿左 / 拿右），他一定会挑对自己最有利、让 p1 输的那条路。
            如果 p2 选左边，p1 输；
            或者 p2 选右边，p1 输；
            p2 只要找到任意一条能搞输 p1 的走法，他就会走那条。
            翻译成逻辑：
            只有 p2 不管选左边还是选右边，p1 最后全都能赢，这一局面对 p1 来说才是稳赢
            也就是必须：ans1 and ans2（两条分支 p1 全赢），才返回 True；
            '''

    return one_round(0, 0, 1, nums)


'''
方法1.5: 
    方法 1 中, tmp[1:], tmp[:-1]每次递归都会创建新列表，过于复杂.
    本质上来说, nums数组一直没有发生过变化, 因此完全可以不用重新赋值.
    把 tmp[1:], tmp[-1:]这种切片, 用双指针改写.
    e.g. 拿了  tmp[idx=0], 下一轮从 tmp[1:]中取, 相当于在nums 中某一个下标(l)开始:
    (因为 tmp 不一定是 nums, 而是 nums的一部分)
    拿了 nums[l], 下一轮从nums[l+1:]开始, 也就是从下标 l+1 开始, 到 r 截止

    e.g. 拿了  tmp[idx=n-1], 下一轮从 tmp[:-1]中取, 相当于在nums 中某一个下标(r)开始:
    (因为 tmp 不一定是 nums, 而是 nums的一部分)
    拿了 nums[r], 下一轮从nums[:r-1]开始, 也就是从下标 l 开始, 到 r-1 截止
'''
def predictTheWinner_v1_point_5(nums: List[int]) -> bool:
    def one_round(p1_score, p2_score, turn, l, r):
        if l==r:
            if turn==1:
                return p1_score+nums[l]>=p2_score
            else:
                return p1_score>=nums[l]+p2_score
        if turn==1:
            ans1=one_round(p1_score+nums[l], p2_score, 2, l+1, r) 
            ans2=one_round(p1_score+nums[r], p2_score, 2, l, r-1) 
            return ans1 or ans2
        else: # turn==2
            ans1=one_round(p1_score, p2_score+nums[l], 1, l+1, r) 
            ans2=one_round(p1_score, p2_score+nums[r], 1, l, r-1)
            return ans1 and ans2
            '''
            p2 手握两个选择（拿左 / 拿右），他一定会挑对自己最有利、让 p1 输的那条路。
            如果 p2 选左边，p1 输；
            或者 p2 选右边，p1 输；
            p2 只要找到任意一条能搞输 p1 的走法，他就会走那条。
            翻译成逻辑：
            只有 p2 不管选左边还是选右边，p1 最后全都能赢，这一局面对 p1 来说才是稳赢
            也就是必须：ans1 and ans2（两条分支 p1 全赢），才返回 True；
            '''
    n=len(nums)
    return one_round(0, 0, 1, 0, n-1)





'''
方法二:
    返回“净胜分”，即 当前玩家得分 - 对手得分
    dfs(l, r) 的定义是：
    在当前玩家面对子数组 nums[l:r+1] 时，当前玩家能获得的最大净胜分（当前玩家得分 - 对手得分）
    这个定义天然包含了"轮到谁"的信息——谁调用 dfs，谁就是"当前玩家"

    假设dfs(l, r)调用时, 当前玩家为player1. 
    dfs(l, r)中调用dfs(l+1, r), dfs(l+1, r)时当前玩家为 player2, 返回 player2 得分-player1 得分
    因此, left_score=nums[l]-dfs(l+1, r) 表示 player1 拿到的分数-下一轮(player2 得分-player1 得分)
    即 player1 本轮分数+player1 在后续轮次拿到的分数-player2 在后续轮次拿到的分数之和
    由于本轮不是 Player2 行动, 因此player2 在后续轮次拿到的分数=player2 从本轮开始到游戏结束轮次拿到的分数
    即=player1 本轮以及之后轮次拿到的分数之和-player2 本轮以及之后轮次拿到的分数之和
    符合 dfs(l, r)定义!

    只要 dfs(0, n-1)>=0, 则 player1 赢;
    反之 player2 赢.


'''
from functools import lru_cache 
def predictTheWinner_v2(nums: List[int]) -> bool:
    '''
    @lru_cache(None) 是 Python 中的一个装饰器（Decorator），
    它的作用是为函数自动添加记忆化（Memoization）缓存
    第一次调用 dfs(0, 5) 时，执行完整函数，计算结果并缓存。
    后续再调用 dfs(0, 5)（比如从不同路径到达），直接返回缓存结果，瞬间完成。
    每次传入的 (l, r) 组合不同，就会创建新的缓存条目
    这样递归之前算出来的, 不会重新算, 而是复用结果.
    '''
    @lru_cache(None)
    def dfs(l, r):
        if l==r:
            return nums[l]
        
        left_score=nums[l]-dfs(l+1, r)
        right_score=nums[r]-dfs(l, r-1)
        # dfs(l, r)表示当前调用这个函数时, 当前玩家得分-对手玩家得分: 净胜分

        return max(left_score, right_score)
        # max 表示：当前玩家是理性的, 因此在两种选择面前, 当前玩家会选择让自己净胜分最大的那个走法
    n=len(nums)
    return dfs(0, n-1)>=0



'''
方法三: 
    在上面, 很显然 dfs 只和 l, r有关. dfs(l, r)经过递归, 其中一些子递归项会算很多遍.
    这里通过 lru_cache 使其不用算很多遍.
    还有另一种方法, 就是记忆化搜索, 也可以不让其算很多遍.
    也就是, 动态规划, 直接用dp[l][r]存储 dfs(l, r), 构建递推式, 最终返回 dp[0][n-1]
'''
def predictTheWinner_v3(nums: List[int]) -> bool:
    n=len(nums)
    dp=[[0 for _ in range(n)] for _ in range(n)]
    # dfs(l, r)=dp[l][r] 表示当前调用这个函数时, 当前玩家得分-对手玩家得分: 净胜分
    for i in range(n):
        dp[i][i]=nums[i]
    for k in range(1, n):
        for l in range(n-k):
            # 注意二维动态规划推导的方向
            r=l+k
            left_score=nums[l]-dp[l+1][r]
            right_score=nums[r]-dp[l][r-1]
            dp[l][r]=max(left_score, right_score)
            # max 表示：当前玩家是理性的, 因此在两种选择面前, 当前玩家会选择让自己净胜分最大的那个走法     
    return dp[0][n-1]>=0