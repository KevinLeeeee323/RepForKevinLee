#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n;
    scanf("%d", &n);
    int* save1=(int*)calloc(n-1, sizeof(int));
    int* save2=(int*)calloc(n, sizeof(int));
    for(int i=1; i<n; i++)
        scanf("%d", &save1[i]);
    for(int i=0; i<n; i++)
        scanf("%d", &save2[i]);
    
    for(int i=1; i<n; i++)
        printf("%d", save1[i]);
    for(int i=0; i<n; i++)
        printf("%d", save2[i]);
}