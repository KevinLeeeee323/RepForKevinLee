from typing import List
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        
        dig_to_le=['', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
        mark=[0 for _ in range(1, 10)]

        ans=[]

        target=len(digits)
        def dfs(path):
            if len(path)==target:
                ans.append(path)
                return 
        
            for 






