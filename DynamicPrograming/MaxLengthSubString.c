#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
    [问题]
        寻找两个非空字符串X, Y的最长公共子串(Substring), 返回其长度, 及其这个子串的内容. 最长子串用 SubString 表示, 其长度 maxlen.
        X 长度 n, Y 长度 m.

    [定义]子串
        从一个序列Arr[n]中取出一些连续排列的元素, Arr[k], Arr[k+1], Arr[k+2], ...Arr[k+m] 为原序列的一个长度为 (m+1)的子串.
        比如序列 A="1234567", "123", "345", 都是其子串, 而"135", "246"不是, 因为其中的元素不相邻

        [区分子串与子序列]
            子序列中的元素可以不相邻, 子串可以
            子序列定义, 参考 MaxLengthSubsequence.c

            序列 Arr {所有子串组成的集合} 是其 {所有子序列组成集合} 的子集

        序列 Z 是序列 X和 Y 的公共子串当且仅当 Z 是序列 X 的子串, 也是序列 Y 的子串.


    [思路一]Brute-Force 蛮力枚举
        枚举 X 的所有子串 Z, 并且看 Z 是否也是 Y 的子串. 维护一个公共子串的最大长度 maxlen.
        如果是的话, 比较 Z 序列的长度和 maxlen, 如果 Z 的长度更长, 那就更新 maxlen.
        同时保存当前最长的子串, 以便后续输出.

        [时间复杂度分析]
        枚举 X 的所有子串Z:  Z 开始于X[i], 结束于 X[j],  0<=i<=j<=n-1, 这样的子串一共有(n+1)n/2 个
        判断Z 是否是 Y 的子串: 可以用 C 语言内置函数 strstr() 进行查找, 标准库中最常见的朴素实现（暴力匹配算法）时间复杂度为 O ((j-i+1)*m)
        因此最终复杂度 sum_{0<=i<=j<=n-1}{O(j-i+1)*m}=O((n^2)*m)

    [思路二]动态规划
        较长子序列中包含了较短子序列, 因此可能有"最优子结构"性质, 可以考虑动态规划.
        定义 n 行 m 列 dp[][]数组, 其中dp[i][j]表示 X[0...i]和 Y[0...j]中, 以 X[i] 和 Y[j] 结尾的最长公共子串的长度(一定要强调以 X[i]和 Y[j] 结尾)
        则可以写出递推式:
            dp[i][j]=0, X[i]!=Y[j] (因为强调了以 X[i], Y[j]结尾, 如果这两个字符不相同, 则没有以之结尾的公共子串)
            dp[i][j]=1+dp[i-1][j-1], X[i]=Y[j]
                X[i]==Y[j], 表达式如上的原因:
                    因为定义 dp[i][j]是以X[i] 和 Y[j] 结尾的最长公共子串的长度, 
                    因此当 X[i]==Y[j]时, 应该只看以X[i-1] 和 Y[j-1] 结尾的最长公共子串的长度, 这样才能保证最长子串的下标连续性
                    并且在 dp[i-1][j-1]基础上+1(X[i]==Y[j])
        
        特别的, dp[0][j]=(X[0]==Y[j]), dp[i][0]==(X[i]==Y[0])

        - 二维数组线性化
            考虑到两个字串长度长, 开设二维 dp 数组时, 会很多次通过 malloc 或者 calloc分配一维数组空间效率低, 因此可以将 dp数组线性化

            具体而言, 开设一维数组 dp_linear, 对应关系为: dp[i][j]=dp_linear[i*m+j]

        如何回溯?
            同时维护maxlen, 表示最大子串长度; 维护 i_0, 表示最长公共子串时的结束位置, 对应字符 X[i_0].
            当找到长度 > maxlen 的最长子串时, 记录此时的 i值 为 i_0, 并且更新 maxlen.

        最终 X[i_0-maxlen+1], X[i_0-maxlen+2], ...X[i_0]为最长子串, 长度 maxlen.

        [时间复杂度分析]
            复杂度在于两层 for 循环, 复杂度 O(n*m).
            后续回溯中涉及复制字符串到 SubString, 时间复杂度最坏为 O(max(n, m)).
            
            因此, 总时间复杂度 O(n*m), 优于[思路一].

        [空间复杂度分析]
            一个 dp 数组, 占据空间 n*m 个 int 值(整数序列) 或者 n*m 个 char 值(字符串序列)

    注: 以下只是以字符串序列为例. 整数数列也可以, 只不过要增加参数 Xsize, Ysize, 即两个数组各自的长度.
*/

int MaxLengthSubString(char* X, char* Y, char** SubString)
{
    int n=strlen(X);
    int m=strlen(Y);
    if(m*n==0)
    {
        *SubString=NULL;
        printf("one of the String is Empty String. Retry\n");
        return 0;
    }

    int* dp_linear=(int*)calloc(n*m, sizeof(int));
    int i=0, j=0, k=0;
    int i_0=-1;
    int maxlen=0;
    for(i=0; i<n; i++)
    {
        for(j=0; j<m; j++)
        {
            k=i*m+j;
            // dp[i][j]=dp_linear[i*m+j]=dp_linear[k]
            if(i==0 || j==0)
                dp_linear[k]=(X[i]==Y[j]);
            else
                dp_linear[k]=(X[i]==Y[j])*(1+dp_linear[k-m-1]); 
            /*
                dp[i][j]=0, X[i]!=Y[j] 
                dp[i][j]=1+dp[i-1][j-1], X[i]=Y[j]
                上面这两种情况合并, 可以写成上面的 else 中的语句
                此处 dp[i-1][j-1]=dp_linear[(i-1)*m+(j-1)], 
                其中 (i-1)*m+(j-1) = i*m+j-m-1 = k-m-1
            */
            if(dp_linear[k]>maxlen) //maxlen>=0, 这样只针对 dp_linear[k]>1 的情况更新
            {
                maxlen=dp_linear[k];
                i_0=i;
            }
        }
    }

    // 输出最长公共子串
    if(maxlen==0)
    {
        *SubString=NULL;
        printf("no common SubString found within X and Y.\n");
    }
    else
    {
        *SubString=(char*)malloc(sizeof(char)*(maxlen+1));
        strncpy(*SubString, X + (i_0 - maxlen + 1), maxlen);
        (*SubString)[maxlen]='\0'; // 对于字符串, 最长子串后面需要加一个'\0', 实际长度为 maxlen+1
        printf("MaxlenSubString is \"%s\"\n", *SubString);
    }
    free(dp_linear);
    return maxlen;
}

/*-------------------------Test Case-------------------------*/
int main()
{
    char X[]="ACGCTGA";
    char Y[]="CTGATG";
    char* SubString=NULL;
    int maxlen=MaxLengthSubString(X, Y, &SubString);
    printf("%d", maxlen);
}