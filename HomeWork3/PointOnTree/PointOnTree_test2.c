#include <stdio.h>
#include <stdlib.h>

void FindGreatestTwo(int* max1, int* max2, int* max1_id, int* max2_id, int* arr, int arrSize)
{
    // only for arrSize>=2
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
    int arr[]={9, 1, 4, 7, 13, 2, 5, 13, 6, 9, 13};
    int max1=0, max2=0, max1_id=0, max2_id=0;
    FindGreatestTwo(&max1, &max2, &max1_id, &max2_id, arr, sizeof(arr)/sizeof(int));
    printf("%d %d %d %d", max1, max2, max1_id, max2_id);

}