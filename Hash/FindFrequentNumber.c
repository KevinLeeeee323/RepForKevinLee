#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
/*
    题目描述:
    提供一个包含 n 个元素的数组，要求返回其中出现次数大于半数（大于 ⌊n/2⌋）的元素。假设数组中一定存在这样的元素。
     Input: 2 2 1 1 1 2 2 2 5
    Output: 2
*/

#define TABLE_SIZE 101 
/*
    这里哈希表取一个质数比较明智, 因为下面通过 mod TABLE_SIZE 的方式存储哈希映射关系, 
    这样会减少哈希冲突的概率.
    但同时, 这里取 TABLE_SIZE 比较大, 没有考虑会把 HashTable 填满的情况
*/

typedef struct
{
    /* data */
    int num;
    int is_used;
    int cnt;
} HashEntry;

HashEntry* HashInit()
{
    HashEntry* HashTable=(HashEntry*)calloc(TABLE_SIZE, sizeof(HashEntry));
    /*calloc 相比 malloc, 会在分配内存后会自动将所有字节初始化为0, 但写法和 malloc 略有不同*/
    if(HashTable==NULL) 
        perror("out of memory"); //处理内存分配失败
    return HashTable;
}

int GetIndex(int key, HashEntry* HashTable) {return (key%TABLE_SIZE +TABLE_SIZE)%TABLE_SIZE;}
/*
    获得对应的由 key 到存储位置映射, 并且保证返回的 index 属于 [0, TABLE_SIZE-1]
    这个函数的第一个 +TABLE_SIZE 是为了处理 key<0 的情况
    这个函数的第二个 %TABLE_SIZE 是为了让最终 index<TABLE_SIZE-1
    e.g. key1=-123, key2=9, TABLE_SIZE=10
    key1%TABLE_SIZE+TABLE_SIZE=(-123)%10+10=7, 再对 TABLE_SIZE 取余=7;
    key2%TABLE_SIZE+TABLE_SIZE=9%10+10=19, 此时超出 TABLE_SIZE-1 范围, 因此还需要取余=19%10=9
*/ 


void UpdateHashTable(int key, HashEntry* HashTable) // 处理哈希冲突, 并且更新哈希表
{
    int index=GetIndex(key, HashTable);
    while(!((HashTable[index].is_used==0) || (HashTable[index].num==key)))
        index=(index+1)%TABLE_SIZE;
    // 上面这个 while 对应着退出条件: 要么找到一个空余的位置, 要么在哈希表中找到当前元素
    // 由于是退出条件, 所以看起来会有点拧巴

    if(HashTable[index].is_used==0) //此时的情况是, 当前位置没有元素, 给这个元素存储上
    {
        HashTable[index].num=key;
        HashTable[index].cnt=1;
        HashTable[index].is_used=1;
    }
    else //此时的情况是, 在哈希表中找到了当前的 key, 直接增加统计到的次数就行
        HashTable[index].cnt++;
}

int FindMaxCnt(HashEntry* HashTable)
{
    int cnt_max=-1;
    int cnt_max_num=-1;
    for(int i=0; i<TABLE_SIZE; i++)
    {
        if(HashTable[i].is_used==1 && HashTable[i].cnt>cnt_max)
        {
            cnt_max=HashTable[i].cnt;
            cnt_max_num=HashTable[i].num;
        }
    }
    return cnt_max_num;
}

int main()
{
    HashEntry* table=HashInit();
    int read=-1;
    while(scanf("%d", &read)!=EOF)
        UpdateHashTable(read, table); //逐个读入, 更新哈西表并且处理哈希冲突
    
    // 以下: 寻找并且输出最大次数的元素, 没有直接利用"元素个数>= n/2"条件, 而是直接去求最大次数了
    int ans=FindMaxCnt(table);
    printf("%d", ans);
    free(table);
    return 0;
}


/*
    其实本题还有另一个方法: 摩尔投票算法 (Boyer-Moore Algorithm)
    - 时间复杂度为 O (n)，空间复杂度为 O (1)
    - 核心思想：
        - 维护一个 candidate（候选元素）和一个 count（计数）。
        - 遍历数组：
            - 如果 count 为 0，将当前元素设为 candidate。
            - 如果当前元素与 candidate 相同，count 加 1。
            - 否则，count 减 1。
        - 遍历结束后，candidate 必定是出现次数超过一半的元素。
        - 为什么这样做有效?
            - 因为目标元素出现的次数比所有其他元素加起来还要多，所以即使每次都和其他元素 “抵消” 一次，最后剩下的也一定是它。

    - 代码
        int main() 
        {
            int candidate = 0;
            int count = 0;
            int read;

            while (scanf("%d", &read) != EOF) {
                if (count == 0) {
                    candidate = read;
                }
                count += (read == candidate) ? 1 : -1;
            }

            // 题目保证存在这样的元素，所以 candidate 就是答案
            printf("%d\n", candidate);

            return 0;
        }
*/