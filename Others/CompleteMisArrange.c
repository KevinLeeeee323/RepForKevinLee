#include <stdio.h>
#include <stdlib.h>

/*
    现在有 n 个不同的包裹，需要寄给 n 个不同的地址，请编程求出每个包裹都送错地址的情况共有多少种。
    输出一个数字，即为种类数。为了防止数字过大的情况，请输出答案对998244353取余的结果。

    Input: 5
    Output: 44

    俗称：完全错排问题
*/

#define MAX 998244353
/*
    递归算法.
    int CompleteMisArrange(int n)
    {
        if(n==1)
            return 0;
        else if(n==2)
            return 1;
        else
            return ((n-1)*((CompleteMisArrange(n-1)%MAX + CompleteMisArrange(n-2)%MAX)%MAX))%MAX;
    }
    算法的问题:
    计算 D(n) 需要 D(n-1) 和 D(n-2)，而计算 D(n-1) 又需要 D(n-2) 和 D(n-3)。
    这导致同一个子问题（如 D(n-2)）被计算了多次
    更好的方法是使用记忆化搜索or 动态规划, 降低重复计算的次数
*/

int main()
{
    // 记忆化搜索
    int n=-1;
    scanf("%d", &n);
    long long* ans=(long long*)malloc(sizeof(long long)*(n+1));
    ans[1]=0;
    ans[2]=1;
    for(int i=3; i<=n; i++)
        ans[i]=((i-1)*((ans[i-1]%MAX + ans[i-2]%MAX)%MAX))%MAX;
    printf("%lld", ans[n]);
}