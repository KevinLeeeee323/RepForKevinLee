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

void FindGreatestTwo(int* max1, int* max2, int* max1_id, int* max2_id, int* arr, int arrSize) 
{
    // only for arrSize>=2
    // 寻找一个长度>=2 的数组的最大值(max1)及其对应下标(max1_id), 以及 次大值(max2)及其对应下标(max2_id)
    if(arr[0]>arr[1])
        *max1=arr[0], *max2=arr[1], *max1_id=0, *max2_id=1;
    else
        *max1=arr[1], *max2=arr[0], *max1_id=1, *max2_id=0;

    for(int i=2; i<arrSize; i++)
    {
        if(arr[i]>*max1)
        {
            *max2=*max1;
            *max2_id=*max1_id;
            *max1=arr[i];
            *max1_id=i;
        }
        else if(arr[i]>*max2)
        {
            *max2=arr[i];
            *max2_id=i;
        }
    }
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
    node** nodeDepList=(node**)malloc(sizeof(node*)*(maxDepth+1));  // 按深度, 存储同一深度的节点

    struct dp_node** save=(struct dp_node**)malloc(sizeof(struct dp_node*)*(maxDepth+1)); 
    // save[i][0]: dp[i][j]最大值所对应的值和id
    // save[i][1]: dp[i][j]次大值所对应的值和id

    for(int i=0; i<=maxDepth; i++)
    {
        nodeDepList[i]=(tree)calloc(n, sizeof(node));
        save[i]=(struct dp_node*)calloc(2, sizeof(struct dp_node));
    }
    
    int* nodeDepList_ColSize=(int*)calloc(maxDepth+1, sizeof(int));
    // int* top=(int*)calloc(maxDepth+1, sizeof(int)); // 后续通过 top 来给 depth_id_ColSize 赋值
    int dep=0;
    for(int i=1; i<=n; i++)
    {
        dep=nodeList[i].depth;
        nodeDepList[dep][nodeDepList_ColSize[dep]++]=nodeList[i];
    }
    save[1][0].id=1;
    save[1][0].dp_val=nodeDepList[1][0].val;
    
    /*
        save[i][0]: dp[i][j]最大值所对应的值和id
        save[i][1]: dp[i][j]次大值所对应的值和id
        
        dp[i][j]=max(save[i-1][0], save[i-1][1], save[i-2][0]), 前提是要排除 i-1层最大值对应的节点是当前节点 nodeDepList[i][j]父节点的情况
    
        具体情况: 
        1. i==2 时, dp[2][j]=nodeDepList[2][j].val

        2. 当第 k 层只有一个节点, save[k-1][0]=save[k-1][1]
            2.1 当第 i-1 层只有一个节点, dp[i][j]=save[i-2][0]

        3. 如果 save[i-1][0]对应的节点是 nodeDepList[i][j]的父节点, 则: dp[i][j]=max(save[i-1][1], save[i-2][0]).
           这正是同时维护最大值和次大值的意义
    */
    
    int** dp=(int**)malloc(sizeof(int*)*(maxDepth+1));
    for(dep=0; dep<=maxDepth; dep++)
        dp[dep]=(int*)calloc(nodeDepList_ColSize[dep], sizeof(int));
    dp[1][0]=nodeDepList[1][0].val;
    
    for(int i=2; i<=maxDepth; i++)
    {
        for(int j=0; j<nodeDepList_ColSize[i]; j++)
        {
            if(i==2)
                dp[i][j]=nodeDepList[i][j].val;
            else
            {
                if(nodeDepList_ColSize[i-1]==1) // 如果上一层只有一个, 那就得往上上一层看
                    dp[i][j]=save[i-2][0].dp_val;
                else // 考虑 i-2 层最大的 dp 值和 i-1 层最大的 dp 值
                {
                    if(save[i-1][0].id==nodeDepList[i][j].fore) // save[i-1][0]对应的节点是 nodeDepList[i][j]的父节点, 这不能选
                        dp[i][j]=max(save[i-1][1].dp_val, save[i-2][0].dp_val)+nodeDepList[i][j].val;
                    else
                        dp[i][j]=max(save[i-1][0].dp_val, save[i-2][0].dp_val)+nodeDepList[i][j].val;
                }
            }
            
        }

        /*
            目前要做的:

            以下在一个新创建的文件上进行


            
            1. 第四个点仍然过不去.
            2. 改一下前面的内容, dp 部分应该没问题了:
                2.1 101 行 给 nodeDepList[i]分配的空间的太大了, 不行就先遍历一遍 nodeList, 确认 nodeDepList[i]应该有多少个(填好 nodeDepList_ColSize数组)
                2.2 91 行 qsort 使得复杂度飙升到 O(n * log n), 可能还是得搞一个 O(n)的方法
        
            3. 一切都完成后,再调整一下结构, 写一些注释
            4. 发给 ldj
        */



        // 维护 save[i][0], save[i][1], 最开始都初始化为 0
        if(nodeDepList_ColSize[i]==1) // 只有一个节点的情况.此时不用管 save[i][1], 后续用不到
        {
            save[i][0].dp_val=dp[i][0];
            save[i][0].id=nodeDepList[i][0].id;
        }
        else
        {
            int max1=0, max2=0; //max1-最大值, max2-次大值
            int max1_id=0, max2_id=0; //max1-id: 最大值所对应下标, max2-id: 次大值所对应下标
            FindGreatestTwo(&max1, &max2, &max1_id, &max2_id, dp[i], nodeDepList_ColSize[i]);
            save[i][0].dp_val=max1, save[i][0].id=nodeDepList[i][max1_id].id;
            save[i][1].dp_val=max2, save[i][1].id=nodeDepList[i][max2_id].id;
        }

    }

    int ans=save[maxDepth][0].dp_val;
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
        free(dp[i]), free(nodeDepList[i]), free(save[i]);
    free(dp), free(nodeDepList), free(save);
}