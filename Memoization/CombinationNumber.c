#include <stdio.h>
#include <stdlib.h>

/*
    计算组合数.
    使用 C(n, k)=n!/(k! * (n-k)!) 公式计算, 会导致超 long long 范围, 难以存储
    利用记忆化搜索, 使用公式 :
    C(n, k)=1,  k==n or k==0
    C(n, k)=C(n-1, k-1)+C(n-1, k), 0<k<n
    
*/

int** Combine(int n)
{
    int** com_save=(int**)malloc(sizeof(int*)*(n+1));
    com_save[0]=(int*)malloc(sizeof(int)*1);
    com_save[0][0]=1;
    com_save[1]=(int*)malloc(sizeof(int)*2);
    com_save[1][0]=1;
    com_save[1][1]=1;
    int j=0;
    for(int i=2; i<=n; i++)
    {
        com_save[i]=(int*)calloc(i+1, sizeof(int));
        for(j=0; j<=i; j++)
        {
            if(j==0 || j==i)
                com_save[i][j]=1;
            else
                com_save[i][j]=(com_save[i-1][j-1]+com_save[i-1][j]);
        }
    }
    return com_save;
}

int main()
{
    int n=20;
    int** save=Combine(n);
    for(int i=0; i<=n; i++)
    {
        for(int j=0; j<=i; j++)
            printf("%d ", save[i][j]);
        printf("\n");
    }
}