import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 1. 洛伦兹系统微分方程（和之前一致）
def lorenz_system(t, state, sigma, rho, beta):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdx = x * y - beta * z
    return [dxdt, dydt, dzdx]

# 2. 计算三维立方体的体积（通过8个顶点的向量叉乘）
def cube_volume(vertices):
    # vertices: 8x3 数组，每行是一个顶点的 (x,y,z)
    v0 = vertices[0]
    v1, v2, v3 = vertices[1], vertices[3], vertices[4]
    # 三个边向量
    a = v1 - v0
    b = v2 - v0
    c = v3 - v0
    # 体积 = 标量三重积的绝对值 / 6
    volume = abs(np.dot(a, np.cross(b, c))) / 6
    return volume

# 3. 设置参数
sigma = 10
rho = 28
beta = 8/3
t_span = (0, 10)  # 演化10秒，足够观察收缩
t_eval = np.linspace(0, 10, 100)  # 100个时间点记录体积

# 4. 定义初始小立方体（中心在 (1,1,1)，边长0.1，8个顶点）
center = np.array([1, 1, 1])
half_edge = 0.05  # 半边长，总边长0.1
# 8个顶点的相对位置（三维立方体的所有组合）
rel_vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]) * half_edge
initial_vertices = center + rel_vertices  # 初始顶点坐标

# 5. 让每个顶点按洛伦兹系统演化
evolved_vertices = []
for v0 in initial_vertices:
    # 求解单个顶点的轨迹
    sol = solve_ivp(
        fun=lambda t, s: lorenz_system(t, s, sigma, rho, beta),
        t_span=t_span,
        y0=v0,
        t_eval=t_eval,
        method='RK45'
    )
    evolved_vertices.append(sol.y.T)  # 每个顶点的轨迹：(100,3)
evolved_vertices = np.array(evolved_vertices)  # 8x100x3

# 6. 计算每个时间点的体积
volumes = []
for t_idx in range(len(t_eval)):
    # 提取每个时间点的8个顶点
    vertices_t = evolved_vertices[:, t_idx, :]
    vol = cube_volume(vertices_t)
    volumes.append(vol)

# 7. 绘图：体积随时间变化（直观看到收缩）
plt.figure(figsize=(10, 5))
plt.plot(t_eval, volumes, color='darkred', linewidth=2)
plt.xlabel('时间 t')
plt.ylabel('立方体体积')
plt.title('洛伦兹系统：相空间体积随时间收缩（耗散性可视化）')
plt.grid(True, alpha=0.3)
# 标注初始体积和最终体积
plt.annotate(f'初始体积：{volumes[0]:.6f}', xy=(0, volumes[0]), xytext=(1, volumes[0]*2),
             arrowprops=dict(arrowstyle='->', color='red'))
plt.annotate(f'10秒后体积：{volumes[-1]:.6f}', xy=(10, volumes[-1]), xytext=(8, volumes[-1]*100),
             arrowprops=dict(arrowstyle='->', color='red'))
plt.yscale('log')  # 对数坐标，更清晰看到指数级收缩
plt.show()