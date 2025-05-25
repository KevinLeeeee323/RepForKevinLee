import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
实现一元线性回归的相关内容:
1. 根据给定的n组样本点(x, y)拟合回归方程y=ax+b,其中a, b是回归系数
   - 通过最小二乘法计算出a, b
   - 生成数据图以及拟合的直线图
2. 对于回归方程进行显著性检验,包括t检验,f检验,相关系数检验
3. 对于给定一个x_0,根据回归方程给出相对应的y_0的1-\alpha置信区间
'''

def LinearRegression(op):
    # 加载数据,转成ndarray
    data = np.loadtxt('data2.txt', delimiter=' ', dtype=np.float32, skiprows=1) # 第一行是数据说明
    x = data[0, :]  # 第1列作为x
    y = data[1, :]  # 第2列作为y

    if np.size(x)==np.size(y):
        n=np.size(x)
    else:
        print('数据数量不匹配,输入错误!\n')
        return
    
    # 各个子函数公用计算结果
    x_hat=np.mean(x)
    y_hat=np.mean(y)
    l_xx=np.sum(np.square(x-x_hat))
    l_xy=np.sum((x-x_hat)*(y-y_hat))
    l_yy=np.sum(np.square(y-y_hat))
    a=l_xy/l_xx
    b=y_hat-a*x_hat

    S_T=l_yy # 总偏差平方和
    S_R=(l_xy)**2/l_xx # 回归平方和
    S_e=S_T-S_R # 残差平方和
    print(f'S_T={S_T}', f'S_R={S_R}', f'S_e={S_e}', sep=', ') # 部分计算结果展示
    
    # ------------------以下是子函数部分----------------

    def Analysis(): # 计算得出回归方程,并画图

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
        # plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='blue', label='sample')
        coe = np.polyfit(x, y, 1) # 利用内置函数拟合

        plt.plot(x, np.poly1d(coe)(x), 'r-', label=f'拟合直线: y={coe[0]:.3f}x{coe[1]:+.2f}')
        plt.title('一元线性回归的回归方程')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()  # 显示图例
        plt.grid(True)  # 显示网格
        plt.show()
        
        print(f'回归方程:y={coe[0]:.3f}*x{coe[1]:+.3f}', sep='')
        return  coe[0], coe[1]


    def Test(): # 进行三种显著性检验
        '''
        对于回归方程y=ax+b,F检验和t检验旨在检验如下假设:
        H_0: a=0 vs H_1: a!=0

        相关性检验旨在对x,y所对应的样本总体X,Y的相关系数\rho进行如下检验:
        H_0: \rho=0 vs H_1: \rho!=0
        '''
        alpha=float(input('请输入显著性水平alpha:\n'))

        F=S_R/(S_e/(n-2))

        # F检验
        Fp=stats.f.ppf(1-alpha, 1, n-2) # 计算1-alpha分位数
        print('进行F检验:')
        print(f'F={F}', f'F_{1-alpha}={Fp}', sep=', ')
        if F < Fp:
            print('F < Fp')
            print(f'在显著性水平alpha={alpha}下,回归方程不显著')
        else:
            print('F > Fp')
            print(f'在显著性水平alpha={alpha}下,回归方程是显著的')
            
        # t检验
        t=np.sqrt(F)
        tp=stats.t.ppf(1-alpha/2, n-2)
        print('进行t检验:')
        print(f't={t}', f't_{1-alpha/2}={tp}', sep=', ')
        if t < tp:
            print('t < tp')
            print(f'在显著性水平alpha={alpha}下,回归方程不显著')
        else:
            print('t > tp')
            print(f'在显著性水平alpha={alpha}下,回归方程是显著的')

        # 相关系数检验
        r=l_xy/np.sqrt(l_xx * l_yy)
        r_cri=np.sqrt(Fp/(Fp+(n-2)))
        print('进行样本总体相关性检验:')
        print(f'r={r}', f'r_cri={r_cri}', sep=', ')
        if r < r_cri: 
            print(f'在显著性水平alpha={alpha}下,样本总体不相关')
        else:
            print(f'在显著性水平alpha={alpha}下,样本总体相关')

        
    def Predict(x_0, alpha): # 给定x_0以及置信水平\alpha, 结合回归方程预测y_0范围
        tp=stats.t.ppf(1-alpha/2, n-2)
        y_0=a*x_0+b
        half_len=tp*np.sqrt((S_e/(n-2))*(1+1/n+(x_0-x_hat)**2/l_xx))
        print(f'y_0的1-alpha=1-{alpha}置信区间为[{y_0-half_len}, {y_0+half_len}]')
    
    # -------------以上是子函数部分-------------

    if op>=0:
        print('请在查看完拟合图像后将窗口关闭,继续进行之后的分析')
        Analysis()
    if op>=1:
        Test()
    if op>=2:
        x_0=float(input('请输入要预测的因变量y_0所对应的自变量值x_0\n'))
        new_alpha=float(input('请输入y_0预测值的置信区间new_alpha\n'))

        Predict(x_0, new_alpha)


if __name__=='__main__':
    str='''
    三种功能如下:
    op=1 只给出回归方程和回归直线
    op=2 在op=1基础上增加显著性检验,含回归显著性检验和样本总体相关系数检验 
    op=3 在op=2基础上增加给定x_0的y_0范围预测   
    '''
    print(str)
    op=int(input('请根据上述说明通过输入op的值,选择要实现的功能:\n'))
    LinearRegression(op)