#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*
    寻找一个给定字符串s中的最长回文子串, 并且返回这个最长的回文子串.
    s 长度不超过 1000.
*/

#define maxlen 1001
char* FindLongestPalindrome(char* s)
{
    int len=strlen(s);
    int** dp=(int**)malloc(sizeof(int*)*len);
    int i=0, j=0;

    // 记录最长会文字串的起终下标
    int maxlenI=0;
    int maxlenJ=0;

    for(i=0; i<len; i++)
        dp[i]=(int*)calloc(len, sizeof(int));
    
    
    for(i=0; i<len; i++)
    {
        for(j=i; j<len; j++)
        {
            if(i==j)
                dp[i][j]=1; // 单个字符构成回文子串
            else if(i==j-1)
                dp[i][j]=(s[i]==s[j]); // 两个字符的情况
            else
                dp[i][j]=dp[i+1][j-1]&(s[i]==s[j]);
            
        }
    }

    /*
    1. 遍历顺序需要修改: 左下->右上
    2. for 循环最后比较 当前回文串长度和 maxlen, 并且更新 maxlenI/J;
    3. 最后把字符串复制到一个 ans 里面, 记得结尾添加'\0'
    */
    return NULL;
}

int main()
{
    char* s1="123hello";
    printf("%d", strlen(s1));
}