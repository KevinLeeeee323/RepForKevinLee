#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*
    [问题]
        寻找两个非空字符串X, Y的最长公共子序列(Subsequence), 返回其长度, 及其这个序列的内容. 最长子序列用 ans 表示, 其长度 maxlen.
        X 长度 n, Y 长度 m.

    [定义]子序列
        从一个序列中取出一些元素, 按照之前的下标顺序排列在一起组成的新序列, 为原序列的子序列.
        比如序列 A="1234567", "123", "145", "137"都是其子序列

        序列 Z 是序列 X和 Y 的公共子序列当且仅当 Z 是序列 X 的子序列, 也是序列 Y 的子序列.

        [区分子序列 & 子串]
            子序列中的元素可以不相邻, 子串不可以
            子串定义, 参考 MaxLengthSubString.c

            序列 Arr {所有子串组成的集合} 是其 {所有子序列组成集合} 的子集
    
    [思路一]Brute-Force 蛮力枚举
        枚举 X 的所有子序列 Z, 并且看 Z 是否也是 Y 的子序列. 维护一个公共子序列的最大长度 maxlen.
        如果是的话, 比较 Z 序列的长度和 maxlen, 如果 Z 的长度更长, 那就更新 maxlen.
        同时保存当前最长的子序列, 以便后续输出.

        时间复杂度:
        枚举 X 的所有子序列Z: O(2^n)=O(2^n-1)=O(\sum_{i=1}^{i=n}{C_n^i})
        判断Z 是否是 Y 的子序列:双指针法. 如果 Z 的每一个字符都按顺序出现在 Y 中, 那就是 Y 的子序列. 反之则不是. 时间复杂度最差为O(nm), 即需要完整同步遍历 X 和 Y.
        因此最终复杂度 O(n*m*2^n), 过于庞大


    [思路二]动态规划
        较长子序列中包含了较短子序列, 因此可能有"最优子结构"性质, 可以考虑动态规划.
        构建(n+1)行, (m+1)列的二维数组 dp, 其中 dp[i][j]表示 X[1...i], Y[1...j]这两个序列的最长公共子序列的长度.
        因此, 题目所求结果即为 dp[n][m].

        下寻找递推式:
        dp[i][j]=max{dp[i][j-1], dp[i-1][j]}, 若 X[i]!=Y[j]
            原因: X[i]!=Y[j], 因此 X[i]和 Y[j]不可能同时出现在最长子序列中, 因此考虑 X[1..i]和 Y[1..j-1]的最长子序列, X[1..i-1]和 Y[1..j]的最长子序列, 取更长的
            其实也应该考虑一下 X[1..i-1]和 Y[1..j-1], 但是显然 dp[i][j-1]>dp[i-1][j-1], dp[i-1][j]>dp[i-1][j-1]因此不考虑这一项
             
        dp[i][j]=max{dp[i-1][j-1]+1, dp[i][j-1], dp[i-1][j]}=dp[i-1][j-1]+1, 若 X[i]==Y[j]
            X[i]==Y[j], 因此 X[i]和 Y[j]可能同时出现在最长子序列中, 故考虑 X[1..i-1]和 Y[1..j-1]的最长子序列, 长度再+1(X[i]==Y[j])
            但也可能是 X[1..i]和 Y[1..j-1], X[1..i-1]和 Y[1..j]的最大子序列.
            因此同时考虑这三者,取 max
        
        (注:这里认为 X, Y数组的下标索引从 1 开始. 但是下面的代码中则不然, 仍是从 0 开始)

        具体推导过程见 https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.player.switch&vd_source=c8e4e809f91f46885a44be8339a7976c&p=24 

        特别的, 对于 dp[0][j]和 dp[i][0], 由于其中一个序列式空串, 直接赋值为 0.

        可一行一行/一列一列的计算递推式, 直到求出 dp[n][m].

        由此找到了最长公共子序列的长度, 但是还没能确定最长公共子序列的起终点. 通过回溯手段可以求出.

        创建回溯矩阵 rec[][], 维度(n+1)行, (m+1)列.
        后续做法参考 上文链接.
        链接中所叙述的 L(left, 左), U(upper, 上), LU(left upper, 左上)通过 0, 1, 2 代替.
        回溯过程中存储每次找到的最长公共子序列的元素(当且仅当 rec[i][j]==2 时). 最终将其按照正确的顺序(即在原序列 X, Y 中的相对先后顺序)输出即可.

        [时间复杂度]
            求解 dp[n][m]过程:
                主要时间复杂度来源于两次 for 循环(1<=i<=n, 1<=j<=m), 两次循环内部时间复杂度为 O(1).  
                该部分复杂度 O(n*m)
            回溯过程: 
                在矩阵内部跳转, 复杂度不超过矩阵规模 O(n*m)
            
            故总体上复杂度 O(n*m).

    注: 以下只是以字符串序列为例. 整数数列也可以, 只不过要增加参数 Xsize, Ysize, 即两个数组各自的长度.
