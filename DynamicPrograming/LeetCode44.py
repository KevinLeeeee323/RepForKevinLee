'''
给你一个输入字符串 (s) 和一个字符模式 (p) ，请你实现一个支持 '?' 和 '*' 匹配规则的通配符匹配：
'?' 可以匹配任何单个字符。
'*' 可以匹配任意字符序列（包括空字符序列）。
判定匹配成功的充要条件是：字符模式必须能够 完全匹配 输入字符串（而不是部分匹配）。

(注意: '?'不能匹配空字符)
'''

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        n=len(s)
        m=len(p)

        if m==0:
            return n==0
        
        # m>0:  Using Dynamic Programming
        dp=[[False for _ in range(n+1)] for _ in range(m+1)]
        # dp[i][j]==True <==> p[0, 1, ...i-1] can match s[0, 1, ...j-1]
        # 注意上面定义中的角标
        dp[0][0]=True
        for i in range(m):
            if p[i]=='*':
                dp[i+1][0]=True
            else:
                break
        
        for i in range(1, m+1):
            for j in range(1, n+1):
                # 递推式如下
                if p[i-1]=='*': 
                    if dp[i-1][j] or dp[i][j-1] or dp[i-1][j-1]:
                        dp[i][j]=True
                elif p[i-1]=='?':
                    if dp[i-1][j-1]:
                        dp[i][j]=True
                else:
                    dp[i][j]=(dp[i-1][j-1] and p[i-1]==s[j-1])
        for i in range(m+1):
            print(dp[i])
        return dp[m][n]


if __name__=='__main__':
    # s = "adceb"; p = "*a*b"
    # s = "aa"; p = "a"
    # s = "aa"; p = "*"
    # s = "cb"; p = "?a"
    # s="abcabczzzde"; p="*abc???de*"
    s=''; p='?'
    print(Solution().isMatch(s, p))




