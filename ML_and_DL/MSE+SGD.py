import sys

m=int(sys.stdin.readline().strip())
N=int(sys.stdin.readline().strip())
alpha=float(sys.stdin.readline().strip())
xs=[]
ys=[]

xs_max=[0, 0, 0]
MAXs=[10000, 100000, 100]

xs_min=MAXs.copy()
for i in range(m):
    x1, x2, x3, y=map(int, sys.stdin.readline().split())
    tmp=[x1, x2, x3, y]
    for i in range(3):
        xs_min[i]=min(xs_min[i], tmp[i])
        xs_max[i]=max(xs_max[i], tmp[i])
    xs.append([x1, x2, x3])
    ys.append(y)

xs_norm=[[0.0 for i in range(3)] for i in range(m)]

for i in range(m):
    for j in range(3):
        if xs_max[j]==xs_min[j]:
            xs_norm[i][j]=0
        else:
            xs_norm[i][j]=(xs[i][j]-xs_min[j])/(xs_max[j]-xs_min[j])

w=[0.0, 0.0, 0.0, 0.0]
for i in range(N):
    grad=[0.0, 0.0, 0.0, 0.0]
    for j in range(m):
        y_pred=0
        for k in range(1, 4):
            y_pred+=w[k]*xs_norm[j][k-1]
        y_pred+=w[0]

        grad[0]+=(y_pred-ys[j])
        for k in range(1, 4):
            grad[k]+=(y_pred-ys[j])*(xs_norm[j][k-1])
    
    # update
    for k in range(4):
        w[k]-=alpha/m*grad[k]

w_normed=[0.0, 0.0, 0.0, 0.0]
for k in range(1, 4):
    if xs_max[k-1]==xs_min[k-1]:
        w_normed[k]=0
    else:
        w_normed[k]=w[k]/(xs_max[k-1]-xs_min[k-1])

w_normed[0]=w[0]-sum(w_normed[j]*xs_min[j-1] for j in range(1, 4))


result = [f"{round(val, 2):.2f}" for val in w_normed]
print(" ".join(result))
'''
round() 的标准语法是：round(number, ndigits=None)
    number： 需要处理的数字（通常是浮点数）。
    ndigits： 需要保留的小数位数

既然 round(val, 2) 已经保留两位小数了，为什么还要加上 :.2f？
这是因为 round() 负责改变数值大小，而 :.2f 负责控制字符串显示的格式。
假设我们算出来的权重刚好是 2.10003：
round(2.10003, 2) 运算后的数值变成了 2.1（浮点数末尾的无意义 0 会被丢弃）。
但题目要求输出格式必须是严格的两位小数形式（例如 2.10）。
这时用 f"{2.1:.2f}"，强制把它格式化为字符串 "2.10"，就能完美满足 OJ 系统（评测机）的格式校验。

题目要求输出一行，4 个浮点数，依次为还原后的w0'~w3' ，结果保留 2 位小数，银行家舍入，以一个空格分隔，前后无冗余空格。
" ".join(result)
" ".join()的含义: 以空格分隔
"\n".join()的含义: 以换行符分隔
()里面的东西必须是字符串. 而 result 正是把每个输出的浮点数, 都提前转换成了字符串.
'''


results=[f"{round(w_normed[i]):.2f}" for i in range(4)]
print(" ".join(results))

