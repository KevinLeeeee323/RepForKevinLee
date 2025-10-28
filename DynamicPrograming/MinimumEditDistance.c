#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
    [问题]
        给定字符串 A 和字符串 B, 返回 A 和 B 的最短编辑距离(Minimum Edit Distance), 并且指明是如何按顺序一步步进行修改的.
        
    [定义]编辑距离
        定义对一个字符串只能进行如下三种操作:
            (1) 删除其中的某一个字符
            (2) 在其中任意位置增加一个字符
            (3) 将其中任意一个字符替换成另外一个字符.
        
        显然, 能够在有限次的上述操作中, 将字符串 A 变成字符串 B. 操作的次数称为"编辑距离". 也就是我们用键盘打字, "编辑"字符串的次数

        将字符串 A 通过有限次操作变成字符串 B 的方式有很多. 每种方式都对应一个最短编辑距离. 其中最小的, 就是[最短编辑距离].

        比如, A="hello_word", B="hell_world"
        最短编辑距离为 2: 删除第一个'o',  并且在'd'前面增加'l'

        其他的编辑方式包括: 删除A的每一个字符, 然后再把 B的每一个字符添加上去. 这样下来, 编辑距离为 20
        注意: 这里的对字符进行操作, 不需要对'\0'进行操作, 只需要操作可见字符串.

        而且 A 和 B 中都是可见字符串, 只包含字母/数字/空格.

    
    [思路]动态规划

        [递推]
            设字符串 A 长度 n, 字符串 B 长度 m.
            以下为方便叙述, A, B字符串下标索引从 1 开始.

            创建有(n+1)行, (m+1)列的二维数组 dp[][].
            dp[i][j]表示A[1...i](A 第一个字符到第 i 个), B[1...j](B 第一个字符到第 j 个)这两个字符串的最短编辑距离.

            则可以写出递推式:

            dp[i][j]=min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+r_{ij}), 
            其中 r_{ij}= (A[i]!=B[j]), 也即A[i]!=B[j], r_{ij}=1, A[i]==B[j]时 r_{ij}=0

            Q:  为什么只考虑 A[i]与B[j-1], A[i-1]与 B[j]这些末尾字符的情况? 毕竟有些时候, 最小编辑距离发生在中间的字符的变化?

            A:  我们关注 "最后一步操作", 是为了将大问题拆解成更小的、可重复解决的子问题, 而不是说编辑操作只能发生在最后一个字符
                将 A[1..i] 转换成 B[1..j]", 无论中间经历了多少操作, 最终一定有一个 "最后执行的操作". 这个最后一步操作只有三种可能（替换、删除、插入）, 而每种操作都恰好对应一个更小的子问题：
                最后一步是 "替换"：说明在执行替换前, A[1..i-1] 已经转换成了 B[1..j-1]（即子问题 dp[i-1][j-1]）, 最后一步把 A[i] 换成 B[j] 即可, 因此末尾+1 
                最后一步是 "删除"：说明在执行删除前, A[1..i-1] 已经转换成了 B[1..j]（即子问题 dp[i-1][j]）, 最后一步删掉 A[i] 即可, 因此末尾+1
                最后一步是 "插入"：说明在执行插入前, A[1..i] 已经转换成了 B[1..j-1]（即子问题 dp[i][j-1]）, 最后一步插入 B[j] 即可, 因此末尾+1

                不考虑 "中间字符的变化", 是因为 "中间字符的变化" 已经被更小的子问题包含了. 

                举个例子：假设我们要将 abc 转换成 adc, 最优操作是把中间的 b 换成 d（1 次操作）. 
                对应到 dp[3][3]（整个字符串的转换）, 最后一步其实什么都不用做（因为 c == c）, 所以 dp[3][3] = dp[2][2]. 
                而 dp[2][2]（ab 转 ad）的最后一步是替换 b 为 d, 即 dp[2][2] = dp[1][1] + 1. 
                dp[1][1]（a 转 a）显然为 0. 
                可见, 中间字符的操作（替换 b 为 d）被包含在子问题 dp[2][2] 中, 而不是直接体现在 dp[3][3] 中. 动态规划通过逐层拆解, 自动覆盖了所有可能的操作位置, 包括中间字符. 

            以上回答是 AI 给出的, 如果不懂, 可以看视频: https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=27 
            特别的, i==0 或 j==0 的情况如下:
                dp[0][j]=j : 空串变成 B[1..j], 插入这 j 个字符
                dp[i][0]=i : A[1..i]变成空串, 删除这 i 个字符

        [回溯]
            如何进行回溯, 即如何得到最小编辑距离时, A 是如何一步步变成 B 的?
            回溯方式类似最大子序列问题.

            创建回溯矩阵 rec[][], 维度(n+1)行, (m+1)列.
            后续做法参考 上文链接.
            链接中所叙述的 L(left, 左, 对应插入), U(upper, 上, 对应删除), LU(left upper, 左上, 对应替换)通过 0, 1, 2 代替.
            回溯过程中, 会找到每次操作的方式和被操作的字符.

            因为回溯的顺序是和从 A 修改到 B 的顺序相反的, 所以只有逆序输出回溯内容, 才能正向输出 A 到 B 的修改顺序.
            这可以通过建立一个操作栈&被操作对象栈来实现.

        [二维数组线性化]
            为了减少 n 很大时多次 malloc (int*)dp[i], 可以将二维数组线性化.
            创建一维数组 dp_linear[], dp[i][j] <-> dp_linear[i*(m+1)+j]
            创建一维数组 rec_linear[], dp[i][j] <-> rec_linear[i*(m+1)+j]

    [复杂度分析]
        递推部分两重 for 循环, 复杂度 O((n+1)*(m+1)).
        回溯部分复杂度小于递推部分

        因此最终复杂度 O((n+1)*(m+1))
