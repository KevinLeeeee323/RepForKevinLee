#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*
    来自 LeetCode题库第5题.

    寻找一个给定字符串s中的最长回文子串, 并且返回这个最长的回文子串.
    s 长度不超过 1000.

    [思路]:
        记 dp[i][j]表示以 s[i]开头, s[j]结尾的字符串是不是回文子串(是:dp[i][j]==1, 不是dp[i][j]==0)
        这样可以通过动态规划的方式得到递推表达式:
        i==j, dp[i][j]=1
        i==j-1, dp[i][j]=1 当且仅当 s[i]==s[j]
        i<j-1, dp[i][j]==1 当且仅当 s[i]==s[j] && dp[i+1][j-1]==1
        注意这样的递推式的遍历方式:
        二维数组 dp,  按副对角线方向为一层遍历, 层次从左下->右上. 每层内部则是从 i 小到 i 大的方向

        为了找出最大的回文子串, 只需维护最大回文子串长度 maxlen_str,以及记录最大会文字串的起始点下标 maxlenI, 
        在当前子数组 s[i]~s[j]是更长的回文子串(即 dp[i][j]==1)的时候更新 maxlen_str, maxlenI 即可
    
    [时间复杂度分析]
        两层循环, 遍历次数实际为 n(n-1)/2, 最终复杂度O(n^2), 其中 n 是字符串长度
*/

#define maxlen 1001
char* FindLongestPalindrome(char* s)
{
    int len=strlen(s);
    int** dp=(int**)malloc(sizeof(int*)*len);
    int i=0, j=0;

    // 记录最长会文字串的起点和长度
    int maxlenI=0;
    int maxlen_str=0;

    for(i=0; i<len; i++)
        dp[i]=(int*)calloc(len, sizeof(int));
    
    int t=0;
    // 遍历顺序: 二维数组 dp,  按副对角线方向为一层遍历, 层次从左下->右上. 每层内部则是从 i 小到 i 大的方向
    for(t=0; t<len; t++)
    {
        i=0, j=i+t;
        for(; i<len; i++)
        {
            j=i+t;
            if(j>=len)
                break; // 防止j越界访问;
            if(i==j)
                dp[i][j]=1; // 单个字符构成回文子串
            else if(i==j-1)
                dp[i][j]=(s[i]==s[j]); // 两个字符的情况
            else
                dp[i][j]=dp[i+1][j-1]&(s[i]==s[j]); // 通过位运算来表示两个条件同时成立
            if(dp[i][j]==1 && j-i+1>maxlen_str)
            {
                maxlenI=i;
                maxlen_str=j-i+1;
            }
        }
    }

    char* ans=(char*)malloc(sizeof(char)*(maxlen_str+1));
    for(t=0; t<maxlen_str; t++)
        ans[t]=s[maxlenI+t];
    ans[maxlen_str]='\0';

    for(i=0; i<len; i++)
        free(dp[i]);
    free(dp);

    return ans;
}

/*---------------Test Case-----------------*/
int main()
{
    char s[]="babad";
    puts(FindLongestPalindrome(s));
}