import sys
import numpy as np

def main():
    
    # DIM: 数据维度
    N, DIM, K=map(int, input().split())
    K=min(N, K)

    # 读入数据
    xs=np.zeros(shape=(N, DIM), dtype=np.float32)
    for i in range(N):
        part=sys.stdin.readline().split()
        for j in range(DIM):
            xs[i][j]=float(part[j])
    xs=np.array(xs, dtype=np.float32)

    # 随机初始化高斯分布个数(均值+方差)
    means=np.random.normal(loc=0.0, scale=1.0, size=(K, DIM)) # # 均值：随机从标准正态分布中取点
    vars=np.array([np.eye(DIM) for _ in range(K)], dtype=np.float32) # 协方差矩阵：初始化为 K 个单位矩阵 (Identity Matrix) 保证可逆

    belongs=np.zeros(shape=(N, K), dtype=np.float32) # belongs[i][j]: 数据 x_i 属于第 j 个类别的程度
    mix_coe=np.ones(shape=K, dtype=np.float32)/K # 混合系数：初始化为均等分配
    
    MAX_ITER=100
    TOL=1e-4
    EPS=1e-10

    def get_prob(x, mean:np.ndarray, var:np.ndarray):
        exponent=-0.5*(x-mean)@np.linalg.inv(var)@(x-mean)
        det = max(np.linalg.det(var), EPS) # 防止方差行列式为负或0导致报错
        return 1/(2*np.pi)**(DIM/2)/(det**0.5)*np.exp(exponent)
    for iter in range(MAX_ITER):

        # 计算每个数据点的隶属度
        for i in range(N):
            probs=np.zeros(shape=K, dtype=np.float32)
            div=0.0 # 分母
            for j in range(K):
                probs[j]=get_prob(xs[i], means[j], vars[j])
                div+=mix_coe[j]*probs[j]

            div=max(div, EPS) # 防止分母为0, 加上一个极小的 epsilon
            for j in range(K):
                belongs[i][j]=mix_coe[j]*probs[j]/div
        
        # 更新每个高斯分布
        Ns=belongs.sum(axis=0)
        new_mix_coe=np.zeros(shape=K, dtype=np.float32)
        for j in range(K):
            if Ns[j]<EPS:
                continue

            # 以下: 更新均值, 方差
            new_means=np.zeros(shape=DIM, dtype=np.float32)
            new_var=np.zeros(shape=(DIM, DIM),dtype=np.float32)
            for i in range(N):
                new_means+=belongs[i][j]*xs[i]
            new_means/=Ns[j]
            means[j]=new_means

            # 必须在更新了均值之后, 再用新均值更新方差
            for i in range(N):
                diff=xs[i]-means[j]
                new_var+=belongs[i][j]*np.outer(diff, diff) # 外积: 两个向量张成矩阵
            new_var/=Ns[j]
            vars[j]=new_var+np.eye(DIM, dtype=np.float32)*EPS # 为了永远保证矩阵可逆，在对角线上加一个极小值eps

            new_mix_coe[j]=Ns[j]/N
        
        update_vol=np.sum(np.abs(new_mix_coe-mix_coe)) # # 使用绝对值求和，避免正负抵消, 来判断收敛
        mix_coe=new_mix_coe.copy() # 使用 copy 防止引用污染

        if update_vol<=TOL:
            print(f"Converged at iteration {iter}")
            break


if __name__ == "__main__":
    main()
