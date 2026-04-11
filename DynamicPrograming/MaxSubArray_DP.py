# MaxSubArray with Python Implementation

def max_sub_array(nums:list[int])->tuple[int, int, int]:

    n=len(nums)

    dp=[0 for _ in range(n)]
    dp[n-1]=nums[n-1]

    max_sub_array_end=[0 for _ in range(n)]

    max_sub_array_value=dp[n-1]
    max_sub_array_end[n-1]=n-1
    max_sub_array_id_mark=n-1

    '''
    max_sub_array_value: 存储最终的最大子数组数值.
    max_sub_array_id_mark: 取到 max_sub_array_value 时的子数组起始点

    dp[i]: 以下标为i 开始的最大子数组的数值
    max_sub_array_end[i]: 以下标为i 开始的最大子数组的终止下标
    '''

    for i in range(n-2, -1, -1):
        if dp[i+1]<0:
            dp[i]=nums[i]
            max_sub_array_end[i]=i
        else:
            dp[i]=dp[i+1]+nums[i]
            max_sub_array_end[i]=max_sub_array_end[i+1]

        if dp[i] > max_sub_array_value:
            max_sub_array_id_mark=i
            max_sub_array_value=dp[i]

    print(f'max subarray happens from id_{max_sub_array_id_mark} to id_{max_sub_array_end[max_sub_array_id_mark]}')
    print(f'the max subarray value is {max_sub_array_value}')
    return max_sub_array_id_mark, max_sub_array_end[max_sub_array_id_mark], max_sub_array_value


if __name__=='__main__':
    nums=[-2,1,-3,4,-1,2,1,-5,4]
    max_sub_array(nums)
