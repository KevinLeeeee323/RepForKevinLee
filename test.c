#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int compare(const void* a, const void* b)
{
    char* str_a=*(char**)a;
    char* str_b=*(char**)b;
    int lenA=strlen(str_a);
    int lenB=strlen(str_b);
    if(lenA!=lenB)
        return lenB-lenA;
    return strcmp(str_b, str_a);
}

char* kthLargestNumber(char** nums, int numsSize, int k) {
    qsort(nums, numsSize, sizeof(char*), compare);
    return nums[k-1];
}

int main()
{
    char* nums[]={"2","21","12","1"};
    int numsSize=sizeof(nums)/sizeof(nums[0]);
    // printf("%d", numsSize);
    qsort(nums, numsSize, sizeof(char*), compare);
    for(int i=0; i<numsSize; i++)
        printf("%s ", nums[i]);
}