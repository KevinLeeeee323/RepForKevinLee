import numpy as np
# 求一组数据的样本方差
def GetSampleVar(data):
    len=np.size(data)
    var=np.sum(np.square(data-np.mean(data)))/(len-1)
    return var

def main():
    print('这是一个计算样本方差的程序')
    ori_data=input('请输入这组数据,空格分隔,以回车作为结束\n').split(' ')
    data=np.reshape(np.array(ori_data, dtype=np.float64), (1, -1))
    print(data)
    var=GetSampleVar(data)
    print(f'data:{data}', f'the sample variance of this group of data is {var}', sep='\n')

if __name__=='__main__':
    main()
