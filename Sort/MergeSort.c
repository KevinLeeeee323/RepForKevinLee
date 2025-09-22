#include <stdio.h>
#include <stdlib.h>

void Merge(int left, int mid, int right, int* arr)
{
    // 将两个子数组 A 和 B, 合并成有序数组
    int* tem=(int*)malloc(sizeof(int)*(right-left+1)); // 临时存储
    int top=-1;
    int i=left, j=mid+1;
    while(i<=mid && j<=right)
    {
        if(arr[i]<arr[j])
        {
            tem[++top]=arr[i];
            i++;
        }
        else
        {
            tem[++top]=arr[j];
            j++;
        }
    }
    if(i>mid)
    {
        for(; j<=right; j++)
            tem[++top]=arr[j];
    }
    else
    {
        for(; i<=mid; i++)
            tem[++top]=arr[i];
    }
    for(int k=0; k<=top; k++)
        arr[left+k]=tem[k];
    free(tem);
}

void MergeSort(int left, int right, int* arr)
{
    if(left<right)
    {
        int mid=(left+right)/2;
        MergeSort(left, mid, arr); //递归处理左侧子数组A
        MergeSort(mid+1, right, arr); //递归处理右侧子数组B
        Merge(left, mid, right, arr); //有序合并数组A和B
    }
}


// 以下是运行实例
int main()
{
    int arr[]={7, 6, 5, 3, 1, 8, 4, 12, 0, 9};
    int size=sizeof(arr)/sizeof(int);
    MergeSort(0, size, arr);
    for(int i=0; i<size; i++)
        printf("%d ", arr[i]);
}