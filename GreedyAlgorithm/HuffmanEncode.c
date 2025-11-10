#include <stdio.h>
#include <stdlib.h>

/*
    Huffman 编码.
    给定n 个字符: a_1, a_2, ... a_n, 第 i个字符a_i出现的频率 f_i (通过数组a, fre 存储)
    构建 Huffman 树, 并且返回每个字符对应的编码结果.

*/
struct item
{
    char c; // character
    int fre; // frequency
    struct item* left;
    struct item* right;
    char* str; // huffman_coding
};
typedef struct item node;
typedef struct item* tree;


void swap(tree a, tree b)
{
    node tmp=*a;
    *a=*b;
    *b=tmp;
}

void adjustHeap(int id, int right, tree arr) //将以 id 为根节点的二叉树调整成小顶堆
{
    /*
        适用前提:
        以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树都已经分别是小顶堆了.
        只是 id , 2*id+1, 2*id+2 的大小顺序可能还需要调整.
        由于调整后可能使得以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树不满足小顶堆特性,
        因此需要借助这个 while 循环, 递归的调整.
    */
    int child_id=2*id+1; //左子节点
    int min_id=child_id; // 记录左右节点中数值最小的节点的下标
    while(child_id<=right)
    {
        if(child_id+1<=right && arr[child_id+1].fre<arr[child_id].fre) // 如果右子节点存在且数值<左子节点
            min_id++; //min_id=2*id+2, 代表右子节点
        if(arr[id].fre>arr[min_id].fre)
        {
            swap(&arr[id], &arr[min_id]);
            id=min_id; // 处理调整后可能破坏"以 max_id 为下标的根节点的二叉树是一个小顶堆"的性质
            child_id=2*id+1; // 更新左右子节点信息
            min_id=child_id;
        }
        else
            break;
    }
}

void buildHeap(int left, int right, tree arr) //构建堆
{
    for(int i=(right-1)/2; i>=left; i--)
        adjustHeap(i, right, arr);
    // (right-1)/2 可以求出当前有子节点的最小节点下标
    // 通过 i-- 的方式调用, 可以保证adjustHeap的适用前提:"以 2*id+1 为根节点和以 2*id+2 为根节点的二叉树都已经分别是小顶堆了"
}


tree BuildHuffmanTree(char* a, int* fre, int n)
{
    tree list=(tree)malloc(sizeof(node)*n);
    tree tmp=NULL;
    for(int i=0; i<n; i++)
    {  
        list[i].c=a[i];
        list[i].fre=fre[i];
        list[i].left=NULL;
        list[i].right=NULL;
        list[i].str=NULL;
    }

    int tmp1=0, tmp2=0;
    /*
    1. 构建小顶堆,也许需要调整上面函数的逻辑, 比如大于小于号
    2. 下面代码循环中要加上' a. 第一次调用 ExtractMin 操作：取出堆顶节点 x（当前频次最小，fre1 = x.freq），此时调整堆以维持小顶堆性质（复杂度 O(log n)）。
                            b. 第二次调用 ExtractMin 操作：取出新的堆顶节点 y（当前频次次小，fre2 = y.freq），再次调整堆（复杂度 O(log n)）。
                            c. 合并节点：新建一个父节点 z，设置 z.freq = x.freq + y.freq，z.left = x，z.right = y（按 fre1 ≤ fre2 约定左小右大）。
                            d. 将父节点 z 插入小顶堆，调整堆以维持性质（复杂度 O(log n)）。'
                        的部分
        
    */

    buildHeap(0, n-1, list);
    for(int i=1; i<n; i++)
    {
        swap(&list[0], &list[n-i]);
        tmp1=list[n-i].fre;
        adjustHeap(0, n-i-1, list);
    
        // maybe n-i-2<0?
        swap(&list[0], &list[n-i-1]);
        tmp2=list[n-i-1].fre;
        adjustHeap(0, n-i-2, list);
        
        tmp=(tree)malloc(sizeof(node));
        tmp->fre=tmp1+tmp2;
        
        tmp->left=&list[n-i];
        tmp->right=&list[n-i-1];

        list[n-i-1]=*tmp;


        /*
            这里按道理说要重新构建小顶堆, 需要调用buildHeap(0, arrSize-i-1, arr);
            但实际上调用 adjustHeap()就可以满足需要.
            经过上一行的 swap()后, 以 2*0+1和 2*0+2 为根节点的二叉树都仍然是小顶堆. 但 0, 1, 2 三个节点上数值的大小关系不定.
            只需要针对 id=0的节点调整就可以, 符合 adjustHeap()使用条件.
        */ 
    }
    // 时间复杂度:O(n*logn)

    /*
        Huffman 编码的一个关键在于, 每次选出频次最少的两个节点(对应频次 fre1, fre2).
        如果 fre1<fre2, 那就把 fre1 对应的 作为左子节点,  fre2 对应的作为右子节点. 其父节点频次 fre1+fre2.( PPT 上, 左子节点频次<右子节点频次, 但也可以反过来)

        每次选出最小的两个频次, 可以通过维护一个小顶堆实现. 
        每次取出堆顶元素(即当前堆中最小元素), 取出后再维护堆, 然后再取. 这样就可以取到两个最小频次元素.
        将这两个分别作为左, 右子节点放到一个根节点下, 将根节点纳入

        Huffman 编码的一个关键在于, 每次选出频次最少的两个节点(对应频次 fre1, fre2).
        如果 fre1<fre2, 那就把 fre1 对应的节点作为左子节点, fre2 对应的节点作为右子节点. 
        其父节点频次为 fre1+fre2（PPT中左子节点频次<右子节点频次的约定可简化编码规则，实际也可反过来，但需保持一致性）。

        每次选出最小的两个频次, 可以通过维护一个小顶堆实现：
        1. 初始化小顶堆：将所有字符节点（仅含字符和频次，无左右子树）插入堆中，堆的排序依据为节点的频次（小顶堆特性：堆顶始终是当前频次最小的节点）。
        2. 循环提取并合并节点：
            a. 第一次调用 ExtractMin 操作：取出堆顶节点 x（当前频次最小，fre1 = x.freq），此时调整堆以维持小顶堆性质（复杂度 O(log n)）。
            b. 第二次调用 ExtractMin 操作：取出新的堆顶节点 y（当前频次次小，fre2 = y.freq），再次调整堆（复杂度 O(log n)）。
            c. 合并节点：新建一个父节点 z，设置 z.freq = x.freq + y.freq，z.left = x，z.right = y（按 fre1 ≤ fre2 约定左小右大）。
            d. 将父节点 z 插入小顶堆，调整堆以维持性质（复杂度 O(log n)）。
        3. 终止条件：当堆中仅剩一个节点时，该节点即为 Huffman 树的根节点，循环结束。

    */

}

void PrintHuffmanEncoding(tree Huffman)
{
    /*
        编码生成规则：
            从根节点出发，对每个节点的左子树路径标记为 "0"，右子树路径标记为 "1"（因左子节点频次≤右子节点，该规则可固定）。
            遍历至叶子节点（原始字符节点）时，路径上的 "0"/"1" 序列即为该字符的 Huffman 编码。
            例如：左-左-右路径对应编码 "001"。

    */
    if(Huffman!=NULL)
    {
        PrintHuffmanEncoding(Huffman->left);
        if(Huffman->str!=NULL)
            printf("%c: %s", Huffman->c, Huffman->str);
        PrintHuffmanEncoding(Huffman->right);
    }
}


int main()
{
    char a[]={'a', 'b', 'c', 'd', 'e', 'f'};
    int fre[]={45, 13, 12, 16, 9, 5};

}