*/

// 注: 以下字符串下标从 0 开始
struct Modify
{
    int type;
    char origin;
    char result;
    int position; // 下标从 0 开始
};
typedef struct Modify node;
typedef struct Modify* list;

#define min(a, b) (((a)<(b))?(a):(b))
int MinimumEditDistance(char* A, char* B, list* OperateStack, int* OperateStackSize)
{
    int n=strlen(A);
    int m=strlen(B);
    int* dp_linear=(int*)calloc((m+1)*(n+1), sizeof(int));
    int* rec_linear=(int*)calloc((m+1)*(n+1), sizeof(int));

    int i=0, j=0, k=0;
    int min_operate_times=0;
    int r_ij=0;
    for(i=0; i<=n; i++)
    {
        for(j=0; j<=m; j++)
        {
            // 注: 以下字符串下标从 0 开始
            k=i*(m+1)+j; // dp/rec[i][j] <-> dp/rec_linear[i*(m+1)+j], 
            if(i==0 || j==0)
            {
                dp_linear[i*(m+1)+j]=(i==0)?j:i;
                rec_linear[i*(m+1)+j]=(i==0)?0:1;
            }
            else // i>0 && j>0
            {
                r_ij=(A[i-1]!=B[j-1]);
                // [i-1][j] <-> (i-1)*(m+1)+j=k-m-1
                // [i][j-1] <-> i*(m+1)+j-1=k-1
                // [i-1][j-1] <-> (i-1)*(m+1)+j-1=k-m-2
                min_operate_times=min(min(dp_linear[k-1]+1, dp_linear[k-m-1]+1), dp_linear[k-m-2]+r_ij);
                if(min_operate_times==dp_linear[k-1]+1) // 插入
                    rec_linear[k]=0;
                else if(min_operate_times==dp_linear[k-1-m]+1) // 删除
                    rec_linear[k]=1;
                else // min_operate_times==dp_linear[k-m-2]+r_ij, 替换
                    rec_linear[k]=2;
                dp_linear[k]=min_operate_times;
            }
        }
    }
    
    // Retrieve and Return
    int ans=dp_linear[n*m+n+m]; // [n][m] <-> n*(m+1)+m
    *OperateStackSize=ans;
    *OperateStack=(list)calloc(ans, sizeof(node));
    if (*OperateStack == NULL) 
    {
        printf("fail to malloc for OperateStack\n");
        exit(1);
    }

    for(int i=0; i<=n; i++)
    {
        for(int j=0; j<=m; j++)
            printf("%d ", rec_linear[i*(m+1)+j]);
        printf("\n");
    }
    printf("-----------------\n");
    i=n, j=m;
    int top=-1;
    int tmp=0;
    while(i>0 || j>0)
    {
    // 注: 以下字符串下标从 0 开始
        k=i*(m+1)+j;
        tmp=rec_linear[k];
        if(i>0 && j>0)
        {
            if(tmp==0) // 插入 B[j-1]
            {
                (*OperateStack)[++top].type=tmp;
                (*OperateStack)[top].origin='\0';
                (*OperateStack)[top].result=B[j-1];
                (*OperateStack)[top].position=i; // 插入 B[j-1], 插入位置: A[i]
                j--;
            }
            else if(tmp==1) // 删除A[i-1]
            {
                (*OperateStack)[++top].type=tmp;
                (*OperateStack)[top].origin=A[i-1]; 
                (*OperateStack)[top].result='\0';
                (*OperateStack)[top].position=i-1; // 删除 A[i-1]
                i--;
            }
            else // tmp==2
            {
                if(A[i-1]!=B[j-1])
                {
                    (*OperateStack)[++top].type=tmp;
                    (*OperateStack)[top].origin=A[i-1]; 
                    (*OperateStack)[top].result=B[j-1];
                    (*OperateStack)[top].position=i-1;
                    // A[i-1]换成 B[j-1]
                }
                i--, j--;
            }  
        }
        else if (i>0) // B已空，删除剩余A
        { 
            (*OperateStack)[++top].type=1;
            (*OperateStack)[top].origin=A[i-1];
            i--;
        } 
        else // A已空，插入剩余B
        { 
            (*OperateStack)[++top].type=0;
            (*OperateStack)[top].result=B[j-1]; // 不会空，j>0 时 B[j-1] 有效
            j--;
        }
    }
   
    free(dp_linear);
    free(rec_linear);
    return ans;
}

