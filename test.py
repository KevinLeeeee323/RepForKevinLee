from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        
        if root is None:
            return False
        
        def _dfs(node:TreeNode, cur_sum)->bool:
            if node.left is None and node.right is None:
                return cur_sum+node.val==targetSum
            
            if node.left is not None:
                if _dfs(node.left, cur_sum+node.val):
                    return True
            if node.right is not None:
                if _dfs(node.right, cur_sum+node.val):
                    return True
                
            return False
                       
        return _dfs(root, 0)
    

if __name__=='__main__':
    print(1==3)
    
