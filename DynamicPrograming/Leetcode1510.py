from math import sqrt

'''
https://leetcode.cn/problems/stone-game-iv/  Leetcode 486的变种, 区别不是很大. 

题干如下:
Alice 和 Bob 两个人轮流玩一个游戏，Alice 先手。
一开始，有 n 个石子堆在一起。每个人轮流操作，正在操作的玩家可以从石子堆里拿走 任意 非零 平方数 个石子。
如果石子堆里没有石子了，则无法操作的玩家输掉游戏。
给你正整数 n ，且已知两个人都采取最优策略。如果 Alice 会赢得比赛，那么返回 True ，否则返回 False 。
'''
class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        
        dp=[[False, False] for _ in range(n+1)]
        # dp[x][0]: x stones left && Alice's turn to take, Alice是否赢
        # dp[x][1]: x stones left && Bob's turn to take, Alice 是否赢
        dp[0][0]=False
        dp[0][1]=True
        dp[1][0]=True
        dp[1][1]=False

        for i in range(2, n+1):
            tmp=int(sqrt(i))
            if tmp*tmp==i:
                dp[i][0]=True
                dp[i][1]=False
            else:
                ans1=False
                ans2=True
                for j in range(1, tmp+1):
                    ans1=ans1 or dp[i-j*j][1]
                    ans2=ans2 and dp[i-j*j][0]
                '''
                仍然是要注意这里的逻辑.
                对于 dp[i][0], 这一步时 Alice 的轮次, Alice 自己执生杀大权,
                    只要 dp[i-j*j][1]中有一个让 Alice可以赢, 
                    那 Alice 就可以拿 j*j 个, 从而赢, 因此用 or 连接
                    基于这个逻辑, 用 ans1=False 连接;
                对于 dp[i][1], 这一步时是 Bob 的轮次, Alice 没法干预 Bob,
                    因此, 如果 Alice 想赢, 不管 Bob 选哪个j*j,
                    必须得要 dp[i-j*j][0]都得是 Alice赢才行, 
                    否则 Bob 必然会直接选择那个让 Alice 输的. 
                    因此用 and 连接
                    基于这个逻辑, 用 ans2=True 连接

                这里之所以用 ans1 和 ans2, 
                是因为没法像 Leetcode486 那样直接写出所有情况and / or 在一起,
                必须得逐个操作, 合并到已有的结果(ans1 / ans2)中
                '''
                dp[i][0]=ans1
                dp[i][1]=ans2
        print(dp)
        return dp[n][0]

print(Solution().winnerSquareGame(4))