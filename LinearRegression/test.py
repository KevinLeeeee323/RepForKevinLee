import numpy as np
from scipy import stats

n=int(input('请输入样本数据对(x, y)的数量\n'))

data = np.loadtxt('data.txt', delimiter=' ', dtype=np.float32)
x = data[0, :]  # 第1列作为x
y = data[1, :]  # 第2列作为y

for i in x:
    print(i)
print('---------')
for i in y:
    print(i)
# print(np.sum(x), np.mean(x), np.sum(np.square(x)), np.sum(y), np.mean(y), np.sum(np.square(y)))12
print(np.size(x))