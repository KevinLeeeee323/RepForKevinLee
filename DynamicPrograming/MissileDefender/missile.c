#include <stdio.h>
#include <stdlib.h>

/*
    [题目描述]
        见同目录下 Problem.md

    [思路]
        自己最开始想的那个思路是贪心算法, 是错误的, 放在最下方的多行注释里了.
        (那里面, 两个系统序号是 0 和 1)

        下面说的都是正确的算法, 基于能够在今天任意时刻知道今天这一天中所有导弹的发射顺序.
        思路仍然是基于动态规划.
        以下, 两个系统序号是 1 和 2

        设立导弹结构体, 其中含有dist1, dist2 两部分, 分别对应其到系统 1 和系统 2 的距离. 距离通过 读取数据的 readData() 函数和 计算距离的 genDist() 函数得出.
        先对这些导弹到系统 1 的距离按照升序排序.(qsort)

        然后, 设定一维数组 sys2Cost, sys2Cost[i]表示系统 2 从第 i 个导弹其开始拦截, 一直拦截到第 N 个导弹的成本/代价(排序后的导弹), 也就是, 第 i 到第 N 个导弹中到系统 2 的最大距离.
        与此同时, sys2Cost[i]的时候, 对应的系统 1 的成本就是拦截 1~(i-1)这些导弹的成本.
        由于导弹按照到系统 1 的距离升序排序, 这一项成本也就是编号为 i-1 的导弹(排序后)到系统 1 的距离, 记为 sysCost[i]. i=1, 2, ... N+1

        特别的:
            当 i=N+1时, sys2Cost[N+1]=0
            当 i=1 时, sys1Cost=0
        
        维护最小成本 min_cost=min(sys1Cost[i]+sys2Cost[i]), 得到最终答案.

        注: 其实 sys1Cost 也可以开一个数组存储, 但似乎没必要
        如何进行回溯?
            看 DP 部分 for 循环. 难度不大.

    [时间复杂度分析]
        readData() 函数时间复杂度 O(N).
        missileDefend_DP() 函数:
            快速排序 qsort 算法部分, 复杂度 O(N*logN);
            递推式求解部分, 复杂度 O(N). 即使加上回溯, 也是 O(N)复杂度.

        因此, 总的复杂度 O(N*logN).
    
    [空间复杂度分析]
        若干长度为 O(N)的一维数组, 空间复杂度 O(N).

*/
#define max(a, b) (((a)>(b))?(a):(b))
#define min(a, b) (((a)<(b))?(a):(b))

struct MissileNode
{
    int dist1;
    int dist2;
};
typedef struct MissileNode node;
typedef struct MissileNode* list;

int compare(const void* a, const void* b)
{
    int a_dist1=(*(list)a).dist1;
    int b_dist1=(*(list)b).dist1;
    return a_dist1-b_dist1;
}

int genDist(int x0, int y0, int x_target, int y_target) // 计算导弹和系统之间的距离
{
    int x_square=(x0-x_target)*(x0-x_target);
    int y_square=(y0-y_target)*(y0-y_target);
    return x_square+y_square;
}

list readData(int* x1, int* y1, int* x2, int* y2, int* N)
{
    scanf("%d%d%d%d", x1, y1, x2, y2);
    scanf("%d", N);
    list missileList=(list)calloc((*N+1), sizeof(node));
    int x=0, y=0;
    missileList[0].dist1=0;
    missileList[0].dist2=0;
    for(int i=1; i<=*N; i++)
    {
        scanf("%d%d", &x, &y);
        missileList[i].dist1=genDist(*x1, *y1, x, y);
        missileList[i].dist2=genDist(*x2, *y2, x, y);
    }
    return missileList;
}

