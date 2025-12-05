import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. 生成模拟二分类数据
np.random.seed(42)  # 固定随机种子，确保结果可复现
n_samples = 100

# 类别0：特征集中在(1,1)附近，标签为0
class0_X = np.random.normal(loc=[1, 1], scale=0.5, size=(n_samples, 2))
class0_y = np.zeros(n_samples)

# 类别1：特征集中在(3,3)附近，标签为1
class1_X = np.random.normal(loc=[3, 3], scale=0.5, size=(n_samples, 2))
class1_y = np.ones(n_samples)

# 合并数据
X = np.vstack((class0_X, class1_X))
y = np.hstack((class0_y, class1_y))

# 2. 训练逻辑回归模型
model = LogisticRegression(random_state=42)
model.fit(X, y)

# 3. 计算模型准确率（用训练集评估，实际中建议用测试集）
y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)

# 4. 生成网格数据，用于绘制决策边界
# 扩展特征范围，让决策边界更完整
x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
x2_min, x2_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

# 生成密集网格点（步长0.02，确保边界平滑）
xx1, xx2 = np.meshgrid(
    np.arange(x1_min, x1_max, 0.02),
    np.arange(x2_min, x2_max, 0.02)
)

# 对网格点预测类别（用于绘制决策区域）
Z = model.predict(np.c_[xx1.ravel(), xx2.ravel()])
Z = Z.reshape(xx1.shape)  # 恢复网格形状

# 5. 绘制可视化图
plt.figure(figsize=(10, 8))  # 设置图大小

# 5.1 绘制决策区域（根据预测结果填充颜色）
# alpha=0.2 控制透明度，避免覆盖数据点
plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=plt.cm.coolwarm)

# 5.2 绘制数据散点图（区分真实类别）
plt.scatter(class0_X[:, 0], class0_X[:, 1], c='blue', label='类别0 (y=0)', alpha=0.7, s=60)
plt.scatter(class1_X[:, 0], class1_X[:, 1], c='red', label='类别1 (y=1)', alpha=0.7, s=60)

# 5.3 标注模型信息（参数和准确率）
w1, w2 = model.coef_[0]  # 特征权重
b = model.intercept_[0]   # 偏置项
info_text = f"逻辑回归模型\nw1={w1:.3f}, w2={w2:.3f}, b={b:.3f}\n准确率={accuracy:.2f}"
plt.text(x1_min + 0.1, x2_max - 0.5, info_text, fontsize=12, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

plt.rcParams["font.family"] = ["PingFang SC", "WenQuanYi Micro Hei", "Heiti TC"]

# 5.4 设置图表标签和标题
plt.xlabel('特征1 (x1)', fontsize=12)
plt.ylabel('特征2 (x2)', fontsize=12)
plt.title('逻辑回归二分类结果可视化\n（蓝色区域=预测类别0，红色区域=预测类别1）', fontsize=14)
plt.legend(loc='lower right', fontsize=12)  # 图例位置
plt.grid(True, alpha=0.3)  # 网格线，增强可读性

# 显示图片
plt.show()