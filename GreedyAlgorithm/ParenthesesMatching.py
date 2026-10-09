'''
题目来源: LeetCode1541 https://leetcode.cn/problems/minimum-insertions-to-balance-a-parentheses-string/description/?envType=daily-question&envId=2026-10-09
给你一个括号字符串 s ，它只包含字符 '(' 和 ')' 。一个括号字符串被称为平衡的当它满足：
任何左括号 '(' 必须对应两个连续的右括号 '))' 。
左括号 '(' 必须在对应的连续两个右括号 '))' 之前。
比方说 "())"， "())(())))" 和 "(())())))" 都是平衡的， ")()"， "()))" 和 "(()))" 都是不平衡的。
你可以在任意位置插入字符 '(' 和 ')' 使字符串平衡。请你返回让 s 平衡的最少插入次数。

原始版本的括号匹配, 来自 LeetCode921 https://leetcode.cn/problems/minimum-add-to-make-parentheses-valid/description/
'''


'''
解法: 贪心.
left_cnt 记录当前未匹配的'('的数量.
由于在这道题目中, 需要每两个')'抵消一个'(', 因此, 抵消的逻辑应该是:
    如果 s[i]=='(': 直接 left_cnt+=1, i+=1 即可
    如果 s[i]=='(' 且 s[i+1]==')': 才可能抵消'(':
        如果 left_cnt==0, 那就没有能够抵消的'('了, 需要补充'(', 答案+1, 并且 i+=2
        如果 left_cnt>0, 那可以抵消, left_cnt-=1, i+=1
    如果 s[i]=='(', s[i+1]!=')'或者 没有 s[i+1](下标超出字符串长度), 那就得补一个')', 答案+=1

最后, 如果有多余的左括号, 也就是遍历到最后left_cnt>0, 那就要补上对应 left_cnt*2 个')'    
'''

class Solution:
    def minInsertions(self, s: str) -> int:
        left_cnt=0
        ans=0
        n=len(s)
        i=0
        while i<n:
            print(i, left_cnt, ans)
            if s[i]=='(':
                left_cnt+=1
                i+=1
            else: # s[i]==')'
                if i<n-1 and s[i+1]==')':
                    i+=2
                else:
                    ans+=1
                    i+=1

                if left_cnt>0:
                    left_cnt-=1
                else:
                    ans+=1
            
        return ans+left_cnt*2

s="(()))(()))()())))"
print(Solution().minInsertions(s))