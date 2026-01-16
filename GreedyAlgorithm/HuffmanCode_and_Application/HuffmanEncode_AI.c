#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#define MaxCharCnt 256 // 最多 256 个字符需要标识, 对应 扩展 ASCII 码数量
/*
    Huffman 编码.
    给定n 个字符: a_1, a_2, ... a_n, 第 i个字符a_i出现的频率 f_i (通过数组a, fre 存储)
    构建 Huffman 树, 并且返回每个字符对应的编码结果.

    过程如下:
    1. 构建 Huffman 树:
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
    
    2. 生成并且存储每个字符的 Huffman 编码.
        递归的生成, 本质是一个 DFS.
    
*/

// 定义节点结构
typedef struct Node
{
    char c;  // character
    int fre; // frequency
    struct Node *left;
    struct Node *right;
} node, *tree;

// 交换两个节点
void swap(tree a, tree b)
{
    node tmp = *a;
    *a = *b;
    *b = tmp;
}

// 调整小顶堆
void adjustHeap(int id, int right, tree arr)
{
    int child_id = 2 * id + 1;
    int min_id = child_id;
    while (child_id <= right)
    {
        if (child_id + 1 <= right && arr[child_id + 1].fre < arr[child_id].fre)
            min_id++;
        if (arr[id].fre > arr[min_id].fre)
        {
            swap(&arr[id], &arr[min_id]);
            id = min_id;
            child_id = 2 * id + 1;
            min_id = child_id;
        }
        else
        {
            break;
        }
    }
}

// 构建小顶堆
void buildHeap(int left, int right, tree arr)
{
    for (int i = (right - 1) / 2; i >= left; i--)
        adjustHeap(i, right, arr);
}

// 向上调整堆（用于插入新节点后维护小顶堆）
void adjustUp(int id, tree arr)
{
    while (id > 0)
    {
        int parentId = (id - 1) / 2;
        if (arr[id].fre < arr[parentId].fre)
        {
            swap(&arr[id], &arr[parentId]);
            id = parentId;
        }
        else
        {
            break;
        }
    }
}

// 提取堆顶最小节点
tree extractMin(int *heapSize, tree arr)
{
    // 为提取的节点分配独立内存，避免依赖堆数组
    tree minNode = (tree)malloc(sizeof(node));
    *minNode = arr[0];           // 拷贝堆顶节点的值
    arr[0] = arr[*heapSize - 1]; // 用最后一个元素填补堆顶
    (*heapSize)--;
    adjustHeap(0, *heapSize - 1, arr); // 向下调整堆
    return minNode;                    // 返回独立指针
}

tree BuildHuffmanTree(char *a, int *fre, int n)
{
    if (n <= 0)
        return NULL;

    // 1. 初始化堆数组（大小为2n-1，容纳所有原始节点和合并节点）
    tree heap = (tree)malloc(sizeof(node) * (2 * n - 1));
    int heapSize = n; // 初始堆大小：n个原始节点

    // 初始化原始节点
    for (int i = 0; i < n; i++)
    {
        heap[i].c = a[i];
        heap[i].fre = fre[i];
        heap[i].left = NULL;
        heap[i].right = NULL;
    }

    // 2. 构建初始小顶堆
    buildHeap(0, heapSize - 1, heap);

    // 3. 循环合并n-1次
    for (int i = 0; i < n - 1; i++)
    {
        // a. 提取第一个最小节点（返回独立指针）
        tree x = extractMin(&heapSize, heap);
        // b. 提取第二个最小节点（返回独立指针）
        tree y = extractMin(&heapSize, heap);

        // c. 合并为新节点（动态分配，指针关联子节点）
        tree z = (tree)malloc(sizeof(node));
        z->c = '\0'; // 中间节点无字符
        z->fre = x->fre + y->fre;
        z->left = x;  // 左子树：频次较小的节点（x->fre <= y->fre）
        z->right = y; // 右子树：频次较大的节点

        // d. 将新节点插入堆尾，并向上调整堆
        heap[heapSize] = *z; // 拷贝z的值到堆数组（仅用于堆排序）
        heapSize++;
        adjustUp(heapSize - 1, heap);
    }

    // 4. 堆中最后一个节点即为根节点（动态分配，返回给调用者）
    tree root = (tree)malloc(sizeof(node));
    *root = heap[0];
    free(heap); // 释放堆数组（已无用）
    return root;
}

