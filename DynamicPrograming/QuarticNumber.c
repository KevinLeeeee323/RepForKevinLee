#include <stdio.h>
#include <stdlib.h>

/*
    [题目描述]
        给定正整数m, n, 将 m 分解为 n 个四次方数的和的形式(k1^4 + k2^4 + ... + kn^4), 要求 n 最小, 返回此时的 n, 以及数组[k1, k2, ...kn] (可以不按顺序)
        e.g.1 当 m=706 时, 因为 706=5^4+3^4，所以有 n=2. 可以证明此时 n 最小, 同时, 返回数组:[3, 5]
        e.g.2 档 m=33 时, 因为 33=2^4+2^4+1, 所以有 n=3, 同时返回数组: [1, 2, 2]

    [数据范围] m≤10^5

    [思路]
        考虑动态规划.
        记dp[m]表示将 m 分解为 n 个四次方数的和的形式所需的最少 n.
        由于 m 的组成分解中只有 k^4 这样的数, 因此可以写出递推式:

            dp[m]=min(dp[m-k^4])+1, for k >=0 such that k^4<=m

        为了加快 dp[m-k^4]的计算, 避免每次都要算 k^4, 可以打表, 提前算出 m<=10^5 内所有的 k^4 存储起来(见 dict[] 数组)

        如何进行回溯?
            rec[i][j]统计为了用最少个数的四次方数和的形式构建i, 所需要的 j^4 的数量.
            上面会找到一个 k0, 使得, k0=argmin((dp[m-k^4])+1), 0<=k^4<=m
            代码中, crit_j 就是 k0
            rec[i]只需要在 rec[i-k0^4]的基础上稍作修改:
                rec[i]][j]=rec[i-k0^4][j], j!=k0
                rec[i][k0]=rec[i-k0^4][k0]+1
            
            这里换了一种返回数组的方式, 打印其中每个k_i 都用了多少个.
            比如 33=1^4+2^4+2^4, 返回:1个1, 2个2 这样的.

            代码写在了 QuarticNumber_DP_rec1() 里
            这样回溯的一个问题: 空间占用太大. rec 数组占据 dictNum*(m+1)个 int 空间.
        
        一种更快, 更省内存的回溯方式?
            简化 rec，只存储 “每个 i 对应的 crit_j”（推荐）
            不需要存储所有 dict[j] 的次数, 只需存储 dp[i] 对应的 crit_j(即最后一个用的四次方数索引)
            最后从 m 回溯到 0 即可生成结果(递归的去构建 i-dict[crit_j]剩下的部分)
            
            代码写在了 QuarticNumber_DP_rec2() 里
            这里的空间占用只有(m+1)个 int 空间            

    [时间复杂度分析]
        两层 for 循环嵌套. 外层 m 次, 内层最坏情况 O(dictNum), 不论哪种回溯方式, 都是如此.
        其中, dictNum 实际上受制于 m 的上界max, 为了满足 k^4<=m, 所以 dictNnum<=(向下取整(m^(1/4))+1)
        因此, 整体时间复杂度约为 O(m^(5/4))        
*/

#define max 100001
#define maxDictNum 20 // 需要大致估计一下, 只需要保证 maxDictNum^4>=max

int dict[]={0, 1, 16, 81, 256, 625, 1296, 2401, 4096, 6561, 10000, 14641, 20736, 28561, 38416, 50625, 65536, 83521};
int dictNum=sizeof(dict)/sizeof(int);
/*
// 可以实现通过打表的方式获得 dict[]. 这里 17^4=83521 < 100000 < 18^4=104976.
// 以下是一个生成 dict[]的函数:
int* genDict(int m, int* dictSize)
{
    int* ans=(int*)calloc(maxDictNum, sizeof(int));
    int i=0;
    for(; i*i*i*i<=m; i++)
        ans[i]=i*i*i*i;
    *dictSize=i;
    return ans;
}

// 然后在外部给 dict 传参:
int dictNum=0;
int* dict=genDict(max, &dictNum);

上面这两行要放到 DP 函数中, 因为C语言中全局变量（包括静态变量）的初始化需要在编译时完成.
初始化值必须是编译器可知的常量(如字面量、宏定义的常量等), 而函数调用(如 genDict(max, &dictNum))的结果是在运行时计算的, 无法用于全局变量的初始化
*/

