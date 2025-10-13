#include <stdio.h>
#include <stdlib.h>

/*
    0-1 背包问题.
    问题场景:
    有如下 n 件商品, 每件商品各一件:a_1, a_2, ...a_n
    每件商品 a_i 有自己的价值 v_i 和体积 p_i, 分别由数组 v 和 p 记录
    现给定一个背包, 背包容积 C, 要求从上述 n 件商品中选出若干件, 使得这些商品总体积不超过背包容积 C, 同时使这些选出的商品的价值最大

    解决方法:
    [方法 1] 纯暴力枚举, 一件一件尝试. 考虑所有可能, 共有 2^n-1种(不考虑什么都不拿的那种)

    [方法 2] 递归枚举
        设 背包剩余容量为x, 当选择范围是 1~i 号商品时, 总价值最大为KnapSack(i, x)
        则:
            KnapSack(i, x)= KnapSack(i-1, x), 当且仅当没有选中 i 号商品;
            KnapSack(i, x)=KnapSack(i-1, x-v_i)+p_i, 当且仅当选中了 i 号商品, 因此要减去 i 号商品的重量, 加上其价值
        由于 KnapSack 代表的是 当前的最大价值, 因此:
        KnapSack(i, x)=max(KnapSack(i-1, x), KnapSack(i-1, x-v_i)+p_i), 当 x-v_i>=0 时
        特别的, 当x-v_i<0, KnapSack(i, x)=Knap(i-1, x)

        这样递归的去计算 Knap(n, C), 得出最终答案
        递归终止条件:  x<0

        这样的递归算法, 计算一个 Knap(i, x)涉及到两个子部分, 因此 Knap(n, C)复杂度 2^n

    [方法 3] 记忆化搜索
        上面的递归会涉及到很多重复计算的部分, 因此通过记忆化搜索的方式降低计算成本.
        通过二维数组P(n, c)存储KnapSack(n, C), 每次调用直接取值求 max 即可.

        时间复杂度为 O(n*C), 空间复杂度为 O((n+1)*(C+1))(需要给数组填上一些辅助 0)
        具体见:https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=19 的6:50s图

        如何记录获得最大价值时, 到底选了哪些商品?
        使用另一个二维数组rec, 通过回溯追查到最优解的时候, 是否选择了那个商品.
        rec[i][j]=1, 表示在背包剩余容量为 j 时, 选择了当前第 i 个商品;rec[i][j]=0 则表示没选
*/
#define max(a, b) (((a) > (b)) ? (a) : (b))
#define MAX 2147483647
int KnapSack_recursive(int i_th, int volume, int *v, int *p) // 方法 2: 递归枚举
{
    // 取编号为 1~i_th 之内的商品, 返回起不超过 当前剩余背包容积volume的最大价值
    if (i_th == 1)
        return (v[1] > volume) ? 0 : p[1];
    else
    {
        int total_price1 = KnapSack_recursive(i_th - 1, volume, v, p); // 不选 i_th 号商品, 考虑前 1~i_th 号商品
        if (volume < v[i_th])
            return total_price1;
        else
        {
            int total_price2 = KnapSack_recursive(i_th - 1, volume - v[i_th], v, p) + p[i_th]; // 选 i_th 号商品, 再考虑前 1~i_th 号商品
            return max(total_price1, total_price2);
        }
    }
}

int KnapSack_memoization(int n, int C, int *v, int *p, int **item_save, int *top) // 方法 3:记忆化搜索
{
    int **pack = (int **)malloc(sizeof(int *) * (n + 1));
    int **rec = (int **)malloc(sizeof(int *) * (n + 1));

    int i = 0, j = 0;
    for (i = 0; i <= n; i++)
    {
        pack[i] = (int *)calloc(C + 1, sizeof(int)); // 置零
        rec[i] = (int *)calloc(C + 1, sizeof(int));
    }
    int tmp1 = -1, tmp2 = -1;
    for (i = 1; i <= n; i++)
    {
        for (j = 1; j <= C; j++)
        {
            // 实际上应该分 i==1 讨论, 但是考虑到pack[0][j]==pack[i][0]==0, 可以不,直接写下面的就行
            // 二维数组rec, 通过回溯追查到最优解的时候, 是否选择了那个商品
            // rec[i][j]=1, 表示在背包剩余容量为 j 时, 选择了当前第 i 个商品;rec[i][j]=0 则表示没选
            if (j < v[i])
            {
                pack[i][j] = pack[i - 1][j];
                rec[i][j] = 0;
            }
            else
            {
                tmp1 = pack[i - 1][j];
                tmp2 = pack[i - 1][j - v[i]] + p[i];
                if (tmp1 < tmp2)
                {
                    pack[i][j] = tmp2;
                    rec[i][j] = 1;
                }
                else
                {
                    pack[i][j] = tmp1;
                    rec[i][j] = 0;
                }
            }
        }
    }
    
    /*
        // debug 使用
        // 打印动态规划矩阵
        for (int i = 0; i <= n; i++)
        {
            for (int j = 0; j <= C; j++)
                printf("%d ", pack[i][j]);
            printf("\n");
        }

        // 打印动态规划矩阵
        for (int i = 0; i <= n; i++)
        {
            for (int j = 0; j <= C; j++)
                printf("%d ", rec[i][j]);
            printf("\n");
        }
    */

    /*
        进行回溯, 通过 rec 数组 查找那些被选择了, 并且将所有选择了的存储在 *item_save这个一维数组中. *top指向栈顶.
        具体来说, 如果当前 rec[i][j]=1, 则说明这个商品在剩余背包容量为 j 时被选择了, 将其添加到*item_save 中
        并且考虑 rec[i-1][j-v[i]], 查看没有选i 时的最优决策下, 选了什么物品
        详见 https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=19  的15:40 秒
        回溯部分时间复杂度 O(n)
    */
    int tmp_volume=C;
    int id_cnt=n;
    *item_save=(int*)calloc(n+1, sizeof(int));
    *top=0;
    while(id_cnt>0)
    {
        if(rec[id_cnt][tmp_volume]==1)
        {
            tmp_volume-=v[id_cnt];
            (*item_save)[++(*top)]=id_cnt;
        }
        id_cnt--;
    }

    int ans = pack[n][C];
    free(pack);
    free(rec);
    return ans;
}

/*---------------------------------------------*/

// 以下是测试代码
int main()
{
    int volume[] = {-100, 4, 1, 6, 5};
    int price[] = {-100, 4, 5, 12, 9};

    // int volume[] = {-100, 3, 4, 5, 4, 10};
    // int price[] = {-100, 2, 9, 10, 9, 24};
    int n = sizeof(price) / sizeof(int) - 1;
    // volume[0], price[0]都是占位, 不参与运算. 函数中的下标运算 1~n

    int C = 10;

    // 方法1
    printf("%d\n", KnapSack_recursive(n, C, volume, price));

    // 方法2
    int *item_save = NULL;
    int top = -1;
    printf("%d\n", KnapSack_memoization(n, C, volume, price, &item_save, &top));
    if(top>=1)
    {
        printf("the selected items are: (index of the items are listed below)\n");
        for(int i=1; i<=top; i++)
            printf("%d ", item_save[i]);
    }
    else
        printf("no item is selected.\n");
}