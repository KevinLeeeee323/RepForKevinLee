# 牛顿法求最小值和最小值点
import numpy as np

h=0.001

def dfdx(x, f): # 一阶导数
    return (f(x+h)-f(x-h))/(2*h)

def d2fdx2(x, f): # 二阶导数
    df_x_plus_h = dfdx(x + h, f)
    df_x_minus_h = dfdx(x - h, f)
    return (df_x_plus_h - df_x_minus_h) / (2 * h)


def NewtonMethod(x0, f, iter_time, eps):
    '''
        Parameters:
            x0: 迭代的起始点.
            f(x): 要求极小值的函数
            iter_time: 设定的最大迭代次数
            eps: 迭代精度控制. 其实和 iter_time 中有一个就行.

        Return Values:
            x_min_f: 最终迭代到的近似极小值点
            min_f: f(x_min_f), 最终迭代得到的的极小值
    '''
    x=x0
    cnt=0

    while cnt<=iter_time and np.absolute(dfdx(x, f))>eps:
        print(f'第{cnt}次迭代: x:{x:.4f}, f(x):{f(x):.4f}')

        df_dx=dfdx(x, f)
        d2f_dx2=d2fdx2(x, f)

        if np.absolute(d2f_dx2) < 1e-8:
            print(f"迭代{cnt}次时二阶导数接近0, 无法继续迭代")
            break

        x_new=x-df_dx/d2f_dx2

        x=x_new
        cnt+=1
    
    
    if cnt > iter_time:
        print(f"迭代终止：已达到最大迭代次数{iter_time}")
    else:
        print(f"迭代终止：一阶导数绝对值{np.absolute(dfdx(x, f)):.4f} ≤ eps={eps}")
  
    x_min_f=x
    min_f=f(x_min_f)
    return x_min_f, min_f
    
if __name__=='__main__':

    def f(x):
        return 3*x**4-4*x**3-12*x**2
    
    x0=-1.2
    iter_time=3
    x_min_f, f_min=NewtonMethod(x0, f, iter_time, eps=0.0001)

        