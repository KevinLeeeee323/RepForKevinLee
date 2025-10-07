#include <stdio.h>
#include <stdlib.h>
// #include <time.h> // 为了设置随机数从而使用随机数主元而调用

void swap(int* a, int* b)
{
    int tmp=*a;
    *a=*b;
    *b=tmp;
}

int FixedPivotPartition(int left, int right, int* arr) //固定主元时的划分方法
{
    /*
        该部分叫做划分. 此处是通过固定的主元(当前数组部分的最后一个元素)将子数组划分成两部分:
        左侧元素<主元, 右侧元素>=主元

        具体实现方式:
        维护两个指针i, j, 其中
        j 指向当前检查的元素,
        i 是当前检查过的元素中, 数值<主元的最后一个元素的下标, 这一部分称为A. 

        也就是说, 下标介于[i+1, j-1]之间的元素是当前检查过的元素中, 数值>=等于主元的, 这一部分称为B.

        维护方式如下:
        当遍历到下标为j的数组元素时, 
            如果其数值<主元, 那就应该将当前元素添加到"小于主元的部分", 
            具体做法为:
                交换arr[i+1]与arr[j], 使之加入到A中;
                更新A的长度, 即i++;
                j++, 遍历下一个元素;

            如果其数值<主元, 那就应该将当前元素添加到"小于主元的部分", 
                但此时显然不需要移动, 就可以使之处在B中.
                j++, 遍历下一个元素;


        等到遍历完当前子数组中所有元素(不包含主元本身), 
        将下标为i+1的元素和主元交换, 就可以得到一个"相对有序"的子数列:
        主元左边的元素都比主元小, 右边的>=主元.

        此时返回主元的下标(i+1), 方便后面以主元为界, 两侧分治

        具体例子可以看 https://www.bilibili.com/video/BV1TC4y1W7wC/?spm_id_from=333.1391.0.0&p=13&vd_source=c8e4e809f91f46885a44be8339a7976c
        时长从5:40左右开始

        复杂度:O(N), 因为是逐个遍历这个长度为N的子数组
    */
    int i=left-1;
    int j=left;

    int pivot=arr[right]; //主元
    for(; j<right; j++)
    {
        if(arr[j]<pivot)
        {
            swap(&arr[j], &arr[i+1]);
            i++;
        }
    }
    swap(&arr[right], &arr[i+1]);
    // printf("%d ", i+1);
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

//     printf("%d ", random_pivot);
//     swap(&arr[right], &arr[random_pivot]);
//     return FixedPivotPartition(left, right, arr); //将随机主元调换到当前子数组的最后一个元素, 然后方法同固定主元时的划分方法
// }

/*
    复杂度分析：
    取决于每次划分主元后,主元的位置.
    如果每次主元都在正中间, 那么 T(n)=2*T(n/2)+O(n), 从而 T(n)=O(n*logn), 这是最好情况
    如果每次主元都在最左侧/每次都在最右侧, 那么 T(n)=T(n-1)+O(n), 从而 T(n)=O(n^2), 这是最坏情况
    最坏情况从何而来?主元特别小 or 特别大
    为了避免每次主元都在最左侧/最右侧, 可以随机选择主元, 从而避免这一情况的发生
    可以证明, 在这种随机选择主元的方式下, 期望时间复杂度为 O(n*logn)
*/

void Divide_and_Conquer(int left, int right, int* arr)
{
    if(left<right)
    {
        int pivot_pos=FixedPivotPartition(left, right, arr); //主元位置下标
        // int pivot_pos=RandomizedPivotPartition(left, right, arr); //如果是随机数主元划分, 使用这个, 注释掉上一行, 并且引用#include <time.h>, 下面使用srand()函数

        Divide_and_Conquer(left, pivot_pos-1, arr); //主元左侧进行划分
        Divide_and_Conquer(pivot_pos+1, right, arr); //住院右侧进行划分

        /*
        和归并排序一样, 快速排序也实现了左侧子数组和右侧子数组都局部有序.
        但不同的是, 快速排序引入了主元机制, 从而使得主元放在左侧子数组和右侧子数组之间, 主元大于左侧元素, 小于右侧元素,
        也就使得数组全局有序, 从而不需要像归并排序那样合并.
        */
    }
}

void QuickSort(int* arr, int arrSize) //套的一层接口, 形式上更好
{
    // srand((unsigned int)time(NULL)); // 随机数主元划分法需要使用这个函数
    /*
        rand() 是 “伪随机数生成器”，需通过 srand(seed) 设置初始种子。
        若不设置种子，rand() 会默认使用种子 1，导致每次运行程序生成完全相同的随机序列,
        例如每次都输出 12, 15, 18, 10, 19
        
        这里调用time, 是利用系统时间生成动态种子. (记得引用<time.h>)
    */
    Divide_and_Conquer(0, arrSize-1, arr); 
}

int main()
{
    int arr[]={8, 7, 2, 1, 5, 4, 7, 9, 10};
    int len=sizeof(arr)/sizeof(int);
    QuickSort(arr, len);
    printf("\n");
    for(int i=0; i<len; i++)
        printf("%d ", arr[i]);
}