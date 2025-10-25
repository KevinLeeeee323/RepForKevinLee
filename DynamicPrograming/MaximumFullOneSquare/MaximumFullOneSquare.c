#include <stdio.h>
#include <stdlib.h>

#define max 4e6 // M*N最大值. 这个题比较夸张, 确实需要这么大的空间.
#define min(a, b) (((a)<(b))?(a):(b))

/*
    [题目描述]
        原始题目描述见同目录下 Problem.png
        以下是提炼后的:

        给定一个矩阵 M*N 的实mat, 每个元素为 0 或 1.
        请找出 mat 矩阵中面积最大的全是 1 的正方形, 返回其面积.
        
        e.g. mat=
                1 0 1 0 0
                1 0 1 1 1
                1 1 1 1 1
                1 0 0 1 0
        这一矩阵中, mat[1][2]为左上角, mat[2][3]为右下角构成的全 1 正方形最大, 边长为 2, 面积为 2*2=4.


        通过stdin [只用一行]输入矩阵mat, 同一行元素之间空格隔开, 不同行之间使用逗号隔开.
        对于上面例子的矩阵, 输入方式为:
        1 0 1 0 0,1 0 1 1 1,1 1 1 1 1,1 0 0 1 0
        数据是从 windows 上读入的, 换行符为 \r\n .


    [思路]
        首先要完成数据的读取, 从而建立起 mat 矩阵. 这部分内容见 initMat_Linear( )函数.
        采用动态规划.
        设M*N 阶矩阵, 通过二维数组 dp表示, 其中 dp[i][j]表示以mat[i][j]为左上角元素的最大全1正方形的边长

        由于要构建的全 1 正方形需要满足右下方扩展的条件, 可写出递推式:
            dp[i][j]=min(dp[i+1][j], dp[i][j+1], dp[i+1][j+1])+1,  mat[i][j]=1
            dp[i][j]=0, mat[i][j]=0

        因此要从 i=M-1, j=N-1, 逐步向 i=0, j=0 的方向计算.

        特别的, mat 最下方一行的元素 dp[M-1][j]或者 mat 最右侧的一列元素 mat[i][N-1], 有:
            dp[M-1][j]=mat[M-1][j],
            dp[i][N-1]=mat[i][N-1],
        因为已到矩阵的最外侧, 没法向右下方扩展.

        在上述地推过程中, 同时维护 dp 中最大元素值 max_len, 即最大全1正方形边长. 最终返回 max_len*max_len(其面积)

        由于这道题涉及到了具体的 IO 操作, 有一些细节需要注意, 以进一步提升代码效率. 就比如说二维数组线性化.
        具体见下面函数中的注释.


    [时间复杂度分析]
        对于 initMat_Linear() 函数:
            假设每读入一个 0 或者 1 后面都跟一个空格, 考虑到mat矩阵总共有 M*N 个元素, 那么字符串总长度大致为 O(2*M*N). 
            该部分的时间复杂度主要在 while 循环逐个读取, 故这个函数时间复杂度为 O(2*M*N).

        对于 MaximumFullOneSquare_DP() 函数:
            进行动态规划, 时间复杂度在于两侧 for 循环, 时间复杂度 O(M*N).

        因此, 总的复杂度仍为 O(M*N).
    
    [空间复杂度分析]
        一共开了 mat, dp 两部分, 不论是线性化的还是二维的, 空间复杂度都是 O(M*N). 
        因此总的空间复杂度 O(M*N)
*/

