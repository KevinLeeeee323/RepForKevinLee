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
int BinarySearch_NoRecursive(int key, int* arr, int arrSize)
{
    int left=0, right=arrSize-1;
    int mid=-1;
    while(left<right)
    {
        mid=(left+right)/2;
        if(arr[mid]>key)
            right=mid;
        else if(arr[mid]<key)
            left=mid+1;
        else //arr[mid]==key
            return mid;
    }
    return arr[left]==key?left:-1;
}

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
}
