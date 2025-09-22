#include <stdio.h>
#include <stdlib.h>
/*
    要解决的问题: 计算最大(子数组元素之和), 并且输出此时的子数组首尾元素下标.
    子数组是指原数组中连续的一部分, 元素个数 ≥ 1

    以下有三个方法:
    - 暴力枚举法
    - 暴力枚举法改进版
    - 分治算法
*/
int MaxSubArray_Brute_Force(int* arr, int arrSize, int* i_save, int* j_save)
{
    // 暴力枚举法, 三层 for 循环, 时间复杂度 O(n^3)
    int max_val=arr[0]-1; //设置一个初始值, 这个值在答案的可能范围中
    int ans=0;
    for(int i=0; i<arrSize; i++)
    {
        for(int j=i; j<arrSize; j++)
        {
            ans=0;
            for(int k=i; k<=j; k++)
                ans+=arr[k];
            if(ans>max_val)
            {
                max_val=ans;
                *i_save=i;
                *j_save=j;
            }
        }
    }
    return max_val;
}

/*---------------------------------------------------*/

int MaxSubArray_Brute_Force_Modified(int* arr, int arrSize, int* i_save, int* j_save)
{
    // 在暴力枚举法基础上修改得到, 时间复杂度由 O(n^3) 变为 O(n^2)
    int max_val=arr[0]-1; 
    /*
    设置一个初始值, 这个值在答案的可能范围中, 
    且一定让下面的 max_val 更新一次, 防止那种数组只有一个元素的情况
    */
    int ans=0;
    for(int i=0; i<arrSize; i++)
    {
        ans=0;
        for(int j=i; j<arrSize; j++)
        {
            ans+=arr[j];
            if(ans>max_val)
            {
                max_val=ans;
                *i_save=i;
                *j_save=j;
            }
        }
    }
    return max_val;
}

/*---------------------------------------------------*/
#define max(a, b) (((a)>(b))?(a):(b))

int CrossSubArray(int left, int mid, int right, int* arr, int* i_save, int* j_save)
{
    /*
    统计跨越左右两部分子数组的最大子数组
    */
    int max_left=arr[mid];
    int ans=0;
    int i=mid;
    for(; i>=left; i--)
    {
        ans+=arr[i];
        if(ans>max_left)
        {
            max_left=ans;
            *i_save=i;
        }
    }
    
    int max_right=arr[mid+1];
    ans=0;
    int j=mid+1;
    for(; j<=right; j++)
    {   
        ans+=arr[j];
        if(ans>max_right)
        {
            max_right=ans;
            *j_save=j;
        }
    }

    return max_left+max_right;
}

int Divide_and_Conquer(int left, int right, int* arr, int* i_save, int* j_save)
{
    if(left<right)
    {
        int i_left=-1, j_left=-1;
        int i_right=-1, j_right=-1;
        int i_cross=-1, j_cross=-1;
        int mid=(left+right)/2;
        int left_max=Divide_and_Conquer(left, mid, arr, &i_left, &j_left);
        int right_max=Divide_and_Conquer(mid+1, right, arr, &i_right, &j_right);
        int cross_max=CrossSubArray(left, mid, right, arr, &i_cross, &j_cross);
        int max_subArray=max(max(left_max, right_max), cross_max);
        if(max_subArray==left_max)
            *i_save=i_left, *j_save=j_left;    
        else if(max_subArray==right_max)
            *i_save=i_right, *j_save=j_right;
        else
            *i_save=i_cross, *j_save=j_cross;
        return max_subArray;

    }
    else //(left==right)
    {
        *i_save=left;
        *j_save=right;
        return arr[left];
    }
}


int MaxSubArray_Divide_and_Conquer(int* arr, int arrSize, int* i_save, int* j_save)
{
    return Divide_and_Conquer(0, arrSize-1, arr, i_save, j_save); 
    //实际 Divide_and_Conquer 函数是主体, 放到这里面只是为了保证这三个方法于参数形式上相对统一
}


/*---------------------------------------------------*/

// 以下是使用实例
int main()
{
    int arr[]={-2,1,-3,4,-1,2,1,-5,4};
    int size=sizeof(arr)/sizeof(int);
    int i_save=-1, j_save=-1;

    //暴力枚举
    int max1=MaxSubArray_Brute_Force(arr, size, &i_save, &j_save);
    printf("%d %d %d\n", max1, i_save, j_save);
    
    //暴力枚举改良版
    int max2=MaxSubArray_Brute_Force_Modified(arr, size, &i_save, &j_save);
    printf("%d %d %d\n", max2, i_save, j_save);

    //分治算法
    int max3=MaxSubArray_Divide_and_Conquer(arr, size, &i_save, &j_save);
    printf("%d %d %d\n", max3, i_save, j_save);
}