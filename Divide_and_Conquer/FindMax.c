#include <stdio.h>
#include <stdlib.h>
#define max(a, b) (((a)>(b))?(a):(b))

int Divide_and_Conquer(int left, int right, int* arr)
{
    if(left<right)
    {
        int mid=(left+right)/2;
        int left_max=Divide_and_Conquer(left, mid, arr);
        int right_max=Divide_and_Conquer(mid+1, right, arr);
        return max(left_max, max(right_max, arr[mid]));
    }
    else //left==right
        return arr[left];
}

int FindMax(int* arr, int arrSize)
{
    return Divide_and_Conquer(0, arrSize-1, arr);
    /*
        复杂度:T(n)=2T(n/2)+O(1), T(n)=O(n)
        复杂度和线性搜索时, 寻找最大一致
    */
}

int main()
{
    int arr[]={9, 3, 4, 1, 2, 10, 5, 6};
    int size=sizeof(arr)/sizeof(int);
    int maxnum=FindMax(arr, size);
    printf("%d", maxnum);
}