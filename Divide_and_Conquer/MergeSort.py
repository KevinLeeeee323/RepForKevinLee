# MergeSort with Python Implementation

def merge_sort(nums:list[int]):
    n=len(nums)
    merge_sort_divide_and_conquer(0, n-1, nums)


def merge_sort_divide_and_conquer(left:int, right:int, nums:list[int]):
    if left<right:
        mid=left+(right-left)//2
        merge_sort_divide_and_conquer(left, mid, nums)
        merge_sort_divide_and_conquer(mid+1, right, nums)

        tmp=[0 for _ in range(right-left+1)]
        i=left; j=mid+1
        k=0
        while i<=mid and j<=right:
            if nums[i]<nums[j]:
                tmp[k]=nums[i]
                i+=1
            else:
                tmp[k]=nums[j]
                j+=1
            k+=1
        if i<=mid:
            tmp[k:]=nums[i:mid+1]
        else:
            tmp[k:]=nums[j:right+1]
        nums[left:right+1]=tmp
        
# 修改2: if i<=mid:
        #     tmp[k:]=nums[i:mid+1]
        # else:
        #     tmp[k:]=nums[j:right+1]
        # nums[left:right+1]=tmp
        # 逻辑写反了, i<=mid, concatnate i 相关而不是 i==mid, concatnate j 相关

nums=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
merge_sort(nums)
print(nums)


