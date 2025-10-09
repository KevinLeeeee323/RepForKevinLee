#include <stdio.h>
#include <stdlib.h>
#include <time.h> // 为了设置随机数从而使用随机数主元而调用

#define MIN -2147483648 //INT32_MIN

/*
    次序选择问题: 如何找出无序数组中的第 K 小元素?(K≥1)

    方法一: 
    - 进行升序排序, 选出第 K 个元素, 就是第 K 小的
    - 考虑选用归并排序 or 快速排序, 时间复杂度 O(N*logN)

    方法二:
    K==2 时的一个特例:锦标赛算法, 可自行了解


    方法三: 借鉴了快速排序中, 通过固定元素进行划分的想法
    快速排序中的[划分]思想:
        选择一个主元, 使得主元左侧元素小于主元, 右侧大于主元.
    那么, 如果此时主元的下标==k, 那么主元恰为第 k 小元素.
    如果主元下标 p>k, 那么在主元左侧序列中递归查找即可;
    如果主元下标 p<k, 那么在主元左侧序列中递归查找即可.
    (只是递归查找时, 查找的为子数组第 k'小元素, 不一定 k'=k, 而是满足特定位置关系)
    具体的数量关系, 参见https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=15中网课3.3.1/12:20 左右
    这样查找下去, 一定可以找到. 找到就返回.
    不同于一般分支方法遵循"问题拆分成子问题-合并子问题的解"的方法, 方法三不需要"合并"这一步
*/

/*------------------------------------------*/
// 方法一: 先排序, 再找出第k小
int compare(const void* a, const void* b) 
{
    int val_a=*(int*)a;
    int val_b=*(int*)b;
    return val_a-val_b;
}

int Kth_Min_Sort(int k, int* arr, int arrSize)
{   
    if(k<1 || k>arrSize) // 排除不可能存在的情况
    {
        printf("index out of array!");
        return MIN;
    }
    qsort(arr, arrSize, sizeof(int), compare);
    return arr[k-1];
}

/*---------------------------------------------*/
// 方法二: 针对 k==2 时的特殊情况, 锦标赛算法, 可自行了解



/*---------------------------------------------*/
// 方法三
void swap(int* a, int* b)
{
    int tmp=*a;
    *a=*b;
    *b=tmp;
}

int FixedPivotPartition(int left, int right, int* arr)
{
    int i=left-1;
    int j=left;
    int pivot=arr[right]; //固定主元, 为当前子数组最后一个元素 arr[right]
    for(; j<right; j++)
    {
        if(arr[j]<pivot)
        {
            swap(&arr[j], &arr[i+1]);
            i++;
        }
    }
    swap(&arr[i+1], &arr[right]);
    return i+1;
}

// int RandomizedPivotPartition(int left, int right, int* arr) // 随机选择主元时的划分方法
// {
//     int random_pivot=rand() % (right - left + 1) + left;
//     /*
//         rand() 函数默认生成 0 ~ RAND_MAX(<stdlib.h> 定义的常量, 通常为 32767, 即 16 位整数最大值) 之间的整数
//         要生成 下标为[left, right]（包含边界）的之间的随机整数作为主元下标，需两步：
//         生成 0 ~ (right - left) 范围内的随机数；
//         加上 left，将范围偏移到 [left, right]
//     */

//     // printf("%d ", random_pivot);
//     swap(&arr[right], &arr[random_pivot]);
//     return FixedPivotPartition(left, right, arr); //将随机主元调换到当前子数组的最后一个元素, 然后方法同固定主元时的划分方法
// }

int Divide_and_Conquer(int left, int right, int k, int* arr)
{
    if(k<1 || k>right-left+1) // 排除不可能存在的情况
    {
        printf("index out of array!");
        return MIN;
    }

    int pivot_pos=FixedPivotPartition(left, right, arr);
    // int pivot_pos=RandomizedPivotPartition(left, right, arr); //如果是随机数主元划分, 使用这个, 注释掉上一行, 并且引用#include <time.h>, 下面使用srand()函数
    int ans=pivot_pos-left+1; //主元是当前数组第 ans 小的元素
    if(ans==k)
        return arr[pivot_pos];
    else if(k<ans)
        return Divide_and_Conquer(left, pivot_pos-1, k, arr);
    else // k>ans
        return Divide_and_Conquer(pivot_pos+1, right, k-ans, arr);

    /*
        注意这个代码的分治结构和"最大子数组问题", "逆序和"等不一样, 不需要合并左右两部分, 而是从左右两部分中选出一个继续进行下去.
        有趣的一点是, 传统分治算法的递归都需要截止条件(base case), 比如"最大子数组问题"中 left<right 进行递归求解, left==right 得到基本情况(base case).
        但在本问题中, 不需要考虑这种情况.以 k<ans 的情况为例:
        当 k<ans, 有 1≤k<ans, 即 ans≥2.
        此时下标范围 [left, pivot_pos-1]=[left, left+ans-2](通过ans=pivot_pos-left+1代换得到)
        该下标范围内, 元素个数为 ans-1, 由 ans>k 知 ans-1≥k, 因此一定能够从中选出第 k 小的元素

        k>ans 情况同理.
    */
}

int Kth_Min_FixedPivotPartition(int k, int* arr, int arrSize) //只是套了一层壳, 让函数接口尽可能统一
{
    return Divide_and_Conquer(0, arrSize-1, k, arr);
    /*
        和固定主元划分的快速排序一样, 算法时间复杂度无法确切估计.
        最好情况, 一次就找到 ans==k, 仅完成一次固定主元的划分, 复杂的 O(n)
        最坏情况, 复杂度 O(n^2), 见https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=15 的18:06

        为了规避复杂度最高的情况, 仍然可以使用[随机主元划分]的方法.
        最终算出期望复杂度为O(n)
    */
}

/*-----------------------------------------*/
int main()
{
    int arr[]={17, 13, 14, 4, 8, 18, 22, 52, 40, 24, 48, 28, 47, 21, 42, 37};
    int size=sizeof(arr)/sizeof(int);
    int k=0;


    // printf("%d", Kth_Min_Sort(k, arr, size)); 
    // 数组 arr 中的第k=8小元素为22.
    // 不要在测试完方法一后接连测试其他方法, 因为方法一已经对其进行重新排序, 无法验证后续代码的正确性

    printf("%d", Kth_Min_FixedPivotPartition(k, arr, size));
    // 如果想要求第 k 大元素, 只需调用 Kth_Min_FixedPivotPartition(size+1-k, arr, size);
}