int* initMat_Linear(int*M, int* N)
{
    /*
        考虑实际读取, 为了进一步提升代码效率, 引入如下修改:
        
        [改进存储方式]
        测试样例中, 最终读到的 mat 存在样本量极大的. 
        这种情况下,如果再开二维数组, 频繁再给其中的每一行(每一个一维数组)malloc, 效率会很低.
        因此可以线性化的方式表示矩阵 mat.
        开设一维数组 linear_mat, 最终 mat[i][j]=linear_mat[i*N+j].
        同时, 一边读, 一边存储并且计算mat 的维度(行数M, 列数 N)
    */

    int* linear_mat=(int*)calloc(max, sizeof(int)); // 假设最多不超过 400000 个元素
    if(linear_mat==NULL) 
    {
        printf("fail to malloc! exit.");
        return NULL;
    }
    int top=-1;
    *M=0, *N=0;
    char c=0;
    while((c=getchar())!=EOF)
    {
        if(c=='\r' || c=='\n') // windows 上读入的换行符为 \r\n
            break;
        if(c=='0' || c=='1')
            linear_mat[++top]=c-'0';
        else if(c==',')
            (*M)++;
    }
    (*M)++; // 逗号数量+1=行数
    if((top+1)%(*M)!=0)
    {
        printf("wrong Input, try again\n");
        return NULL;
    }
    *N=(top+1)/(*M);

    return linear_mat;
}

int MaximumFullOneSquare_DP(int* linear_mat, int M, int N)
{
    // shape(mat)=M 行(0~M-1) , N 列(0~N-1)
    int* dp=(int*)calloc(M*N, sizeof(int));
    int tmp1=-1, tmp2=-1, tmp3=-1;
    /*
        
        [dp 的逻辑]
            假设 dp[i][j]表示以mat[i][j]为左上角元素的最大全1正方形的边长. mat[i][j]=linear_mat[i*N+j]
            由于要构建的全 1 正方形需要满足右下方扩展的条件, 可写出递推式:
            dp[i][j]=min(dp[i+1][j], dp[i][j+1], dp[i+1][j+1])+1,  mat[i][j]=1
            dp[i][j]=0, mat[i][j]=0

            因此要从 i=M-1, j=N-1, 逐步向 i=0, j=0 的方向计算.

            特别的, mat 最下方一行的元素 dp[M-1][j]或者 mat 最右侧的一列元素 mat[i][N-1], 有
                dp[M-1][j]=mat[M-1][j],
                dp[i][N-1]=mat[i][N-1],
            因为已到矩阵的最外侧, 没法向右下方扩展.
        
        
        考虑实际读取, 为了进一步提升代码效率, 引入如下修改:
        [改进存储方式]
            目前用 int** mat（指针数组）存储矩阵，对于 M=150, N=2000，需要：
            150 次 malloc（每行一次），频繁的系统调用会降低效率；
            内存碎片化风险高，大样本下可能分配失败。
            改用 “单块连续内存” 存储二维矩阵一次性分配 M*N 的连续内存， 线性化方式, 用 dp[i*N + j] 代替 dp[i][j]，减少系统调用
            这样也可以与上面的线性化 mat 匹配
    */

    int i=0, j=0, k=0;
    int max_dp=0;

    for(i=M-1; i>=0; i--)
    {
        for(j=N-1; j>=0; j--)
        {
            k=i*N+j; // dp[i][j] <-> i*N+j
            if(j==N-1 || i==M-1)
                dp[k]=linear_mat[k];
            else
            {
                if(linear_mat[k]==0)
                    dp[k]=0;
                else //linear_mat[i*N+j]=1
                {
                    // dp[i][j]=min(dp[i+1][j], dp[i][j+1], dp[i+1][j+1])+1
                    tmp1=dp[k+N]; //dp[i+1][j] <-> (i+1)*N+j <-> k+N
                    tmp2=dp[k+1]; // dp[i][j+1] <-> i*N+(j+1) <-> k+1
                    tmp3=dp[k+N+1]; // dp[i+1][j+1] <-> (i+1)*N+(j+1) <-> k+N+1
                    dp[k]=min(tmp1, min(tmp2, tmp3))+1;
                }
            }
            max_dp=(max_dp<dp[k])?dp[k]:max_dp; // 同时更新dp 中的最大值 max_dp
        }
    }
    return max_dp*max_dp; //根据题意, 返回最大全 1 正方形的面积 
}

int main()
{
    int M=-1, N=-1;
    int* linear_mat=initMat_Linear(&M, &N);
    if(linear_mat!=NULL)
    {
        int ans=MaximumFullOneSquare_DP(linear_mat, M, N);
        printf("%d", ans);
    }
}