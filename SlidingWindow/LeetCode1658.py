'''
移除的是 nums 最左边或最右边的元素，那么剩下的元素是什么？是 nums 的连续子数组。
移除的元素和 x + 剩余的元素和 = nums 的所有元素之和 s。
所以剩余的元素和 target= s−x。
问题变成：
从 nums 中找最长的子数组（这样移除的数尽量少），满足子数组的元素和恰好等于 s−x。

作者：灵茶山艾府
链接：https://leetcode.cn/problems/minimum-operations-to-reduce-x-to-zero/solutions/2048811/ni-xiang-si-wei-pythonjavacgo-by-endless-b4jt/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

方法一: 
    两层 for 循环遍历所有子数组, 找到最长且和为 target=s-x 的, 复杂度 O(n^2).

方法二:
    滑动窗口, 如下. 本质也是在遍历所有子数组.  
    但其实是在方法一的基础上进行了剪枝, 大大降低了复杂度, 可以到 O(n).
    这一剪枝的开展得益于数组中元素之和全为正数. 剪枝的方法和原理如下:
    假设当前遍历到的子数组为 nums[left...right], left和right为左右区间端点, 均包含在内.
    设当前子数组和为 tmp_sum.
    置区间左端点 left 初始值为 0, 然后从 0~n-1 遍历 right:
        若 tmp_sum < target, 由于 nums 所有数均为正数, right 作为右端点在向右延展, 才有可能让 tmp_sum 增大至 target;
        若 tmp_sum > target, right 作为右端点在向右延展. 由于 nums 所有数均为正数, 故只会让 tmp_sum 进一步增大,
            故无需考虑以 left 为左端点, 右区间端点>=right 的子数组了, 直接剪枝掉.
        若 tmp_sum==target, 则这是一个可能的结果, 保存下来(因为需要最大的数组长度)
'''

class Solution:
    def minOperations(self, nums: list[int], x: int) -> int:
        n=len(nums)
        min_op=float('inf')
        target=sum(nums)-x
        if target==0:
            return n
        elif target<0:
            return -1
        tmp_sum=0
        right=-1
        left=0
        for right in range(0, n):
            tmp_sum+=nums[right]
            while tmp_sum>target:
                tmp_sum-=nums[left]
                left+=1
                
            if tmp_sum==target:
                min_op=min(min_op, n-(right-left+1))
        if min_op==float('inf'):
            return -1
        else:
            return int(min_op)

if __name__=='__main__':
    nums = [3,2,20,1,1,3]
    x = 10
    print(Solution().minOperations(nums, x))
            