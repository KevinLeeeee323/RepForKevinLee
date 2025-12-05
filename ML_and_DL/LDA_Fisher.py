import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import make_classification

class FisherLDA():
    def __init__(self, dataset) -> None:
        self.dataSet=np.array(dataset)
        self.dataSize=self.dataSet.shape[0]
        self.varShape=self.dataSet.shape[1]-1 # 数据特征维度
        
        half=self.dataSize//2
        self.trainSet=dataset[0:half]
        self.testSet=dataset[half:]

        self.label_idx=self.dataSize-1 # 标签所在列的下标
    
    def Train(self)->None:
        """
        训练过程：计算类内散度矩阵 Sw, 得到投影向量 w 和偏置 b
        """

        posClass = self.trainSet[self.trainSet[:, self.label_idx] == 1][:, :self.varShape]
        negClass = self.trainSet[self.trainSet[:, self.label_idx] == -1][:, :self.varShape]
        '''
        self.trainSet[:, self.label_idx] == 1 是一个布尔索引，生成一个形状为 (n_samples,) 的布尔数组，表示哪些样本的标签为 1
        numpy 数组如果索引是布尔数组, 会去找那些布尔数组中元素为 True 的项.
        [:, :self.varShape]表示只取这些样本的前 self.varShape 列（即特征部分）
        '''


        def S_withinClass(subset)->tuple[np.ndarray, np.ndarray]:
            """
            计算单类的类内散度矩阵和均值向量
            """
            mean=np.mean(subset, axis=0)
            mat=np.zeros(shape=(self.varShape, self.varShape))
            for x in subset:
                to_mean=x-mean
                
                mat+=np.outer(to_mean, to_mean) # 构成类间散度矩阵
            return mat, mean
        
        S1, m1=S_withinClass(posClass)
        S0, m0=S_withinClass(negClass)
        Sw=np.array(S0+S1)
        Sw_inv=np.linalg.inv(Sw)
        w=Sw_inv@(m1-m0)
        b=-0.5*(w@(m1+m0))
        
        self.w=w
        self.b=b

    def Predict(self, x)->int:
        x=np.array(x).flatten()
        if x.shape[0]==self.varShape:
            result=self.w@x+self.b
            if result>0:
                return 1 # 预测为正类
            else:
                return -1 # 预测为反类
        else:
            raise ValueError(f"输入特征维度错误: 应为 {self.varShape}, 实际为 {x.shape[0]}")


    def Test_and_show(self): 
        ''' 
            对给定测试集输出结果, 并且返回正确率
            在二维场景下展示分类结果
        '''
        testCnt=self.dataSize//2
        rightCnt=0
        plt.figure()
        for item in self.testSet:
            result=self.w@item[0:2]+self.b
            if result * item[2]>=0:
                rightCnt+=1
                if item[2]==1:
                    color='g' # 分类正确的正类
                else:
                    color='b' # 分类正确的反类
            else:
                color='r' # 分类错误的
            plt.scatter(item[0], item[1], c=color)
        
        # 构建直线 y = (-w0*x - b)/w1
        x_line = np.linspace(np.min(X[:,0]), np.max(X[:,0]), 100)
        y_line = -(self.w[0] * x_line + self.b) / self.w[1]
        plt.plot(x_line, y_line, label='LDA Boundary')
        plt.show()

        return rightCnt/testCnt # 分类正确率

        
if __name__=='__main__':

    # 生成 Train Set
    SampleNum=60
    X, Y = make_classification(n_samples=SampleNum, n_features=2, n_redundant=0, n_classes=2, n_informative=2,
                           n_clusters_per_class=1, class_sep=0.8, random_state=10)
    Y=2*Y-1 # 标签变为 1, -1
    Y=np.reshape(Y, shape=(SampleNum, -1))

    Data=np.hstack((X, Y))
    myLDA=FisherLDA(Data)
    myLDA.Train()
    print(myLDA.Test_and_show())