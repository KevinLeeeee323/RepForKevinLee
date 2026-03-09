class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        from collections import deque
        def gen_binarys_bfs(n:int)->set:
            bi_str=[[]]
            bi_str=deque(bi_str)
            bi_set=[]

            while bi_str:
                cur=bi_str.popleft()

                if len(cur)==n:
                    bi_set.append(cur)
                    continue
                bi_str.append(cur+[0])
                bi_str.append(cur+[1])
            # print(len(bi_set))
            # print(bi_set)

            return bi_set

        def gen_subset(bi_set:list[list[int]]):
            subset_list=[]
            n=len(bi_set[0])
            for mark in bi_set:
                subset=[]
                for i in range(n):
                    if mark[i]==1:
                        subset.append(nums[i])
                subset_list.append(subset)
            
            return subset_list
        
        n=len(nums)
        bi_set=gen_binarys_bfs(n)
        print(bi_set)
        return gen_subset(bi_set)



ans=Solution()
nums=[1, 2, 3]
new=ans.subsets(nums)
print(new)
        