int missileDefend_DP(int x1, int y1, int x2, int y2, list Missiles, int N)
{
    qsort(Missiles+1, N, sizeof(node), compare); // 对一天中所有导弹按照距离系统1 的距离升序排序 
    // 第 Missiles[0]只是起到占位作用, 没有实际意义, 不参与计算, 因此从 Missiles+1 即 Missiles[1]开始排序
    int* sys2Cost = (int*)calloc(N +2, sizeof(int)); // sys2Cost[i] 表示系统 2 从排序后的第 i 个导弹开始拦截的代价
    sys2Cost[N+1]=0; // 表示系统 2 不参与任何导弹的拦截, 成本为 0
    
    int i=0;
    for (i = N; i >= 1; i--) 
        sys2Cost[i] = max(sys2Cost[i + 1], Missiles[i].dist2);
    
    int sys1Cost = 0; 
    int min_cost = sys2Cost[1];
    // sys1Cost 表示系统 1 拦截排序后的第 1 个到第 i-1 个导弹的代价, 随着下面 for 循环中i 的更新而更新
    // sys1Cost 初始化为 0, 是指系统 1 一个也不拦截的情况下, 系统 2 拦截所有的导弹
    // min_Cost=min(sys1Cost+sys2Cost) 初始化时最好是其中一个可能是最小值的值. 这里 对应 i=1, sys1Cost=0

    // 寻找最小代价: 系统1覆盖前1~(i-1)个，系统 2 从第 i 个开始, 覆盖剩下的. 上面一行已经算上了 i=1.
    for (i = 2; i <= N+1; i++) 
    {
        sys1Cost = max(sys1Cost, Missiles[i-1].dist1);
        min_cost = min(min_cost, sys1Cost + sys2Cost[i]);
        /*
            这里在 min_cost> sys1Cost + sys2Cost[i]的时候,设置一个跟踪变量 i0, 即可进行回溯, 知道前 1~(i0-1) 个导弹要被系统 1 拦截.
            至于如何知道被拦截的这些导弹在排序前的真实到达顺序?
            在结构体中添加一项 struct Missile.id, 在 readData()时写入, 完成递推并且寻得最小成本后, 打印出来就行.
        */
    }
    
    free(sys2Cost);
    return min_cost;
}

int main()
{
    int x1=0, y1=0, x2=0, y2=0;
    int N=0;
    list Missiles=readData(&x1, &y1, &x2, &y2, &N);
    int ans=missileDefend_DP(x1, y1, x2, y2, Missiles, N);
    printf("%d", ans);

    // debug info
    // printf("x1:%d y1:%d x2:%d y2:%d N:%d\n", x1, y1, x2, y2, N);
    // for(int i=0; i<N; i++)
    //     printf("%d %d\n", missileLocation[0][i], missileLocation[1][i]);
}


/*
    以下是一个不适用于这道题的错误做法, 混淆视听. 以至于在小样本的情况下, 这个算法也是对的:
    这个算法的本质是贪心算法, 可以理解成, 在不知道之后导弹的数量和位置时, 选择当前拦截后总成本代价最小的方案
    不适用于这个题的地方, 也就在于这个"不知道", 因为实际上题目默认了可以知道

    int** readData(int* x1, int* y1, int* x2, int* y2, int* N)
    {
        scanf("%d%d%d%d", x1, y1, x2, y2);
        scanf("%d", N);
        int** location=(int**)malloc(sizeof(int*)*2);
        int i=0, j=0;
        location[0]=(int*)calloc((*N+1), sizeof(int)); // 存储各导弹的 x 坐标
        location[1]=(int*)calloc((*N+1), sizeof(int)); // 存储各导弹的 y 坐标
        for(int i=1; i<=*N; i++)
            scanf("%d%d", &location[0][i], &location[1][i]);
        return location;
    }

    // genDist() 函数定义同上

    int missileDefend_Greedy_DP(int x1, int y1, int x2, int y2, int** arr, int N)
    {
        int** dp=(int**)malloc(sizeof(int*)*2);
        dp[0]=(int*)calloc((N+1), sizeof(int)); // 存储各导弹的 x 坐标
        dp[1]=(int*)calloc((N+1), sizeof(int)); // 存储各导弹的 y 坐标
        // dp[i][j]表示 i 号导弹系统拦截 1~j 号导弹所需的最少距离
        int dist1=0, dist2=0;
        for(int i=1; i<=N; i++)
        {
            dist1=genDist(x1, y1, arr[0][i], arr[1][i]);
            dist2=genDist(x2, y2, arr[0][i], arr[1][i]);
            if(dist1<=dp[0][i-1] || dist2<=dp[1][i-1]) // 如果现行距离以内能拦截到, 就两个都不更新
            {
                dp[0][i]=dp[0][i-1];
                dp[1][i]=dp[1][i-1];
            }
            else // 如果现行距离以内拦截不到, 那就更新
            // 更新的原则: 每次只更新一个, 且保证更新后, 当前的总成本是最小的
            {
                if(dist1+dp[1][i-1]<=dist2+dp[0][i-1]) // 更新系统 0 的成本更小, 那就更新系统 0
                {
                    dp[0][i]=dist1;
                    dp[1][i]=dp[1][i-1];
                }
                else // dist1+dp[1][i-1]>dist2+dp[0][i-1] // 更新系统 1 的成本更小, 那就更新系统 1
                {
                    dp[0][i]=dp[0][i-1];
                    dp[1][i]=dist2;
                }
            }
        }
        return dp[0][N]+dp[1][N];
    }

    int main()
    {
        int x1=0, y1=0, x2=0, y2=0;
        int N=0;
        int** missileLocation=readData(&x1, &y1, &x2, &y2, &N);
        int ans=missileDefend_DP(x1, y1, x2, y2, missileLocation, N);
        printf("%d", ans);
    }
*/