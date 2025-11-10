#include <stdio.h>
#include <stdlib.h>

/*
    部分背包问题.

    [问题描述] 假设现在有n 个商品: a_0, a_1, ...a_{n-1}.
        每个商品 a_i对应的价值是 p_i, 对应的体积 p_i. 分别通过数组 p[]和 v[]存储.

        现在有一个容量为 C 的背包.可以往背包中塞物品, 使之不超过背包的总容量.
        每个商品可以无限细度分割后放入背包.

        求放进背包的商品的总的价值的最大值, 以及存放方式(第 i 个商品放进背包的比重 pro_i, 0<=pro_i<=1, pro_i=1 表示整个放进去了, pro_i=0 表示没放进去, pro_i 在 0 和 1 之间表示放进去了一部分(经过分割)).

        e.g. 商品A 整个的体积是 3, 价值是 4.如果只把A 的 1/3 放进背包, 则 A 放进背包部分的价值是 4/3.
        
    [思路]贪心算法
        优先装那些[性价比]高的商品, 而且是尽可能的整个装进去. 商品 a_i 的[性价比]定义为: p_i/v_i.
        等到最后装不下整个的, 那就把能装进背包的部分装进去(将物体分割成能装进去的部分).

        之所以这样的方法被称作贪心[算法], 是因为其每一步都试图选择[当下的最优解], 而且最终得到结果就是[全局最优解].
        贪心算法[不一定]最终能够得出全局最优解, 换而言之, 有些题应用贪心[策略]是错的. 这种策略会导向不是[全局最优解]的结局.
        在那些应用了贪心[策略], 且最终证明该[策略]能够导向最优解的情境下, 我们称之为贪心[算法]. 

        这道题可以证明, 这样选取, 最终出来的就是最优解.
        证明方式参考网课链接: https://www.bilibili.com/video/BV1TC4y1W7wC?spm_id_from=333.788.videopod.episodes&vd_source=c8e4e809f91f46885a44be8339a7976c&p=33

    [复杂度分析]
        对于性价比进行排序, n 个物体的排序复杂度 O(n*log(n)).
        后续遍历物品直到背包装满, 最坏情况 n 个商品都被遍历到, O(n).

        因此, 总的复杂度 O(n*log(n)).
*/

typedef struct node
{
    int id;
    int volume;
    int price;
}item, *list;

int compare(const void* a, const void* b)
{
    list ptr_a=(list)a;
    list ptr_b=(list)b;

    double pv_a=ptr_a->price*1.0/ptr_a->volume; // a 的性价比
    double pv_b=ptr_b->price*1.0/ptr_b->volume; // b 的性价比
    if(pv_a>=pv_b)
        return -1;
    else // pv_a<pv_b
        return 1;
    
}

double FractionalKnapsack(int n, int C, int* v, int* p, double** proportion)
{
    int i=0;
    list items=(list)malloc(sizeof(item)*n);
    for(i=0; i<n; i++)
    {
        items[i].id=i;
        items[i].price=p[i];
        items[i].volume=v[i];
    }
    qsort(items, n, sizeof(item), compare);

    *proportion=(double*)calloc(n, sizeof(double));
    
    double maxPrice=0;
    int tmp_C=C;
    for(i=0; tmp_C>0 && i<n; i++)
    {
        if(tmp_C>=items[i].volume)
        {
            (*proportion)[items[i].id]=1;
            tmp_C-=items[i].volume;
            maxPrice+=items[i].price;
        }
        else // tmp_C<items[i].volume
        {
            double ratio=tmp_C*1.0/items[i].volume;
            (*proportion)[items[i].id]=ratio;
            maxPrice+=items[i].price*ratio;
            tmp_C=0;
        }
    }
    free(items);
    return maxPrice;
}


/*--------------------------Test Case--------------------------*/
int main()
{
    int volume[]={2, 4, 5, 6, 8};
    int price[]={4, 6, 7, 6, 10};
    int size=sizeof(volume)/sizeof(int);
    int C=10;

    double* proportion=NULL;
    double maxPrice=FractionalKnapsack(size, C, volume, price, &proportion);
    printf("maxPrice in the backpack: %lf\n", maxPrice);
    for(int i=0; i<size; i++)
        printf("no.%d good: %lf in the backpack\n", i, proportion[i]);
}