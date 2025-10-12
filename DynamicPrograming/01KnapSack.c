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
        使用另一个二维数组, 通过回溯追查到最优解的时候, 是否选择了那个商品.
        [回溯记录这里不太懂, 需要再看一下]
*/
# define max(a, b) (((a)>(b))?(a):(b))

int KnapSack_recursive(int n, int C, int* v, int* p) //方法 2: 递归枚举
{


}


int KnapSack_memoization(int n, int C, int* v, int* p) // 方法 3:记忆化搜索
{
    int** pack=(int*)malloc(sizeof(int*)*(n+1));
    for(int i=0; i<=n; i++)
        pack[i]=(int*)calloc(C+1, sizeof(int)); //置零




    
    // 回溯部分代码应该也在这里面, 确定哪些商品被选中
    int ans=pack[n][C];
    free(pack);
    return ans;
}









/*---------------------------------------------*/

// 以下是测试代码
int main()
{

}