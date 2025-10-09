#include <stdio.h>
#include <stdlib.h>
#define MIN -2147483648 //INT32_MIN
#define NumPerGroup 5

/* 
    中位数算法求解次序选择问题:找出数组中第 k 小的元素, k>=1
    该算法的本质和 SelectionProblem.c 中的分治选择算法一样, 都是基于 QuickSort 的主元划分思想, 
    选出主元然后分治解决问题.
    但这里和分治选择算法不一样的就是如何选择主元.
    中位数算法可以保证，无论输入数据是什么样的，每次划分后，
    主元都能将数组大致分为相等的两部分（至少有 30% 的元素小于等于主元，也至少有 30% 的元素大于等于主元）
    这种 “有保证” 的划分比例，使得算法的时间复杂度在最坏情况下也是 O(n)

    中位数的中位数算法可以看作是快速选择算法的一个"加强版",
    它通过牺牲一点实现的简单性和常数时间开销，换取了一个在任何情况下都稳定的线性时间复杂度保证
*/

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int compare(const void* a, const void* b)
{
    return *(int*)a-*(int*)b;
}

int findMedianOfMedians(int* arr, int left, int right)
{
    /*
    在 arr[left...right] 范围内, 将数组中元素五个一组划分成若干组,
    每个组求出中位数
    然后返回这些中位数的中位数
    */

    // 特殊情况(数组中元素少于 5 个)
    int size = right - left + 1;
    if (size <= NumPerGroup)
    {
        qsort(&arr[left], size, sizeof(int), compare);
        return arr[left + size / 2];
    }

    // 确定组数
    int numGroups = size / NumPerGroup;
    int remainder = size % NumPerGroup;
    if(remainder>0)
        numGroups++;
    int* medians=(int*)calloc(numGroups, sizeof(int));
    
    // 分组找到每组的中位数
    int groupStart=0, groupEnd=0;
    for (int i = 0; i < numGroups-1; i++) 
    {
        groupStart = left + i * NumPerGroup;
        qsort(&arr[groupStart], NumPerGroup, sizeof(int), compare);
        medians[i] = arr[groupStart + 2]; // 每组的中位数
    }
    
    // 处理最后一组
    groupStart = left + (numGroups-1) * NumPerGroup;
    int num=right-groupStart+1;
    qsort(&arr[groupStart], num, sizeof(int), compare);
    medians[numGroups-1] = arr[groupStart + num/2];

    // 找到这些中位数的中位数
    qsort(medians, numGroups, sizeof(int), compare);
    int ans=medians[numGroups/2];
    free(medians);
    return ans;
}

/**
 * @brief 分区函数
 *
 * @param arr 数组
 * @param left 起始索引
 * @param right 结束索引
 * @param pivotValue 用于划分的基准值
 * @return int 基准值最终所在的索引
 */
int partition(int* arr, int left, int right, int pivotValue)
{
    // 先将基准值交换到数组末尾，方便处理
    for (int i = left; i <= right; i++)
    {
        if (arr[i] == pivotValue)
        {
            swap(&arr[i], &arr[right]);
            break;
        }
    }
    int pivot_pos = right;
    int pivot = arr[right];
    int i = left - 1; // i 是小于等于区的边界

    for (int j = left; j < right; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    // 将基准值放到它最终的位置
    swap(&arr[i + 1], &arr[pivot_pos]);
    return i + 1;
}

/**
 * @brief 中位数的中位数算法，寻找第 k 小的元素 (k 是 0-based 索引)
 *
 * @param arr 数组
 * @param left 起始索引
 * @param right 结束索引
 * @param k 要找的元素的 0-based 排名 (0 代表最小，n-1 代表最大)
 * @return int 第 k 小的元素的值
 */
int medianOfMedians(int left, int right, int k, int* arr)
{
    if (left == right)
        return arr[left]; // 基本情况：只有一个元素

    int pivotValue = findMedianOfMedians(arr, left, right); // 选择基准：找到中位数的中位数    
    int pivot_pos = partition(arr, left, right, pivotValue); // 划分：根据基准值分区

    int ans=pivot_pos-left+1;
    if (k == ans)
        return arr[pivot_pos];  // 找到了:基准值的位置就是 k
    else if (k < ans)
        return medianOfMedians(left, pivot_pos - 1, k, arr); // 目标在左半部分
    else // k>ans
        return medianOfMedians(pivot_pos + 1, right, k-ans, arr); // 目标在右半部分
}

int FindKthMin(int k, int* arr, int arrSize)
{
    if(k<1 || k>arrSize)
    {
        printf("index out of array!");
        return MIN;
    }
    return medianOfMedians(0, arrSize-1, k, arr);
}

/*-----------------------------------------*/
int main()
{
    int arr[] = {12, 3, 5, 7, 4, 19, 26};
    int size = sizeof(arr) / sizeof(arr[0]);

    int arr_copy[size]; // 为避免修改原数组，创建一个副本进行操作
    for (int i = 0; i < size; i++)
        arr_copy[i] = arr[i];

    int k_th_smallest = 3;
    printf("第 %d 小的元素是: %d\n", k_th_smallest, FindKthMin(k_th_smallest, arr_copy, size)); 
    // 如果想要求第 k 大元素, 只需调用 FindKthMin(size+1-k_th_smallest, arr_copy, size)
}