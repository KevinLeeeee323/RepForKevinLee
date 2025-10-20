#include <stdio.h>
#include <stdlib.h>

/*
    最大子数组 之 动态规划

    [问题]
        要解决的问题: 给定长度为 n 的无序数组, 计算最大(子数组元素之和), 并且输出此时的子数组首尾元素下标.
        子数组是指原数组中连续的一部分, 元素个数 ≥ 1

    [理论&思路]
        在动态规划的框架下, 可以利用记忆化搜索的方法, 构造二维数组求解

        设 dp 数组, 其中 dp[i]表示以下标为i 的元素作为起始点的最大子数组的数值.
        设 end_save 数组, 其中 end_save[i]表示以下标为i 的元素作为起始点的最大子数组的终点下标
        也就是说, dp[i]的计算中, 一定要至少包含 arr[i]这一项.
        那么可以写出递推式:
        dp[i]= (i<arrSize-1)
        \begin{cases}
            arr[i]+dp[i+1], dp[i+1]>0
            arr[i], dp[i+1]<=0
        \end{cases}

        特别的, dp[arrSize-1]=arr[arrSize-1].

        通过维护一个最大子数组数值 maxSubArray, 以及记录取得最大子数组时的起点 maxSubArrayI,
        可以定位到:
        1. 最大子数组的值 maxSubArray
        2. 取得最大子数组时, 这一段子数组的起始点下标[maxSubArrayI, end_save[maxSubArrayI]].

        具体推导见视频 https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=22 

    [时间复杂度]
        一个 for 循环, n 次遍历. 其中n 是数组长度. 时间复杂度为O(n)
*/

int MaxSubArray_DP(int* arr, int arrSize, int* start, int* end)
{
    if(arrSize==0)
    {
        printf("arrSize==0");
        return 0; // 数组中没有数字
    }
    int* dp=(int*)calloc(arrSize, sizeof(int));
    int* end_save=(int*)calloc(arrSize, sizeof(int));
    int maxSubArray=arr[0];
    /*
        这里不可以随意初始化 maxSubArray=0.
        必须要初始化为 maxSubArray 为其中一个可能的最大子数组的解.
        对于数组 arr={-1}, 这会导致最终输出值为 0.
        maxSubArray=arr[0] 是一个不错的选择.
    */
    int maxSubArrayI=0;
    for(int i=arrSize-1; i>=0; i--)
    {
        if(i<arrSize-1)
        {
            if(dp[i+1]>0)
            {
                dp[i]=arr[i]+dp[i+1];
                end_save[i]=end_save[i+1];
            }
            else
            {
                dp[i]=arr[i];
                end_save[i]=i;    
            }
        }
        else // i==arrSize-1
        {
            dp[i]=arr[i];
            end_save[i]=i;
        }
        if(dp[i]>maxSubArray)
        {
            maxSubArray=dp[i];
            maxSubArrayI=i;
        }
    }
    *start=maxSubArrayI;
    *end=end_save[maxSubArrayI];
    free(dp);
    free(end_save);
    return maxSubArray;

    /*
        当然也可以写一个 i 升序的:
        dp'[i]表示以下标为i 的元素作为终点的最大子数组的数值

        设 start_save 数组, 其中 start_save[i]表示以下标为i 的元素作为终点点的最大子数组的起点下标
        也就是说, dp[i]的计算中, 一定要至少包含 arr[i]这一项.
        那么可以写出递推式:
        dp[i]=
        \begin{cases}
            arr[i]+dp[i-1], dp[i-1]>0
            arr[i], dp[i-1]<=0
        \end{cases}

        特别的, dp'[0]=arr[0].

        通过维护一个最大子数组数值 maxSubArray, 以及记录取得最大子数组时的终点 maxSubArrayI,
        可以定位到:
        1. 最大子数组的值 maxSubArray
        2. 取得最大子数组时, 这一段子数组的起始点下标[ start_save[maxSubArrayI], maxSubArrayI].
    */
}





/*------------------------------------------*/

// 以下是使用实例
int main()
{
    int arr[]={-2,1,-3,4,-1,2,1,-5,4};
    int size=sizeof(arr)/sizeof(int);
    int start=-1, end=-1; //最大子数组的起终点下标
    int ans=MaxSubArray_DP(arr, size, &start, &end);
    printf("%d %d %d", ans, start, end);
}