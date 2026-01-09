def FractionalKnapsack(item_list:list[tuple[int, int]], C:int):
    # item_list[i]=(v[i], p[i]) 体积-volume, 价值-price
    item_list_sorted=sorted(item_list, key=lambda x:x[1]/x[0], reverse=True)
    max_price=0
    room=C
    i=0
    while room>0 and i<len(item_list):
        v=item_list_sorted[i][0]
        p=item_list_sorted[i][1]
        x=1 if room>v else room/v
        room-=x*v
        max_price+=p*x
        i+=1
    return max_price


if __name__=='__main__':
    volumes=[2, 4, 5, 6, 8]
    prices=[4, 6, 7, 6, 10]
    C=10
    item_list=[(volumes[i], prices[i]) for i in range(len(volumes))]
    max_price=FractionalKnapsack(item_list, C)
    print(max_price)


