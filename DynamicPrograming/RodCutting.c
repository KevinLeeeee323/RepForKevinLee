#include <stdio.h>
#include <stdlib.h>

struct RodPiece
{
    int len;
    int price;
};
typedef struct RodPiece node;
typedef struct RodPiece* list;

int compare(const void* a, const void* b)
{
    int val_a=(*(list)a).len;
    int val_b=(*(list)b).len;
    return val_a-val_b;
}
/*
    [问题描述]
        给定一个长度为 n 的钢条, 可以将其零成本的切割成很多小段进行售卖
        钢条长度 1 2 3 4 5  6  7  8  9  10 
        对应价格 1 5 8 9 10 17 17 20 24 25

        对于每一个切割的小段,  如表中记录的那样, 最小切割长度为 1,最大切割长度为 10.
        求怎样切割, 能够获得最大的利润(这里由于切割成本是 0, 因此钢条卖出去的总价格=利润)? 并且输出当取得最大利润时的切割方式.
    
    [例子] 一个可行的切割方式
        10=5+5, 切成两段长度为 5 的钢条, 最终利润 10+10=20.
        又或者, 10=1+2+3+4, 四段, 长度分别为 1, 2, 3, 4, 对应利润分别为 1, 5, 8, 9, 最终利润 1+5+8+9=23.


    [暴力枚举]
        枚举n 可以被拆成的情况:, 以 n=4 为例:
         4=0+4, 4=1+3, 4=2+2, 4=1+1+2, 4=1+1+1+1, 分别计算每种的利润, 返回最大的

    [思路] 动态规划
        见一下两种算法.

*/
#define max(a, b) (((a)>(b))?(a):(b))
int RodCutting_Method1_DP(int n, list Rods, int RodsSize, int** rec) // 我的理解 T(n)=max(T(n-k)+T(k)), k=1, 2, 3...n
{
    int* dp=(int*)calloc(n+1, sizeof(int));
    *rec=(int*)calloc(n+1, sizeof(int));

    int profit_max=0;
    int i=0, j=0, k=0;
    
    for(i=1; i<=n; i++)
    {
        profit_max=0;
        for(j=1; j<i; j++)
        {
            if(dp[j]+dp[i-j]>profit_max)
            {
                profit_max=dp[j]+dp[i-j];
                (*rec)[i]=j;
            }
        }
        for(k=0; k<RodsSize; k++)
        {
            if(i==Rods[k].len && Rods[k].price>profit_max)
            {
                profit_max=Rods[k].price;
                (*rec)[i]=Rods[k].len;
            }
        }
        /*
            [动态规划 思路1]
                dp[i] 表示当前长度为 i 的钢条的最大利润.
                每一次都把问题拆分成两个子问题: i 一定是通过 长度为j 的钢条和长度为 i-j 的钢条进行售卖的
                因此, 可以写出递推式:
                    dp[i]=max(dp[j]+dp[i-j]), 如果长度为 i 的钢条不能单独售卖
                    dp[i]=max(dp[j]+dp[i-j], price[i]), 如果长度为 i 的钢条能单独售卖. price[i]表示已知数据中, 所给出的长度为 i 的钢条的价格.
                    其中 j=1, 2, 3 ... (i-1)
            
            [回溯]
                即如何确定最大利润时的切分方式?
                [思路 1]的回溯方式要比[思路 2]复杂不少. 而且要递归的进行.
                
                设置 rec[] 数组进行回溯. rec[i]=j 表示当长度为i 的钢条取得最大利润时, 将其拆分成 长度为j 和长度为 i-j 的两部分.
                只要赋值 j 和 i-j 中任意一个就行, 因为两部分都需要在递归中输出, 无非是先后顺序不同罢了.
                其划分方式就对应了下面 RodCutting_Method1_Retrieve() 函数的写法.

                画图来说, 以 n=23 为例, 一层一层的, 递归的拆成可以单独出售的钢条:
                                23
                                / \
                               /   \
                              /     \
                             2       21
                                     /\
                                    3  18
                                       |\
                                       | \
                                       6  12
                                           |\
                                           | \
                                           6  6
                              
            [时间复杂度分析](不考虑回溯部分, 回溯部分复杂度不好分析)
                外层for 循环, O(n)
                内层有两个并列的 for 循环, 一个复杂度 O(i), 另一个 O(m)
                其中 m 为可以单独售卖的钢条的种类数（不同长度的钢条数量）.

                因此, 总的复杂度 O(n^2+n*m)
        */
        dp[i]=profit_max;
    }
    int ans=dp[n];
    free(dp);
    return profit_max;
    
}

