#include <stdio.h>
#include <stdlib.h>

/*
    [问题背景]
        两个矩阵 A(m 行 k 列), B(k 行 n 列)进行乘法运算, 最终生成 C=A*B, 一个 m 行 n 列的矩阵.
        对于 C 中的每一个元素 c_ij, c_{ij}=\sum_{t=1}^{k}{a_{it}*b_{tj}}
        对于 c_ij 的计算, 其中有 k次乘法和 k-1 次加法.
        对于矩阵 C 中有 m*n 个这样的 c_ij, 因此可以视为, 这一次矩阵乘法复杂度O(m*n*k).

        对于多个矩阵进行联乘, 由于乘法结合律的存在, 乘法运行的顺序, 会导致最终的复杂度有所不同.
        比如对于矩阵 A*B*C, A(10 行 20 列), B(20 行 30 列), C(30 行 40 列)
        假如计算顺序为(A*B)*C:
            A*B 计算复杂度为 O(10*30*20), 而 D=A*B 为 10 行 30 列, D*C 复杂度为 O(10*40*30)
            因此加在一起, 复杂度为 O(6000+12000)=O(18000)
            
        假如计算顺序为A*(B*C):        
            B*C 计算复杂度为 O(20*40*30), 而 E=B*C 为 20 行 40 列, A*E 复杂度为 O(10*40*20)
            因此加在一起, 复杂度为 O(24000+8000)=O(32000)

        这两种计算顺序的不同, 会导致最终计算的复杂度不同!
        因此再进行多个矩阵的连乘时, 应当对于计算适当添加括号, 改变计算先后顺序, 从而降低最终的复杂度.


    [问题描述]
        给定 n 个矩阵:A_1, A_2, ...A_n, 其中 A_i的规模为 p_{i-1}行 p_i 列.
        (这样表示的话, A_i和 A_{i+1}才可能相乘: A_i的规模为 p_{i-1}行 p_i 列, A_{i+1}的规模为 p_i行 p_{i+1} 列)
        将这些矩阵相乘, 最终结果 B=A_1 * A_2 * ... * A_n, 最终规模为 p_0 行 p_n 列.

        要求找到一种加括号的方式, 从而确定矩阵连乘的计算顺序, 使得最小化矩阵连乘计算的复杂度


    [解决思路]
        显然, 计算 A_i * A_{i+1} * ... * A_j 总是需要把计算拆成两个子问题进行:
        (A_i * A{i+1} * ... * A_k) * (A_{k+1} * A_{k+2} * ... * A_j}, 其中 k=i, i+1, ...j-1
        因此, 需要两部分的计算复杂度都最小, 才能使得总计算复杂度最小.

        这样看的话, 问题具有最优子结构性质. 可以使用动态规划进行求解.
    
    [解决方案: 动态规划]
        构建二位动态规划数组 dp, 其中 dp[i][j]表示计算A_i * A_{i+1} * ... * A_j所需的最小计算复杂度.
        则可以写出递推公式:
            dp[i][j]=0, i==j(一个单独的矩阵, 无需计算) 这一部分在 dp 数组中直接初始化成 0.
            dp[i][j]=min(dp[i][k] + dp[k+1][j] + p_{i-1} * p_k * p_j), i!=j
                解释:
                dp[i][k]是计算 B=A_i * A{i+1} * ... * A_k所需的复杂度, B 的规模是 p_{i-1}行 p_k 列
                dp[k+1][j]是计算C=A_{k+1} * A_{k+2} * ... * A_j 所需的复杂度, C 的规模是 p_k行 p_j 列
                p_{i-1} * p_k * p_j 是计算 B*c 的复杂度. 三部分加在一起, 构成从 A_k 进行划分时的计算复杂度.
                遍历所有的可能划分方式 k, 从中找到最小的复杂度, 得到 dp[i][j].

        dp 数组维度为(1+n)行, (1+n)列. 其中第 0 行 第 0 列并没有参与到计算中, 无需考虑对其的初始化.
        真正需要初始化的, 是上面的 dp[i][i]=0., 1<=i<=n.
        然后进行递推时, 要注意遍历的方向.

        最终求出 dp[1][n]作为答案.

    [回溯: 确定最终的括号添加方式]
        设置rec 二维数组, 进行回溯.
        其中 rec[i][j]=k 表示 dp[i][j]取得最小值时, 对应的划分点 A_k 矩阵的下标 k.(在递推过程中, 同时构建起 rec二维数组)
        对 rec[1][n]开始, 进行回溯:
                                    A_1 * A_2 * ... * A_n (rec[1][n]=k1)
                                     /                          \
                A_1 * A_2 * ... * A_k1                           A_{k1+1} * A_{k1+2} * ... * A_n
                        (rec[1][k1]=k2)                                         (rec[k1+1][n]=k3)
                    /            \                                        /                 \
        A_1 * A_2 * ... A_k2    A_{k2+1} * A{k2+2} * ... * A_k1         ...                 ...
        ...                      ...

    [时间复杂度分析]
        动态规划部分, 复杂度 O(n^3). 因为对于每一个 i, j, 求出 dp[i][j]需要比较 j-i 次, 
        且考虑到所有满足 1<=i<j<=n 的(i, j)对, 
        因此最终复杂度为 \sum_{i=1}^{n}{\sum_{j=i+1}^{n}{j-i}}, 大概在 O(n^3)级别.

        进行回溯时, 复杂度约为 O(n).

        因此最终的时间复杂度总计 O(n^3).

    [注]p_i 通过p 数组存储, 下标范围[0, n].

*/

