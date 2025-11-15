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
    for(int i=1; i<=maxDepth; i++)
        for(int j=0; j<nodeDepList_ColSize[i]; j++)
            printf("depth of %d: %d\n", nodeDepList[i][j].id, i);

    // 
    /*
        动态规划部分. 大致思路是 AI 生成的
        dp[i][0]表示1~i 的最大点权和, 在不选
    
    
    */
    int** dp=(int**)malloc(sizeof(int*)*(maxDepth+1));
    for(int i=0; i<=maxDepth; i++)
        dp[i]=(int*)calloc(2, sizeof(int));
    dp[1][0]=0, dp[1][1]=nodeDepList[1][0].val;
    
    int tmp=0;
    
    for(int i=2; i<=maxDepth; i++)
    {
        dp[i][0]=max(dp[i-1][0], dp[i-1][1]);
        for(int j=0; j<nodeDepList_ColSize[i]; j++)
        {
            tmp=nodeDepList[i][j].val+dp[i-1][0];
            if(tmp>dp[i][1])
                dp[i][1]=tmp;
        }
    }

    int ans=max(dp[maxDepth][0], dp[maxDepth][1]);
    printf("%d", ans);

    free(nodeList);
    free(nodeDepList_ColSize);
    // free(top);
    for(int i=0; i<=maxDepth; i++)
        free(dp[i]), free(nodeDepList[i]);
    free(dp), free(nodeDepList);

}