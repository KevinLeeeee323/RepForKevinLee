#include <stdio.h>
#include <stdlib.h>

int GroupXor(int* arr, int arrSize)
{
    int xor_sum=0;
    for(int i=0; i<arrSize; i++)
        xor_sum^=arr[i];
    return xor_sum;
}

int main()
{
    /*
        贪心算法, 在这里或者叫脑筋急转弯更合适.

        补充几个知识点:
        1. 异或的运算律: C语言中, 异或的符号是 a^b
           a^b^c=(a^b)^c=a^(b^c)=(a^c)^b, 满足交换律和结合律.
           a^b^c 称为 a, b, c 的异或和.

        2. 任意正整数 X, Y, X + Y >= X Xor Y.
           当且仅当x 和 y 没有同时为 1 的二进制位，即 “无进位加法”时成立.

        基于以上, 对于三个数 a, b, c, 我们可以知道:
        a+b+c >= a+(b^c) >= a^(b^c) = a^b^c,
        也就是说, 这几个数之间的加法次数越少, 异或次数越多, 理论上这组数的权值越小.
        
        权值: 各组的异或和加起来. 比如 a+(b^c), 相当于 b 和 c 一组, a 另外一组.

        对多于三个数的情况, 也是适用的.

        所以, 为了让权值最小, 那就让所有数分到同一组, 这样最终的权值就是所有数的异或和.
    */
   
    int n=0;
    scanf("%d", &n);
    int* save_arr=(int*)calloc(n, sizeof(int));
    for(int i=0; i<n; i++)
        scanf("%d", &save_arr[i]);
    int ans=GroupXor(save_arr, n);
    printf("%d", ans);
}