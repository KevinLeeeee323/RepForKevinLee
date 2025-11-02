import numpy as np

N_sample=100000 # 采样数量, 理论上越大, 积分数值越准
M=4.02 # M应该略大于 f(x)在积分区间上最大值, 因此调整函数和区间后, 需要调整 M
# np.random.seed(42)  # 固定种子为42（任意整数均可）, 从而使得每次运行生成相同的 x1 和 x2
def MonteCarlo_Integral(f, start, end):
    # global N_sample
   
    xs = np.random.uniform(low=start, high=end, size=N_sample)
    ys = np.random.uniform(low=0, high=M, size=N_sample)
    S=(end-start)*M
    cnt=0
    for x, y in zip(xs, ys):
        if y<f(x):
            cnt+=1
    S_integral=S*cnt/N_sample
    return S_integral


if __name__=='__main__':
    print(MonteCarlo_Integral(lambda x:x**2, 0, 2))

