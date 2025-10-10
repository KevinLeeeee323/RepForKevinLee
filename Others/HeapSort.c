#include <stdio.h>
#include <stdlib.h>
#define MIN -2147483648 //INT32_MIN

/*
    什么是堆排序?怎么做?
    - 什么是大顶堆
        - 先做一些假设:数组索引起始为 0, 且下列所说的左右节点, 不超过索引范围(尤其注意不超过索引上界)
        - 对于一个数组, 对于下标为 id 的节点, 下标为2*id+1的节点是其左子节点, 2*id+2 的节点是其右子节点.(左右节点索引如果不超过索引上限存在的话)
          按照这样原则构建成一棵二叉树, 这样的数据结构称为堆.
        - 对于没有左子节点且没有右子节点的下标为id 的节点, 我们称之为叶节点.
        - 当然, 并没有真的去构建一棵二叉树, 而是说, 后续的操作都是基于上述的左右节点和根节点的关系, 通过堆的方式去操作.
        - 大顶堆是在堆的基础上, 满足:任意 i 在索引范围内且 i 不是叶节点, a[i]>=a[2*i+1], 且 a[i]>=a[2*i+2](如果右节点存在的话)
    - 如何利用一个大顶堆完成升序排序? 
        - 根据上述大顶堆的特性, 如果将一个数组(下标范围 0 ~ arrSize-1)构建成大顶堆, 一定满足 arr[0]是数组最大元素.
        - 大致思路就是, 每次把最大的元素交换到数组末尾 arr[end], 然后把下标为 0 ~ end-1的元素再次构建大顶堆.
        - 这样循环多次, 一定可以满足都把当前数组的最大元素放到数组末尾.多次之后, 可以保证数组升序.
    - 具体实现? heapSort()函数由如下几个部分实现:
        - swap()函数负责完成交换.
        - buildHeap()函数负责建堆, 会调用很多次 adjustHeap()函数.这些调用在遵从一定顺序(从下到上, id 从大到小)的情况下, 可以构建成大顶堆.
        - adjustHeap()函数能够把以 id 为根节点的二叉树调整成大顶堆
    - 堆排序还可以实现选择排序--选出第 K 大的元素?见下面 FindKthMax_heapSort 函数
*/

void swap(int* a, int* b)
{
    int tmp=*a;
    *a=*b;
    *b=tmp;
}

void adjustHeap(int id, int right, int* arr) //将以 id 为根节点的二叉树调整成大顶堆
{
    /*
        适用前提:
        以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树都已经分别是大顶堆了.
        只是 id , 2*id+1, 2*id+2 的大小顺序可能还需要调整.
        由于调整后可能使得以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树不满足大顶堆特性,
        因此需要借助这个 while 循环, 递归的调整.
    */
    int child_id=2*id+1; //左子节点
    int max_id=child_id; // 记录左右节点中数值最大的节点的下标
    while(child_id<=right)
    {
        if(child_id+1<=right && arr[child_id+1]>arr[child_id]) // 如果右子节点存在且数值>左子节点
            max_id++; //max_id=2*id+2, 代表右子节点
        if(arr[id]<arr[max_id])
        {
            swap(&arr[id], &arr[max_id]);
            id=max_id; // 处理调整后可能破坏"以 max_id 为下标的根节点的二叉树是一个大顶堆"的性质
            child_id=2*id+1; // 更新左右子节点信息
            max_id=child_id;
        }
        else
            break;
    }
}

void buildHeap(int left, int right, int* arr) //构建堆
{
    for(int i=(right-1)/2; i>=left; i--)
        adjustHeap(i, right, arr);
    // (right-1)/2 可以求出当前有子节点的最大节点下标
    // 通过 i-- 的方式调用, 可以保证adjustHeap的适用前提:"以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树都已经分别是大顶堆了"
}

void heapSort(int* arr, int arrSize)
{
    buildHeap(0, arrSize-1, arr);
    for(int i=1; i<arrSize; i++)
    {
        swap(&arr[0], &arr[arrSize-i]);
        adjustHeap(0, arrSize-i-1, arr);
        /*
            这里按道理说要重新构建大顶堆, 需要调用buildHeap(0, arrSize-i-1, arr);
            但实际上调用 adjustHeap()就可以满足需要.
            经过上一行的 swap()后, 以 2*0+1和 2*0+2 为根节点的二叉树都仍然是大顶堆. 但 0, 1, 2 三个节点上数值的大小关系不定.
            只需要针对 id=0的节点调整就可以, 符合 adjustHeap()使用条件.
        */ 
    }
    // 时间复杂度:O(n*logn)
}

/*----------------------------------------------------------*/
/*
    堆排序的另一个妙用:可以求数组中第 K 大的元素.(arrSize>=K>=1)
    通过利用堆排序下面的特性可以实现:
        堆排序每次做完一次 swap()+adjustHeap(), 都会把当前数组中最大元素放到数组最后一个位置.
    可实现如下:
*/
int FindKthMax_heapSort(int k_th_max, int* arr, int arrSize)
{
    if(k_th_max<1 || k_th_max>arrSize)
    {
        printf("index out of array!");
        return MIN;
    }
    buildHeap(0, arrSize-1, arr);
    for(int i=1; i<k_th_max; i++) //只需要构建堆 k_th_max 次就可以 (for 循环 k_th_max-1 次, 加上上面一行, 正好 k_th_max 次)
    {
        swap(&arr[0], &arr[arrSize-i]);
        adjustHeap(0, arrSize-i-1, arr);
    }
    return arr[0]; //自己手算一下, 实际是返回 arr[0], 因为到了 i=k_th_max-1后, 不会再进入下一次循环, 也就不会 swap 到末尾
}

/*----------------------------------------------------------*/
void print(int* arr, int arrSize)
{
    for(int i=0; i<arrSize; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main()
{
    int arr[]={50, 7, 1, 3, 2, 8, 10, 6};
    int size=sizeof(arr)/sizeof(int);
    heapSort(arr, size);
    print(arr, size);  

    int* arr_copy=(int*)malloc(sizeof(int)*size);
    for(int i=0; i<size; i++)
        arr_copy[i]=arr[i];
    int k=3;
    printf("%dth max: %d", k, FindKthMax_heapSort(k, arr_copy, size));
}