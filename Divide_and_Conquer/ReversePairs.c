#include <stdio.h>
#include <stdlib.h>

/*
    要解决的问题, 统计数组中的逆序对总数, 其中数组 arr 长度 为 n.
    一个逆序对可以这样定义: (0≤i<j≤n-1)
    X(i,j)=1 iff (arr[i]>arr[j])
    统计所有逆序对数, 即求 \sum_{i=0}^{j=n-1}{X(i,j)}

    以下分别是几种解法:
    1. 暴力求解
    2. 分治算法(思路上类似归并排序, 但会造成原始数组在经过算法后会被按照升序重新排序)

    // 补充一个高等代数中的知识: 将数组中的元素交换一次两个元素的位置, 逆序对的总数的奇偶性发生变化
*/


// 方法一: 暴力解法
int ReversePairs_Brute_Force(int* arr, int arrSize)
{
    int cnt=0;
    int i=0, j=0;
    for(; i<arrSize; i++)
        for(j=i+1; j<arrSize; j++)
            if(arr[i]>arr[j])
                cnt++;
    return cnt;
}



/*----------------------------------------------------------*/
// 方法二: 分治算法
// 时间复杂度: O(n*logn)
int CrossSubArray_ReversePairs(int left, int mid, int right, int* arr)
{
    // 跨子数组逆序数计数
    int i=left, j=mid+1;
    int* tmp=(int*)malloc(sizeof(int)*(right-left+1));
    int top=-1;
    int cnt_reverse_pairs=0; // 统计跨子数组逆序

    /*
        以下是在通过双指针法, 一边统计这两个有序子数组的跨数组逆序数, 
        一边把子数组变得有序, 为更长的数组统计逆序数做准备
        该部分时间复杂度:O(n)
    */
    while(i<=mid && j<=right)
    {
        if(arr[i]> arr[j])
        {
            tmp[++top]=arr[j];
            cnt_reverse_pairs+=mid-i+1, j++;
        }
        else
        {
            tmp[++top]=arr[i];
            i++;
        }
    }
    if(i>mid)
    {
        for(; j<=right; j++)
            tmp[++top]=arr[j];
    }
    else
    {
        for(; i<=mid; i++)
            tmp[++top]=arr[i];
    }
    for(int k=0; k<=top; k++)
        arr[k+left]=tmp[k];
    return cnt_reverse_pairs;
    
    /*
        注:若题目条件改成 逆序对的如下定义:
        X(i,j)=1 iff i<j and arr[i]>3*arr[j], 
        则需要先对两个子数组利用双指针的方式算一次跨子数组的逆序数(判定标准 arrr[i]>3*arr[j] 或 arr[i]<=3*arr[j])
        再对于整个数组进行双指针排序(判定标准 arr[i]>arr[j] 或 arr[i]<=arr[j]).
    
        如果不像上面说的这样, 而只是单纯将上述代码中的判别条件改为 arr[i]<3*arr[j] && arr[i]>=3*arr[j]
        则会造成排序错误.
        就比如, arr[i]=4, arr[j]=2, 理论上排序时应该 arr[j]=2 在前, arr[i]=4 在后, 
        但是由于 arr[i]<3*arr[j], 则会 arr[i]=4 在前, arr[j]=2 在后, 从而排序错误, 造成最终结果错误
    */
}

int SubArray_ReversePairs(int left, int right, int* arr)
{
    // 数组的逆序数=左半部分子数组逆序数+右半部分子数组逆序数+跨两个子数组逆序数
    if(left<right)
    {
        int mid=(left+right)/2;
        int cnt_left=SubArray_ReversePairs(left, mid, arr);
        int cnt_right=SubArray_ReversePairs(mid+1, right, arr);
        int cnt_cross=CrossSubArray_ReversePairs(left, mid, right, arr);
        int cnt_total=cnt_left+cnt_right+cnt_cross;
        return cnt_total;
    }
    else
        return 0; //递归终止条件, 子数组只有一个元素, 此时逆序数为 0

}

int ReversePairs_Divide_and_Conquer(int* arr, int arrSize)
{
    //做在最外层的一个借口, 只是为了传参时形式美观
    return SubArray_ReversePairs(0, arrSize-1, arr);
}

/*----------------------------------------------------------*/
// 以下是使用样例
int main()
{
    int arr[]={9, 7, 5, 4, 6};
    int size=sizeof(arr)/sizeof(int);

    int ReversePair_cnt1=ReversePairs_Brute_Force(arr, size);
    printf("%d\n", ReversePair_cnt1); 

    int ReversePair_cnt2=ReversePairs_Divide_and_Conquer(arr, size);
    printf("%d\n", ReversePair_cnt2);
    /* 
    注: 方法二会对原数组顺序造成改变, 后续步骤进行时, 应考虑方法二带来的影响
    */
}