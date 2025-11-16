import numpy as np
import matplotlib.pyplot as plt

def plot_root_locus(poles, zeros, K_range=(0, 1e6), num_points=1000):
    """
    绘制根轨迹图
    参数：
        poles: 开环极点列表（复数值或实数值），如 [0, -2]
        zeros: 开环零点列表（复数值或实数值），如 [-1]
        K_range: 增益K的范围，默认 (0, 1e6)
        num_points: 采样点数，越多轨迹越平滑
    """
    # 生成增益K的对数分布（避免低K时采样过疏，高K时过密）
    K = np.logspace(np.log10(K_range[0]+1e-10), np.log10(K_range[1]), num_points)
    all_roots = []  # 存储所有K对应的闭环极点

    for k in K:
        # 步骤1：计算开环传递函数的分子（num）和分母（den）多项式系数
        den = np.poly(poles)  # 分母系数（长度=极点个数+1）
        if len(zeros) == 0:
            num = np.array([1])  # 无零点时，分子为常数1（0阶多项式）
        else:
            num = np.poly(zeros)  # 分子系数（长度=零点个数+1）
        
        # -------------------------- 关键修改：分子系数补零对齐 --------------------------
        # 分母阶数 = len(den) - 1，分子阶数 = len(num) - 1
        # 补零：在分子系数前面加 (分母长度 - 分子长度) 个0，确保两者长度一致
        num_padded = np.pad(num, (len(den) - len(num), 0), mode='constant')
        # ------------------------------------------------------------------------------
        
        # 步骤2：闭环特征方程系数 = 分母系数 + K×补零后的分子系数
        closed_den = den + k * num_padded
        
        # 步骤3：求解特征方程的根（复根）
        roots = np.roots(closed_den)
        all_roots.append(roots)

    # 转换为数组，方便绘图（shape: (num_points, 极点个数)）
    all_roots = np.array(all_roots)

    # 绘制根轨迹图
    plt.figure(figsize=(8, 6))
    # 遍历每个闭环极点的轨迹（每一列对应一个极点随K的变化）
    for i in range(all_roots.shape[1]):
        plt.plot(all_roots[:, i].real, all_roots[:, i].imag, 'b-', linewidth=1.5)  # 实轴→x，虚轴→y

    # 标注开环极点（×）和零点（○）
    plt.scatter(np.real(poles), np.imag(poles), c='red', s=100, marker='x')
    if len(zeros) > 0:
        plt.scatter(np.real(zeros), np.imag(zeros), c='green', s=100, marker='o', edgecolors='black')

    # 绘制坐标轴（实轴、虚轴）
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

    # 图形美化（适配自控理论绘图规范）
    plt.xlabel('Re(s)', fontsize=12)
    plt.ylabel('Im(s)', fontsize=12)
    plt.title('root locus', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')  # 实轴和虚轴等比例，避免轨迹变形
    plt.savefig('./rootLocus.jpg')
    plt.show()


# ------------------------------ 示例：绘制4阶系统根轨迹 ------------------------------
if __name__ == "__main__":
    print("绘制根轨迹...")
    poles = [0, 0, -2, -5]  # 开环极点
    zeros = [-0.5]    # 开环零点
    plot_root_locus(poles, zeros, K_range=(0, 30))  