*/


void printMats(int n, int m, int** mat) //debug 用
{   
    int i=0, j=0;
    for(i=0; i<n; i++)
    {
        for(j=0; j<m; j++)
            printf("%d ", mat[i][j]);
        printf("\n");
    }
}

int MaxLengthSubSequence(char* X, char* Y, char** ans)
{
    /*
        注意: 上述注释中默认字符串起始下标为 1.
        但是在下面的代码中, 仍是以 0 为下标的.这就导致和注释中or视频链接中的递推公式不太一样
    */
    int n=strlen(X);
    int m=strlen(Y);
    int i=0, j=0;

    int** dp=(int**)malloc(sizeof(int*)*(n+1));
    int** rec=(int**)malloc(sizeof(int*)*(n+1));
    for(i=0; i<=n; i++)
    {
        dp[i]=(int*)calloc(m+1, sizeof(int));
        rec[i]=(int*)calloc(m+1, sizeof(int));
    }

    // 求解 dp[n][m], 同时标注rec 回溯矩阵
    int tmp0=-1, tmp1=-1;
    for(i=1; i<=n; i++)
    {
        for(j=1; j<=m; j++)
        {
            if(X[i-1]==Y[j-1])
            {
                dp[i][j]=dp[i-1][j-1]+1;
                rec[i][j]=2;
            }
            else //X[i-1]=Y[j-1]
            {
                tmp0=dp[i-1][j];
                tmp1=dp[i][j-1];
                if(tmp0>=tmp1)
                {
                    dp[i][j]=tmp0;
                    rec[i][j]=0;
                }
                else
                {
                    dp[i][j]=tmp1;
                    rec[i][j]=1;
                }
            }   
        }
    }    
    int maxlen=dp[n][m]; // 最终结果
    
    // 进行回溯, 确定最大公共子序列的组成
    *ans=(char*)malloc(sizeof(char)*(maxlen+1));
    int tmp=maxlen-1;

    i=n, j=m;
    while(i>0 && j>0 && tmp>=0) // 这里的条件判断是否有问题?
    {
        if(rec[i][j]==0)
            i--;
        else if(rec[i][j]==1)
            j--;
        else // rec[i][j]==2, 对应'LR', 此时X[i-1]==Y[j-1]是最长子序列中的元素
        {
            (*ans)[tmp]=X[i-1];
            tmp--;
            i--, j--;
        }
    }
    (*ans)[maxlen]='\0';

    // debug info
    // printMats(n+1, m+1, dp);
    // printf("--------------------\n");
    // printMats(n+1, m+1, rec);

    for(i=0; i<=n; i++)
    {
        free(dp[i]);
        free(rec[i]);
    }
    free(dp);
    free(rec);

    return maxlen;
}

/*----------------------Test Case----------------------*/
int main()
{
    char X[]="ezupkr";
    char Y[]="ubmrapg";

    // char X[1001];
    // char Y[1001];
    // scanf("%s%s", X, Y);
    char* ans=NULL;
    int maxlenSubSequence=MaxLengthSubSequence(X, Y, &ans);
    printf("%d\n", maxlenSubSequence);
    puts(ans);
    
}