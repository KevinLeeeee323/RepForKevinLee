# QuickPow with Python Implementation

def quick_pow(x, pow:int):

    def quick_pow_divide_and_conquer(x, pow:int):
        if pow==0:
            return 1
        elif pow==1:
            return x
        
        half=quick_pow_divide_and_conquer(x, pow//2)
        ans =half* half
        if pow%2==0:
            return ans
        else:
            return ans * x
    
    return quick_pow_divide_and_conquer(x, pow)


if __name__=='__main__':
    x=3
    pow=5
    print(quick_pow(3, 5))