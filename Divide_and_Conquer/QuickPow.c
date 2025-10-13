#include <stdio.h>
#include <stdlib.h>

/*
    Task1: 求幂
    给定任意实数 x, 整数 n, 求 x^n
    
    方法1: 暴力解法:for 循环 n 次求 x^n, 时间复杂度 O(n)

    方法2: 分治, 通过 x^(n/2)和 x^n 关系构建递推式: T(n)=T(n/2)+O(1)
        根据主定理, T(n)=O(log(n))
*/

double Pow_Divide_and_Conquer(double x, int n)
{
    if(n==1)
        return x; // 递归终止条件
    double half=Pow_Divide_and_Conquer(x, n/2);
    double ans=half*half;
    if(n%2==0)
        return ans;
    else
        return ans*x;
}

/*------------------------Test Case---------------------*/
int main()
{
    printf("%lf", Pow_Divide_and_Conquer(3.1, 2));
}