char number_suffix[][3]={"st", "nd", "rd", "th"};
char* NumberSuffix(int n)
{
    // 规范语法, 让最后打印的时候, 如果是 1/2/3, 输出 1st/2nd/3rd, 而不是 1th/2th/3th
    int tmp=n%10;
    if(tmp>=1 && tmp<=3)
        return number_suffix[tmp-1];
    else
        return number_suffix[3];
}


/*--------------------------Test Case--------------------------*/
int main()
{
    char A[]="ABC_BDAB";
    char B[]="BD!CABA";
    // char A[]="hello,word";
    // char B[]="hell_world!";

    list OperateStack=NULL;
    int OperateStackSize=0;
    int ans=MinimumEditDistance(A, B, &OperateStack, &OperateStackSize);
    printf("Minimum Edit Distance: %d\n", ans);
    printf("Below shows how to convert from String A to String B:\n\n");
    int tmp=0;
    int pos=0;
    
    // 打印如何修改.
    // 其中的下标从 1 开始,都以A 的原始字符串为准.
    for(int i=OperateStackSize-1; i>=0; i--)
    {
        tmp=OperateStack[i].type;
        pos=OperateStack[i].position;
        if(tmp==0)
            printf("Insert '%c' after the %d_%s character of String A, which is '%c'\n", OperateStack[i].result, pos, NumberSuffix(pos), A[pos-1]);
        else if(tmp==1)
            printf("Delete the %d_%s character of String A, which is, '%c'\n", pos+1, NumberSuffix(pos+1), OperateStack[i].origin);
        else // tmp==2
            printf("Convert the %d_%s character of String A which is '%c', to '%c'\n", pos+1, NumberSuffix(pos+1), OperateStack[i].origin, OperateStack[i].result);
    }
}