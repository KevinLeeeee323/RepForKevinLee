#include <stdio.h>
#include <stdlib.h>
#define max(a, b) (((a)>(b))?(a):(b))
struct item
{
    int id;
    int val;
    int fore; // 父节点
    int depth;
};
typedef struct item node;
typedef struct item* tree;

tree myReadData(int n)
{
    tree nodeList=(tree)calloc(n+1, sizeof(node));
    nodeList[1].depth=1;
    nodeList[1].id=1;
    nodeList[1].fore=-1; // 根节点, 无父节点
    int i=0;
    int tmp=0;
    for(i=2; i<=n; i++)
    {
        scanf("%d", &tmp);
        nodeList[i].fore=tmp; // 父节点
        nodeList[i].id=i;
        nodeList[i].depth=nodeList[tmp].depth+1; 
        // 偷点过, 可以知道必然有父节点 id<子节点 id, 因此子节点深度计算前, 父节点 id 必然已经被计算过了
    }
    for(i=1; i<=n; i++)
        scanf("%d", &nodeList[i].val);
    return nodeList;
}

int compare(const void* a, const void* b)
{
    int val_a=((tree)a)->depth;
    int val_b=((tree)b)->depth;
    return val_a-val_b; // 按照深度升序排序
}

int main()
{
    int n;
    scanf("%d", &n);
    tree nodeList=myReadData(n); // 长度 0, 1, 2...n, nodeList[0]不用且所有值已通过 calloc 函数赋为0
    
    /*
        将节点按照层级排序并且按照深度分级别存储.
        首先对节点进行排序, 然后逐个统计节点深度信息, 并且通过如下方式表示:
        maxDepth: 节点中的最大深度. 认为根节点深度为 1.

        nodeDepList 是对原始nodeList 的另一种排序方式, 更方便后续使用.
        nodeDepList[i][j]表示, 深度为 i 的节点中的第 j 个.

        nodeDepList_ColSize[i]则表示深度为 i的节点的数量, 其实是在告诉 nodeDepList[i]中有多少个元素. 借鉴了 LeetCode 的接口表示方法.        
    */

    qsort(nodeList, n+1, sizeof(node), compare);
    int maxDepth=nodeList[n].depth;
    node** nodeDepList=(node**)malloc(sizeof(node*)*(maxDepth+1));  // 只存储其 id
    for(int i=0; i<=maxDepth; i++)
        nodeDepList[i]=(tree)calloc(n, sizeof(node));
    int* nodeDepList_ColSize=(int*)calloc(maxDepth+1, sizeof(int));
    // int* top=(int*)calloc(maxDepth+1, sizeof(int)); // 后续通过 top 来给 depth_id_ColSize 赋值
    int dep=0;
    for(int i=1; i<=n; i++)
    {
        dep=nodeList[i].depth;
        nodeDepList[dep][nodeDepList_ColSize[dep]++]=nodeList[i];
    }
    // for(dep=1; dep<=maxDepth; dep++)
    //     nodeDepList_ColSize[dep]=top[dep];

    // temporary debug
    // for(int i=1; i<=maxDepth; i++)
    //     for(int j=0; j<nodeDepList_ColSize[i]; j++)
    //         printf("depth of %d: %d\n", nodeDepList[i][j].id, i);

    // 
    /*
        动态规划部分. 大致思路是 AI 生成的
        dp[i][j]表示1~i 的最大点权和, 在选nodeDepList[i][j] 的情况下

        上面代码构建起了树结构, 可以为下面打下基础.

        目前能够通过几个数据点, 但是有两个点过不去, 而且有两个点超时了.
        下面要做的重要的事情, 就是搞清楚, dp[i][j]表示什么, 怎么计算, 最优子问题结构是怎样的

        以下是 AI 指出的思维漏洞:

        当前只考虑了：

        从i-1层转移（当i-1层有多个节点时）
        从i-2层转移（当i-1层只有一个节点时）

        但没考虑：

        从更早的层转移（比如i-3层）

        当前层不选任何节点的情况, 可以和 (i-2)的情况合并?


    */
    int** dp=(int**)malloc(sizeof(int*)*(maxDepth+1));

    node** save=(node**)malloc(sizeof(node*)*(maxDepth+1));
    for(int i=0; i<=maxDepth; i++)
        save[i]=(tree)calloc(2, sizeof(node));

    /*
        save[i][0]: dp[i][j]最大值所对应的值和id
        save[i][1]: dp[i][j]次大值所对应的值和id
        
        dp[i][j]=max(save[i-1][0], save[i-1][1], save[i-2][0]), 前提是要排除 i-1层最大值对应的节点是当前节点 nodeDepList[i][j]父节点的情况
    
        具体情况: 
        1. i==2 时, dp[2][j]=nodeDepList[2][j].val

        2. 当第 k 层只有一个节点, save[k-1][0]=save[k-1][1]
            2.1 当第 i-1 层只有一个节点, dp[i][j]=save[i-2][0]

        3. 如果 save[i-1][0]对应的节点是 nodeDepList[i][j]的父节点, 则:dp[i][j]=max(save[i-1][1], save[i-2][0]).
           这正是同时维护最大值和次大值的意义
        
    */

    for(dep=0; dep<=maxDepth; dep++)
        dp[dep]=(int*)calloc(nodeDepList_ColSize[dep], sizeof(int));
    dp[1][0]=nodeDepList[1][0].val;
    

    int tmp=0;
    for(int i=2; i<=maxDepth; i++)
    {
        for(int j=0; j<nodeDepList_ColSize[i]; j++)
        {
            tmp=0;
            if(i==2)
                dp[i][j]=nodeDepList[i][j].val;
            else
            {
                // if(nodeDepList_ColSize[i-1]==1) // 如果上一层只有一个, 那就得往上上一层看
                // {
                //     for(int k=0; k<nodeDepList_ColSize[i-2]; k++)
                //     {
                //         if(tmp<dp[i-2][k])
                //             tmp=dp[i-2][k];     
                //     }
                //     dp[i][j]=tmp+nodeDepList[i][j].val;
                // }
                // else // 从上一层中选一个最大的, 加上当前节点的权值 val
                // {
                //     for(int k=0; k<nodeDepList_ColSize[i-1]; k++)
                //     {
                //         if(nodeDepList[i][j].fore!=nodeDepList[i-1][k].id)
                //         {
                //             tmp=nodeDepList[i][j].val+dp[i-1][k];
                //             if(tmp>dp[i][j])
                //                 dp[i][j]=tmp;
                //         }
                //     }
                // }
            }
        }
    }

    int ans=0;
    for(int j=0; j<nodeDepList_ColSize[maxDepth]; j++)
        if(ans<dp[maxDepth][j])
            ans=dp[maxDepth][j];
    printf("%d\n", ans);


    // for(int i=1; i<=maxDepth; i++)
    // {
    //     for(int j=0; j<nodeDepList_ColSize[i]; j++)
    //         printf("%d ", dp[i][j]);
    //     printf("\n");
    // }
    free(nodeList);
    free(nodeDepList_ColSize);
    // free(top);
    for(int i=0; i<=maxDepth; i++)
        free(dp[i]), free(nodeDepList[i]);
    free(dp), free(nodeDepList);


}