void RodCutting_Method1_Retrieve(int n, int* rec, list Rods, int RodsSize)
{
    if(n>0)
    {
        if(n==rec[n])
            printf("%d ", n);
        else
        {
            RodCutting_Method1_Retrieve(rec[n], rec, Rods, RodsSize);
            RodCutting_Method1_Retrieve(n-rec[n], rec, Rods, RodsSize);
        }
    }
    // for(int i=1; i<=n; i++)
    //     printf("%d %d\n", i, rec[i]);
}

int RodCutting_Method1(int n, list Rods, int RodsSize)
{
    int* rec=NULL;
    int ans=RodCutting_Method1_DP(n, Rods, RodsSize, &rec);
    printf("The Rod should be cut into slices with a length of the following:\n");
    RodCutting_Method1_Retrieve(n, rec, Rods, RodsSize);
    return ans;
}

int RodCutting_Method2(int n, list Rods, int RodsSize)
{
    qsort(Rods, RodsSize, sizeof(node), compare); // 以下做法需要先保证钢条按照长度升序排序
    int* dp=(int*)calloc(n+1, sizeof(int));
    int* rec=(int*)calloc(n+1, sizeof(int));

    int profit_max=0;
    int i=0, j=0, k=0;
    for(i=1; i<=n; i++)
    {
        profit_max=0;
        for(j=0; j<RodsSize && Rods[j].len<=i; j++)
        {
            if(Rods[j].price+dp[i-Rods[j].len]>profit_max)
            {
                profit_max=Rods[j].price+dp[i-Rods[j].len];
                rec[i]=Rods[j].len;
            }
        }
        dp[i]=profit_max;
        /*
            [动态规划 思路2]
                dp[i] 表示当前长度为 i 的钢条的最大利润.
                每一次都把问题拆分成两个子问题: i 一定是通过 长度为 j 的钢条和长度为 i-j 的钢条进行售卖的
                注意这里和[思路 1]的不同之处就在于 j 的范围. 其实可以进一步缩小范围: j只限制在那些可以单独售卖的钢条的长度.
                因此, 可以写出递推式:
                    dp[i]=max(price[j]+dp[i-j]) 
                    其中, price[j]是已知条件中, 第 j 个可以单独售卖的钢条的价格. len[j]为第 j 个可以单独售卖的钢条的长度.
            
            [回溯]
                即如何确定最大利润时的切分方式?
                设置 rec[] 数组进行回溯, rec[i]=Rods[j].len 表示当前长度为 i 的钢条取得最大利润时, 被切割并拿出去售卖部分的长度len[j]
                其中 len[j] 为第 j 个可以单独售卖的钢条的长度.


            [时间复杂度分析]
                
                外层循环 O(n), 内层循环 O(m), 其中 m 为可以单独售卖的钢条的种类数（不同长度的钢条数量）.
                
                因此, 总时间复杂度 O(n*m), 优于[思路 1].

                上述分析没有考虑代码最上面的qsort排序算法. 如果输入数据已经按照升序排序的话, 则无需排序.
                如果考虑qsort的话, 时间复杂度需要进一步提升到O(n*logn+n*m).
        */
    }
    int ans=dp[n];

    int tmp=n;
    printf("The Rod should be cut into slices with a length of the following:\n");
    while(tmp>0)
    {
        printf("%d ", rec[tmp]);
        tmp-=rec[tmp];
    }
    free(dp);
    free(rec);
    return ans;
}

int main()
{
    int lenArr[]={1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int priceArr[]={1, 5, 8, 9, 10, 17, 17, 20, 24, 25};
    int arrSize=sizeof(lenArr)/sizeof(int);

    list Rods=(list)calloc(arrSize, sizeof(node));
    for(int i=0; i<arrSize; i++)
    {
        Rods[i].len=lenArr[i];
        Rods[i].price=priceArr[i];
    }
    int n=18;

    // 思路1
    int ans1=RodCutting_Method1(n, Rods, arrSize);
    printf("\nMaximum Profit: %d\n", ans1);

    printf("-----------------------------------\n");

    // 思路2
    int ans2=RodCutting_Method2(n, Rods, arrSize);
    printf("\nMaximum Profit: %d\n", ans2);

}