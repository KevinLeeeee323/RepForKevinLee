from typing import List
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        mark=[0 for _ in range(n+1)]
        ans=[]

        def dfs(tmp):
            if len(tmp)==k:
                ans.append(tmp)
                return

            for v in range(1, n+1):
                if mark[v]==1:
                    return
                
                mark[v]=1
                dfs(tmp+[v])
                mark[v]=0

        dfs([])
        
        return ans

ans=Solution()
n = 5
k = 3
print(ans.combine(n, k))