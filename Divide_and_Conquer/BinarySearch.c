#include <stdio.h>
#include <stdlib.h>

/*
    给定一个 N=arrSizde 个元素有序的(升序)整型数组 arr 和一个目标值 key,
    通过二分查找的方式搜索 nums 中的 key, 如果 key 存在返回下标, 否则返回 -1

    二分查找复杂度: O(logN)
    利用子数组有序性, 每次都在子数组中查找
*/

/*---------------------------------------------------*/
// 版本一:递归
int Search(int left, int right, int key, int* arr)
{
    if(left<right)
    {
        if(arr[left]>key || arr[right]<key)
            return -1;
        int mid=(left+right)/2;
        int left_result=Search(left, mid, key, arr);
        int right_result=Search(mid+1, right, key, arr);
        return (left_result==-1)?right_result:left_result;
    }
    else //主要是针对left==right而设计的, 但数组只有一个元素时也会出现 left>right, 但返回-1, 不影响
        return (arr[left]==key)?left:-1;
}

int BinarySearch_Recursive(int key, int* arr, int arrSize)
{
    return Search(0, arrSize-1, key, arr);
}

/*---------------------------------------------------*/
//版本二: 不使用递归
// int BinarySearch_NoRecursive(int key, int* arr, int arrSize)
// {
//     int left=0, right=arrSize-1;
//     int mid=-1;
//     while(left<right)
//     {
//         mid=(left+right)/2;
//         if(arr[mid]>key)
//             right=mid;
//         else if(arr[mid]<key)
//             left=mid+1;
//         else //arr[mid]==key
//             return mid;
//     }
//     return arr[left]==key?left:-1;
// }

// 以上是我自己写的二分查找
// 以下是主流的二分查找写法(非递归版), 一些细节略有出入:
int BinarySearch_MainStream(int key, int* arr, int arrSize)
{
    int left=0;
    int right=arrSize-1;
    int mid=-1;
    while(left<=right)
    {
        mid=left+(right-left)/2; //这一行见下面的多行注释
        if(arr[mid]==key)
            return mid;
        else if(arr[mid]<key)
            left=mid+1; 
        else //arr[mid]>key
            right=mid-1; //和自己写的不一样
    }
    return -1; //不用像自己写的那种, 还要判断
}

/*---------------------------------------------------*/

/*
    二分查找变体
    变体的目的, 不是只查当前目标元素 key 是否在数组里面, 而是找到符合要求(比如大于或大于等于 key)的最小下标
    相比普通二分查找, 多的一点就是, 用一个 res 存储可能的正确答案, 如果后面有更符合的, 就更新 res 的值.
*/

int BinarySearch_LowerBound(int key, int* arr, int arrSize) {
    // 找到第一个>= 目标值key 的元素位置
    int left = 0;
    int right = arrSize - 1;
    int res = arrSize;
    int mid=-1;
    while (left <= right) 
    {
        mid = left + (right - left) / 2;
        if (arr[mid] >= key) 
        {
            res = mid;      // 可能是答案
            right = mid - 1;   // 向左查找更优解
        } 
        else
            left = mid + 1;   // 向右查找
    }
    return res;
}

int BinarySearch_UpperBound(int key, int* arr, int arrSize) {
    // 找到第一个严格大于 目标值key 的元素位置
    int left = 0;
    int right = arrSize - 1;
    int res = arrSize;
    int mid=-1;
    while (left <= right) 
    {
        mid = left + (right - left) / 2;
        if (arr[mid] > key) 
        {
            res = mid;      // 可能是答案
            right = mid - 1;   // 向左查找更优解
        } 
        else
            left = mid + 1;   // 向右查找
    }
    return res;
}

/*
    当 left 和 right 都是较大的正数时，它们的和可能超出整数类型的最大范围：
    mid = (left + right) / 2：
    如果 left 和 right 都接近 INT_MAX
    left + right 会溢出，导致结果错误
    例如：left = right = 1e9 时，和会溢出

    mid = left + (right - left) / 2：
    先计算 right - left，结果一定小于 right
    再除以 2，结果更小
    最后加上 left，不会发生溢出
    所以推荐写 mid = left + (right - left) / 2
*/

/*---------------------------------------------------*/
// 以下是使用样例
int main()
{
    int arr[]={-5, -1, 0, 0, 0, 11, 19, 23};
    int size=sizeof(arr)/sizeof(int);
    int key=19;

    // 方法一
    printf("%d\n", BinarySearch_Recursive(key, arr, size));

    // 方法二
    printf("%d\n", BinarySearch_NoRecursive(key, arr, size));

    //对比以下两种变体
    printf("%d\n", BinarySearch_LowerBound(key, arr, size)); //寻找第一个>=key 的
    printf("%d\n", BinarySearch_UpperBound(key, arr, size)); // 寻找第一个>key 的
}
