#include <stdio.h>
#include <stdlib.h>

/*
    最大子数组 之 动态规划

    要解决的问题: 给定长度为 n 的无序数组, 计算最大(子数组元素之和), 并且输出此时的子数组首尾元素下标.
    子数组是指原数组中连续的一部分, 元素个数 ≥ 1

    在动态规划的框架下, 可以利用记忆化搜索的方法, 构造二维数组求解

    理论:




    时间复杂度:O(n)
*/
# define max(a, b) (((a)>(b))?(a):(b))


int MaxSubArray_DP(int* arr, int arrSize, int* start, int* end)
{
    

    // 回溯部分的代码也写在这里面, 确定最大子数组到底是哪一段

    // 记得 free()
    
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