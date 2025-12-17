import numpy as np
from scipy.optimize import linprog

# 1. 定义目标函数系数（按x1, x2, x3顺序）
c = [1, 3, -2]

# 2. 定义不等式约束 A*x <= b
# 对应：x2 + 2x3 <=4；-5x2 -2x3 <=-1（即5x2+2x3>=1）
A = np.array([
    [0, 1, 2],
    [0, -5, -2]
])
b = np.array([4, -1])

# 3. 定义等式约束 Aeq*x = beq
# 对应：x1 - x2 + x3 =5
A_eq = np.array([[1, -1, 1]])
b_eq = np.array([5])

# 4. 定义变量上下界（x1,x2,x3 >=0，无上界则设为None）
# bounds格式：[(x1下界, x1上界), (x2下界, x2上界), (x3下界, x3上界)]
bounds = [(0, None), (0, None), (0, None)]

# 5. 调用linprog求解（method指定求解器，'highs'为推荐的高效求解器）
result = linprog(
    c=c,
    A_ub=A,
    b_ub=b,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method='highs',  # 推荐使用highs求解器（scipy 1.6+支持）
    options={'disp': False}  # 关闭迭代过程输出
)

# 6. 输出结果
if result.success:
    print("求解成功！")
    print(f"最优解：")
    print(f"x1 = {result.x[0]:.4f}")
    print(f"x2 = {result.x[1]:.4f}")
    print(f"x3 = {result.x[2]:.4f}")
    print(f"目标函数最小值 = {result.fun:.4f}")
else:
    print(f"求解失败，原因：{result.message}")