void Retrieve(int** rec, int i, int j) // 负责回溯. 在 MatrixChainMultiplication() 中被调用
{
    if(i==j)
        printf("A%d", i);
    else
    {
        int tmp=rec[i][j];
        // 以下引入了很多 if 判断, 防止在只有一个矩阵的时候, 依然加括号, 比如(A1)
        if(i!=tmp)
            printf("(");
        Retrieve(rec, i, tmp);
        if(i!=tmp)
            printf(")");
        if(tmp+1!=j)
            printf("(");
        Retrieve(rec, tmp+1, j);
        if(tmp+1!=j)
            printf(")");
    }
}

int MatrixChainMultiplication(int *p, int n)
{
    int i=0, j=0;

    int** dp=(int**)malloc(sizeof(int*)*(n+1));
    if(dp==NULL)
    {
        exit(-1);
        printf("fail to malloc.\n");
    }
    for(i=0; i<=n; i++)
        dp[i]=(int*)calloc(n+1, sizeof(int));

    int** rec=(int**)malloc(sizeof(int*)*(n+1));
    if(rec==NULL)
    {
        exit(-1);
        printf("fail to malloc.\n");
    }
    for(i=0; i<=n; i++)
        rec[i]=(int*)calloc(n+1, sizeof(int));

    int t=1;
    int k=0;
    int min=0;
    int tmp=0;
    for(t=1; t<n; t++)
    {
        for(i=1; i<=n-t; i++)
        {
            j=i+t;
            // 假定 k=i 时有最小值, 然后比较 k=i+1, i+2, ...j
            min=dp[i][i]+dp[i+1][j]+p[i-1]*p[i]*p[j];
            rec[i][j]=i;
            for(k=i+1; k<j; k++)
            {
                tmp=dp[i][k]+dp[k+1][j]+p[i-1]*p[k]*p[j];
                if(tmp<min)
                {
                    min=tmp;
                    rec[i][j]=k;
                }
            }
            dp[i][j]=min;
        }
    }

    // for(i=0; i<=n; i++)
    // {
    //     for(j=0; j<=n; j++)
    //         printf("%d ", rec[i][j]);
    //     printf("\n");
    // }

    // 回溯, free 与输出
    int ans=dp[1][n];
    printf("Minimum Cost Calculating Order:\n");
    Retrieve(rec, 1, n);
    printf("\n");
    for(i=0; i<=n; i++)
        free(dp[i]), free(rec[i]);
    free(dp), free(rec);
    return ans;
}


/*-----------------------------Test Case-----------------------------*/
int main()
{
    int p[]={1, 2, 3, 5, 4, 3, 2};
    // int p[]={10, 100, 5, 50}; // Other Test Cases
    int n=sizeof(p)/sizeof(int)-1;
    int ans=MatrixChainMultiplication(p, n);
    printf("Minimum Cost: %d", ans);
}