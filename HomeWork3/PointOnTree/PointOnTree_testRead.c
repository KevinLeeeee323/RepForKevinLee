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

struct dp_node
{
    int id;
    int dp_val;
};

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
        // 偷过点, 可以知道必然有父节点 id<子节点 id, 因此子节点深度计算前, 父节点 id 必然已经被计算过了
    }
    for(i=1; i<=n; i++)
        scanf("%d", &(nodeList[i].val));
    return nodeList;
}

int compare(const void* a, const void* b)
{
    int val_a=((tree)a)->val;
    int val_b=((tree)b)->val;
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

    // qsort(nodeList, n+1, sizeof(node), compare);
    printf("Read %d nodes\n", n);
    for(int i=n; i>=n-21; i--) 
    {
        printf("Node %d: parent=%d, val=%d, depth=%d\n", 
            nodeList[i].id, nodeList[i].fore, nodeList[i].val, nodeList[i].depth);
    }

}