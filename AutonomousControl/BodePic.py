import numpy as np
import matplotlib.pyplot as plt
from control import TransferFunction, frequency_response

# ----------------------
# 1. 定义积分环节传递函数 G(s) = 1/(s)（频域 G(jω) = 1/(jω)）
# ----------------------
num = [1]       # 分子：1
den = [2, 1, 0]    # 分母：s（即 s + 0）
G = TransferFunction(num, den)

# ----------------------
# 2. 设置频率范围（对数刻度，0.01 ~ 100 rad/s，1000个点）
# ----------------------
omega = np.logspace(-2, 2, 1000)  # 对数分布的频率轴，符合Bode图规范

# ----------------------
# 3. 计算频率响应（替代旧版 bode_plot 的返回值）
# ----------------------
# frequency_response 返回 (mag, phase, omega)，mag为幅值（非dB），phase为弧度
mag, phase_rad, omega_out = frequency_response(G, omega)

# 转换为控制工程标准格式：幅频特性（dB）、相频特性（度）
mag_dB = 20 * np.log10(mag.squeeze())  # 20log10(幅值)，squeeze()去除多余维度
phase_deg = np.rad2deg(phase_rad.squeeze())  # 弧度转角度

# ----------------------
# 4. 手动绘制Bode图（幅频+相频子图）
# ----------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)  # 共享x轴（频率轴）

# 上子图：幅频特性（对数频率轴，dB值）
ax1.semilogx(omega_out, mag_dB, color='blue', linewidth=2)
ax1.set_ylabel('幅频特性 (dB)', fontsize=10)
ax1.set_title('积分环节 G(jω) = 1/(jω) 的 Bode 图', fontsize=12)
ax1.grid(True, which="both", ls="-")  # 显示网格（both：线性+对数刻度）
ax1.set_ylim([-100, 20])  # 合理设置y轴范围，避免图形过扁

# 下子图：相频特性（对数频率轴，角度）
ax2.semilogx(omega_out, phase_deg, color='red', linewidth=2)
ax2.set_xlabel('频率 ω (rad/s)', fontsize=10)
ax2.set_ylabel('相频特性 (deg)', fontsize=10)
ax2.grid(True, which="both", ls="-")
ax2.set_ylim([-100, 0])  # 积分环节相频恒为-90°，缩小范围更清晰
ax2.axhline(y=-90, color='black', linestyle='--', alpha=0.5)  # 添加-90°参考线

# 调整子图间距，避免标签重叠
plt.tight_layout()
plt.show()