int QuarticNumber_DP_rec1(int m, int** returnArr, int* returnSize)
{
    // 初始化
    int* dp=(int*)calloc(m+1, sizeof(int));
    int** rec=(int**)malloc(sizeof(int*)*(m+1));
    for(int i=0; i<=m; i++)
        rec[i]=(int*)calloc(dictNum, sizeof(int));
    
    int min=0, crit_j=0; // crit_j 就是上文所指的 k0
    int i=0, j=0, k=0;
    for(i=1; i<=m; i++)
    {
        min=dp[i-1], crit_j=1; //dict[1]=1 
        // min 必须得是dp[i-j^4]可能取值中的一个. 而 dp[i-1]确实是其中一个.
        for(j=2; j<dictNum && dict[j]<=i; j++) // 上一行已经涵盖了 j=1 的 dict[j], 这里从 j=2 开始
        {
            if(dp[i-dict[j]]<min)
            {
                min=dp[i-dict[j]];
                crit_j=j;
            }
        }
        for(k=0; k<dictNum; k++) // 回溯部分
        {
            if(k!=crit_j)
                rec[i][k]=rec[i-dict[crit_j]][k];
            else
                rec[i][k]=rec[i-dict[crit_j]][k]+1;
        }
        dp[i]=min+1; // 更新 dp[i]
    }

    // return and free
    int ans=dp[m];

    *returnArr=(int*)calloc(dictNum, sizeof(int));
    *returnSize=dictNum;
    for(j=0; j<dictNum; j++)
        (*returnArr)[j]=rec[m][j];
    
    for(i=0; i<=m; i++)
        free(rec[i]);
    free(rec);
    free(dp);
    
    return ans;
}

int QuarticNumber_DP_rec2(int m, int** returnArr, int* returnSize)
{
    // 初始化
    int* dp=(int*)calloc(m+1, sizeof(int));
    int* rec=(int*)calloc(m+1, sizeof(int));
    
    int min=0, crit_j=0; // crit_j 就是上文所指的 k0
    int i=0, j=0, k=0;
    for(i=1; i<=m; i++)
    {
        min=dp[i-1], crit_j=1; //dict[1]=1 
        // min 必须得是dp[i-j^4]可能取值中的一个. 而 dp[i-1]确实是其中一个.
        for(j=2; j<dictNum && dict[j]<=i; j++) // 上一行已经涵盖了 j=1 的 dict[j], 这里从 j=2 开始
        {
            if(dp[i-dict[j]]<min)
            {
                min=dp[i-dict[j]];
                crit_j=j;
            }
        }
        rec[i]=crit_j;
        dp[i]=min+1; // 更新 dp[i]
    }

    // return and free
    int ans=dp[m];

    *returnArr=(int*)calloc(dictNum, sizeof(int));
    *returnSize=ans;
    int top=-1;
    int tmp=m;
    while(tmp>0)
    {
        (*returnArr)[++top]=rec[tmp];
        tmp-=dict[rec[tmp]];
    }
    
    free(rec);
    free(dp);
    
    return ans;
}

/*--------------------Test Case--------------------*/
int main()
{
    int m=181;
   
    // 回溯方式 1
    int returnSize1=0;
    int* returnArr1=NULL;
    int ans1=QuarticNumber_DP_rec1(m, &returnArr1, &returnSize1);

    printf("building %d uses quardic numbers at least %d times\n", m, ans1);
    for(int i=0; i<dictNum; i++)
        printf("%2d used times: %d\n", i+1, returnArr1[i]);

    printf("\n");

    // 回溯方式 2
    int returnSize2=0;
    int* returnArr2=NULL;
    int ans2=QuarticNumber_DP_rec2(m, &returnArr2, &returnSize2);

    printf("building %d uses quardic numbers at least %d times\n", m, ans2);
    printf("Numbers below are used for the calculation: \n %d = ", m);
    for(int i=0; i<returnSize2; i++)
    {
        printf("%d^4", returnArr2[i]);
        if(i<returnSize2-1)
            printf(" + ");
    }
}