import numpy as np

def InfoGain(data:list[tuple[int, int]])->float:
    
    def DichotomyEntropy(yes:int, no:int)->float:

        total=yes+no
        prob_yes=yes/total
        prob_no=no/total

        if prob_no==0:
            return -np.log2(prob_yes)*prob_yes
        elif prob_yes==0:
            return -np.log2(prob_no)*prob_no
        return -np.log2(prob_yes)*prob_yes-np.log2(prob_no)*prob_no
    
    info_gain=0
    total=sum(data[i][1] for i in range(len(data)))
    
    total_yes=sum(data[i][0] for i in range(len(data)))
    # print('total', total, 'total_yes', total_yes)
    # total_no=0
    for yes, all in data:
        info_gain-=all/total*DichotomyEntropy(yes, all-yes)
    info_gain+=DichotomyEntropy(total_yes, total-total_yes)

    return info_gain


data1=[(3, 6), (4, 6), (1, 5)]
print(InfoGain(data1))

data2=[(5, 8), (3, 7), (0, 2)]
print(InfoGain(data2))

data3=[(3, 4), (3, 4), (1, 1)]
print(InfoGain(data3))


data4=[(2, 4), (4, 6), (3, 4)]
print(InfoGain(data4))