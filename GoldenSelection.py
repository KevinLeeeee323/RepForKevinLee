# 0.618 法(黄金分割法) 进行一维搜索
import numpy as np

def GoldenSplit(a, b, f, eps):
    
    '''
        Parameters:
            黄金分割法近似求解最小值.
            [a, b]是传入的闭区间. 需要满足f 在[a, b]上是单峰函数
            f(x) 是函数.
            eps 用来进行精度控制.

        Return Values:
            x_min_f: f 在[a, b]上的一个近似最小值点.
            f_min: f(x_min_f), f在[a, b]上的一个近似最小值.
    '''

    ratio=(np.sqrt(5)-1)/2

    if a>=b:
        return np.nan, np.nan
    
    while b-a>eps:
        # update lambda_k, miu_k
        lam=ratio*a +(1-ratio)*b # lambda_k
        miu=(1-ratio)*a + ratio*b # miu_k

        print(f'a:{a:.3f}, b:{b:.3f}, λ:{lam:.3f}, μ:{miu:.3f}, f(λ):{f(lam):.3f} f(μ):{f(miu):.3f}')
        if f(lam)>f(miu):
            a=lam # a_{k+1}
        else:
            b=miu # b_{k+1}
        
    print(f'a:{a:.3f}, b:{b:.3f}')

    ans=(a+b)/2
    return ans, f(ans)

'''
    黄金分割法的一个减少计算的点在于 lam_{k+1}=miu_k, 或者 miu_{k+1}=lam_k, 上述做法没体现出来, 而是每次重新算 lam, miu.
    下面这版代码考虑了这个复用.
'''

def GoldenSplit_New(a, b, f, eps)-> tuple:
    
    '''
        Parameters:
            黄金分割法近似求解最小值.
            [a, b]是传入的闭区间. 需要满足f 在[a, b]上是单峰函数
            f(x) 是函数.
            eps 用来进行精度控制.

        Return Values:
            x_min_f: f 在[a, b]上的一个近似最小值点.
            f_min: f(x_min_f), f在[a, b]上的一个近似最小值.
    '''

    ratio=(np.sqrt(5)-1)/2

    if a>=b:
        return np.nan, np.nan

    cnt=0

    while b-a>eps:
        # update lambda_k, miu_k
        
        if cnt==0:
            lam=ratio*a +(1-ratio)*b
            miu=(1-ratio)*a + ratio*b
        else:
            print(f'a:{a:.3f}, b:{b:.3f}, λ:{lam:.3f}, μ:{miu:.3f}, f(λ):{f(lam):.3f} f(μ):{f(miu):.3f}')
            if f(lam)>f(miu):
                a=lam_pre # a_{k+1}=lambda_k
                lam=miu_pre # lambda_{k+1}=miu_k
                miu=(1-ratio)*a + ratio*b # miu_k
            else:
                b=miu_pre # b_{k+1}=miu_k
                miu=lam_pre # miu_{k+1}=lambda_k
                lam=ratio*a +(1-ratio)*b # lambda_k
        
        cnt+=1
        lam_pre, miu_pre=lam, miu

        
    print(f'a:{a:.3f}, b:{b:.3f}')

    ans=(a+b)/2
    return ans, f(ans)

if __name__=='__main__':
    def f1(x):
        return 2*x**2-x-1

    def f2(x):
        return np.exp(-x)+x**2

    # x_min_f, f_min=GoldenSplit(0, 1, f, 0.2)
    x_min_f, f_min=GoldenSplit_New(0, 1, f2, 0.2) # 新的一版, 虽然最终数值上没什么差别

    if np.isfinite(x_min_f) and np.isfinite(f_min):
        print(f'x_min_f:{x_min_f:.3f}, f_min:{f_min:.3f}')
    else:
        print('not a vaild range with lower bound greater than upper bound. Retry')

