#include <stdio.h>
#include <stdlib.h>

/*
    计算组合数.
    使用 C(n, k)=n!/(k! * (n-k)!) 公式计算, 会导致超 long long 范围, 难以存储
    利用记忆化搜索, 使用公式 :
    C(n, k)=1,  k==n or k==0
    C(n, k)=C(n-1, k-1)+C(n-1, k), 0<k<n
    但该方法在 n 较大的时候仍然会超过 long long 可以表示的范围值.
*/

long long** Combine(int n)
{
    long long** com_save=(long long**)malloc(sizeof(long long*)*(n+1));
    com_save[0]=(long long*)malloc(sizeof(long long)*1);
    com_save[0][0]=1;
    com_save[1]=(long long*)malloc(sizeof(long long)*2);
    com_save[1][0]=1;
    com_save[1][1]=1;
    int j=0;
    for(int i=2; i<=n; i++)
    {
        com_save[i]=(long long*)calloc(i+1, sizeof(long long));
        com_save[i][0]=1;
        for(j=1; j<=i; j++)
        {
            if(j>i/2)
                    com_save[i][j]=com_save[i][i-j];
            else
                com_save[i][j]=com_save[i-1][j-1]+com_save[i-1][j];
        }
    }
    return com_save;
}

/*
    另一种计算方法, 利用公式:
    C(n, m)=n!/(m! * (n-m)!)=[n*(n-1)*...(n-m+1)]/[m*(m-1)*...1]
*/
int CombineNumber(int n, int m) // 计算组合数 C_n^m
{
    if(m>n)
    {
        printf("%d is bigger than %d therefore C(%d, %d) is illegal\n", m, n, n, m);
        return -1;
    }
    long long ans = 1;
    
    for (int x=n-m+1, y=1; y<=m; x++, y++)
        ans*=x/y;
    return ans;
}

int main()
{
    int n=40;
    long long** save=Combine(n);
    for(int i=0; i<=n; i++)
    {
        for(int j=0; j<=i; j++)
            printf("%lld ", save[i][j]);
        printf("\n");
    }

    long long ans=CombineNumber(9, 4);
    printf("%lld", ans);
}