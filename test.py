


class Solution:
    def findFinalValue(self, nums: list[int], original: int) -> int:
        nums_sorted=sorted(nums, reverse=False)
        def BinarySearch(start, end, key):
            left=start
            right=end
            while left<=right:
                mid=left+(right-left)//2
                if nums[mid]>key:
                    left=mid+1
                elif nums[mid]<key:
                    right=mid=1
                else:
                    return mid
        


        
        return 