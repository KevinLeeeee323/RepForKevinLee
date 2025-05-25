import numpy as np
from scipy import stats

'''
使用条件:单因子,重复数相同的方差检验
功能特性:
1.支持p值检验和F比检验两种检验方式
2.可以输出MLE和置信区间
'''

def GetData(r:int, m:int):

    try:
        data_input=np.array(input("请依次输入每个水平的数据,空格分隔,回车作为结束\n").split(), dtype=np.float32)

        # 验证输入元素数量是否符合要求
        if len(data_input) != r * m:
            raise ValueError(f"The number of data is incorrect. Requires r * m={r} * {m}={r*m}.")
        
        data=np.reshape(data_input, (r, m))

    # 不能用input作为变量名,这是python内置函数input

    except ValueError as e:
        print(f"Wrong Input: {e}")
        return np.array([])  # 返回空数组或其他默认值
    except Exception as e:
        print(f"Unknown Error: {e}")
        return np.array([])

    print(data)
    return data

def Test(data, alpha):
    
    # 对于二位ndarray,不指定axis时,np.mean()计算这个ndarray中所有数的平均值
    
    # 计算检验所需数据
    (r, m)=np.shape(data)
    n=m*r
    line_aver=np.mean(data, axis=1) # 行平均
    total_aver=np.mean(data) # 总数据平均
    S_e=np.sum(np.square(data-line_aver.reshape(-1, 1))) # 组内偏差平方和
    S_A=m*np.sum(np.square(line_aver-total_aver))    # 组间偏差平方和
    # S_T=S_e+S_A # 总偏差平方和

    '''
    line_aver.reshape(-1, 1) 的作用
    将一维数组 line_aver(形状为 (r,))重塑为二维列向量(形状为 (r, 1))。
    -1 表示自动计算该维度的大小，确保元素总数不变
    '''
    
    # 计算自由度:
    f_e=n-r
    f_A=r-1

    F=(S_A/f_A)/(S_e/f_e) # 检验统计量-F比
    p_value = stats.f.sf(F, f_A, f_e)  # P值
    print('相关数据以及结果如下:')
    print(f'S_A:{S_A}', f'S_e:{S_e}', sep='\n')

    # # 通过p值检验
    # if p_value > alpha:
    #     print('Factor A is not Substantial')
    # else:
    #     print('Factor A is substantial')

    # 通过F比检验
    Fp=stats.f.ppf(1-alpha, f_A, f_e) # 计算1-alpha分位数
    print(f'F={F}', f'F_{1-alpha}={Fp}', sep='\n')
    if F < Fp:
        print('F < Fp')
        print('Factor A is not Substantial')
    else:
        print('F > Fp')
        print('Factor A is substantial')

    return (line_aver, total_aver, S_e)


def extra(line_aver, total_aver, S_e, r, m, alpha):
    n=m*r
    # 输出最大似然估计(MLE)
    print(f'the MLE of expectation is {total_aver}')
    for i in range(r):
        print(f'the MLE of average{i} is {line_aver[i]}')
    print(f'the MLE of variance is {S_e/n}')

    print(f'the Unbiased Estimate of variance is {S_e/(n-r)}') # 方差的无偏估计和MLE不同

    # 输出置信区间(Confidence Interval)
    half_len=stats.t.ppf(1-alpha/2, n-r)*np.sqrt(S_e/((n-r)*m))
    for i in range(r):
        print(f'the 1-alpha={1-alpha} confidence interval of average{i} is {line_aver[i]}+-{half_len}')


def main():
    # 读取数据维度(r, m),显著性水平\alpha
    print('以下是单因子重复数相同的方差检验程序')
    r, m, alpha=input("请输入该因子的水平数r,重复数m以及显著性水平alpha\n").split()
    (r, m)=map(int, (r, m))
    alpha=float(alpha)

    data=GetData(r, m) # 读取数据
    (line_aver, total_aver, S_e)=Test(data, alpha) # 检验

    extra(line_aver, total_aver, S_e, r, m, alpha)# 额外操作:获取MLE和置信区间


if __name__=='__main__':
    main()

'''
一个使用Numpy广播特性的例子:

# 原始数据 (3组,每组2个样本)
data = np.array([
    [1, 2],  # 第1组
    [4, 5],  # 第2组
    [7, 8]   # 第3组
])  # 形状: (3, 2)

# 计算每组的平均值
line_aver = np.mean(data, axis=1)  # [1.5, 4.5, 7.5]，形状: (3,)

# 重塑为列向量
line_aver_reshaped = line_aver.reshape(-1, 1)  # 形状: (3, 1)
# 具体值: [[1.5], [4.5], [7.5]]

# 广播相减:data (3, 2) - line_aver_reshaped (3, 1)
# line_aver_reshaped 被广播为:
# [[1.5, 1.5],
#  [4.5, 4.5],
#  [7.5, 7.5]]

# 相减结果:
# [[1-1.5, 2-1.5],
#  [4-4.5, 5-4.5],
#  [7-7.5, 8-7.5]]
# = [[-0.5, 0.5],
#    [-0.5, 0.5],
#    [-0.5, 0.5]]
'''