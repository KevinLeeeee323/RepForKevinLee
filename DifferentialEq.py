import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import itertools

# 定义微分方程组: dx/dt = x + y, dy/dt = x - 3y
def system(t, state):
    x, y = state
    dxdt =y**3-4*x    # dx/dt的表达式
    dydt = y**3-y-3*x   # dy/dt的表达式
    return [dxdt, dydt]

# 时间范围
t_start = 0
t_end = 0.08
t_eval = np.linspace(t_start, t_end, 100)  # 用于绘图的时间点

x0s=np.arange(2, 3, 0.4)
y0s=np.arange(2, 3, 0.4)

# 创建图形
plt.figure(figsize=(8, 4))
# 设置图形属性
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 5)   # x轴范围
plt.ylim(0, 5)  # y轴范围

# 求解并绘制每个初始条件下的轨迹
for (x0, y0) in itertools.product(x0s, y0s):
    # 求解微分方程
    solution = solve_ivp(
        system, 
        [t_start, t_end], 
        [x0, y0], 
        t_eval=t_eval,
        method='RK45'  # 龙格-库塔方法
    )
    
    # 提取解
    x = solution.y[0]
    y = solution.y[1]
    
    # 绘制轨迹
    plt.plot(x, y)
    
    # 绘制初始点（用圆点标记）
    plt.scatter(x0, y0, color='black', s=20)



plt.title('Track')
plt.grid(True)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
# plt.legend(loc='best')
plt.axis('equal')  # 等比例坐标轴
plt.show()