// 生成编码, 本质是一个 DFS 深度优先搜索
void generateHuffmanCode(tree root, char *currentCode, int codeLen, char **charCodes, int *charFreq)
{
    if (root == NULL)
        return;

    // 终止条件：遇到叶子节点（原始字符）
    if (root->left == NULL && root->right == NULL && root->c != '\0')
    {
        currentCode[codeLen] = '\0'; // 给编码加结束符
        int idx = (unsigned char)root->c;
        charCodes[idx] = (char *)malloc(strlen(currentCode) + 1);
        strcpy(charCodes[idx], currentCode);
        charFreq[idx] = root->fre; // 存储字符自身的频率
        return;
    }

    // 左子树：拼接 '0'，递归深入
    currentCode[codeLen] = '0';
    generateHuffmanCode(root->left, currentCode, codeLen + 1, charCodes, charFreq);

    // 右子树：拼接 '1'，递归深入
    currentCode[codeLen] = '1';
    generateHuffmanCode(root->right, currentCode, codeLen + 1, charCodes, charFreq);
}

// 对外接口：初始化编码数组 + 调用递归函数 + 输出结果（修正频率输出）
void getHuffmanCodes(tree root, int n, char **charCodes, int *charFreq)
{
    if (root == NULL || n <= 0)
        return;

    // 1. 初始化编码和频率存储数组
    for (int i = 0; i < MaxCharCnt; i++)
    {
        charCodes[i] = NULL;
        charFreq[i] = 0;
    }

    // 2. 申请临时编码缓冲区（最长编码长度为 n-1）
    char *tempCode = (char *)malloc(n * sizeof(char)); // 预留结束符位置

    // 3. 递归生成编码
    generateHuffmanCode(root, tempCode, 0, charCodes, charFreq);

    // 4. 释放临时缓冲区
    free(tempCode);

    // 5. 输出所有字符的编码（显示自身频率）
    printf("Huffman 编码结果：\n");
    for (int i = 0; i < MaxCharCnt; i++)
    {
        if (charCodes[i] != NULL)
        {
            printf("字符 '%c' (频率：%d) → 编码：%s\n", i, charFreq[i], charCodes[i]);
        }
    }
}

// 递归释放 Huffman 树的所有节点（避免内存泄漏）
void freeHuffmanTree(tree root)
{
    if (root == NULL)
        return;
    freeHuffmanTree(root->left);  // 递归释放左子树
    freeHuffmanTree(root->right); // 递归释放右子树
    free(root);                   // 释放当前节点
}

// 辅助函数：释放编码数组内存（你的原有代码，正确）
void freeHuffmanCodes(char **charCodes)
{
    for (int i = 0; i < MaxCharCnt; i++)
    {
        if (charCodes[i] != NULL)
        {
            free(charCodes[i]);
            charCodes[i] = NULL;
        }
    }
}

// 统一释放所有资源
void Free_All(tree root, char** charCodes)
{
    freeHuffmanTree(root);
    freeHuffmanCodes(charCodes);
}

/*--------------------------Test Case--------------------------*/
int main()
{
    char a[] = {'a', 'b', 'c', 'd', 'e', 'f'};
    int fre[] = {45, 13, 12, 16, 9, 5};
    int n = sizeof(a) / sizeof(char);

    // 1. 构建 Huffman 树
    tree root = BuildHuffmanTree(a, fre, n);

    // 2. 生成编码
    char *charCodes[MaxCharCnt];
    int charFreq[MaxCharCnt] = {0}; // 存储每个字符的自身频率
    getHuffmanCodes(root, n, charCodes, charFreq);

    // 3. 释放所有资源
    Free_All(root, charCodes);
}