#define TABLE_SIZE 1003
#include <stdlib.h>
#include <stdio.h>

/*
    手写哈希, 数据结构导入自 FindFrequentNumber.c, 但是在大样本时仍然被卡了时间复杂度.
    似乎是有更优化的哈希方法.
*/
typedef struct
{
    /* data */
    int num;
    int is_used;
    int cnt;
} HashEntry;

HashEntry* HashInit(int Length)
{
    HashEntry* HashTable=(HashEntry*)calloc(Length, sizeof(HashEntry));
    if(HashTable==NULL) 
        perror("out of memory"); //处理内存分配失败
    return HashTable;
}

int GetIndex(int key, HashEntry* HashTable) {return (key%TABLE_SIZE +TABLE_SIZE)%TABLE_SIZE;}

void UpdateHashTable(int key, HashEntry* HashTable, int* EntryCnt) // 处理哈希冲突, 并且更新哈希表
{
    int index=GetIndex(key, HashTable);
    while(!((HashTable[index].is_used==0) || (HashTable[index].num==key)))
        index=(index+1)%TABLE_SIZE;

    if(HashTable[index].is_used==0) //此时的情况是, 当前位置没有元素, 给这个元素存储上
    {
        HashTable[index].num=key;
        HashTable[index].cnt=1;
        HashTable[index].is_used=1;
        (*EntryCnt)++;
    }
    else //此时的情况是, 在哈希表中找到了当前的 key, 直接增加统计到的次数就行
        HashTable[index].cnt++;
}


int compare(const void* a, const void* b)
{return ((HashEntry*)a)->cnt-((HashEntry*)b)->cnt;}


int findLeastNumOfUniqueInts(int* arr, int arrSize, int k) {

    HashEntry* table=HashInit(TABLE_SIZE);
    int i=0;
    int numCnt=0;
    for(i=0; i<arrSize; i++)
        UpdateHashTable(arr[i], table, &numCnt);
    
    HashEntry* newTable=HashInit(numCnt); //统计真正存了数据的地方
    int top=-1;
    for(i=0; i<TABLE_SIZE; i++)
        if(table[i].is_used==1)
            newTable[++top]=table[i];

    qsort(newTable, top+1, sizeof(HashEntry), compare);

    // for(int i=0; i<=top; i++)
    //     printf("%d %d %d\n", i, newTable[i].num, newTable[i].cnt);

    if(top+1!=numCnt)
    {   
        printf("error");
        return -1;
    }
    printf("numCnt:%d\n", numCnt);
    int minus=0;
    for(i=0; i<=top && minus<=k; i++)
    {
        numCnt--;
        minus+=newTable[i].cnt;
    }
    if(minus>k)
        numCnt++;
    free(table);
    free(newTable);
    return (numCnt<=0)?0:numCnt;
}

int main()
{
    int arr[]={4,3,1,1,3,3,2};
    // int arr[]={5,5, 4};
    int size=sizeof(arr)/sizeof(int);
    int k=3;
    printf("%d", findLeastNumOfUniqueInts(arr, size, k));
}