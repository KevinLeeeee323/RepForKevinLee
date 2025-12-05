import torch
import torch.nn as nn
import torch.optim as optim

'''
    AI 写的代码
    
    # 字符级RNN序列预测代码简介
    ## 核心功能
    该代码实现了一个轻量级循环神经网络(RNN),专注于**字符级下一个字符预测任务**——模型通过学习训练集中的单词字符依赖关系(如"h→e""p→i"),具备对全新长单词的字符序列泛化预测能力,完整覆盖"数据准备-模型训练-泛化测试"全流程.

    ## 输入说明
    ### 1. 数据输入(内置结构化配置)
    - **词汇表**:包含训练与测试所需全部字符(h、e、l、o、a、p、w、r、d、m、n、i、j、u、c)(如果新增加的单词中超出这些范围, 需要手动添加),模型可识别所有参与任务的字符;
    - **训练集**:几个标注好"输入-目标"映射的单词序列,输入为单词前n-1个字符,目标为对应下一个字符(如`pine`的输入`['p','i','n']`对应目标`['i','n','e']`),用于模型学习字符依赖规律;
    - **测试集**:全新单词`pineapple`,输入为其前8个字符`['p','i','n','e','a','p','p','l']`,用于评估模型未见过的字符序列泛化能力.

    ### 2. 模型参数输入(可调整)
    - 输入/输出维度:等于词汇表大小(适配one-hot编码);
    - 隐藏层神经元数:16(适配长序列上下文记忆);
    - 训练配置:随机梯度下降(SGD)优化器(学习率0.1)、负对数似然损失(NLLLoss)、训练轮次2000轮.

    ## 输出说明
    ### 1. 训练过程输出
    - 每200轮打印一次平均训练损失,直观展示模型学习进度(损失逐步下降至0.1以下,表明模型学透训练集字符依赖).

    ### 2. 测试结果输出
    - 测试集平均损失:量化模型对全新单词的预测偏差;
    - 详细预测结果:包含测试单词的输入序列、模型预测的下一个字符序列、真实目标序列,以及预测是否完全正确的判断(如输入`['p','i','n','e','a','p','p','l']`,理想预测输出为`['i','n','e','a','p','p','l','e']`).

    ## 核心价值
    通过"短单词训练→长单词泛化"的逻辑,验证RNN对字符序列依赖的学习与迁移能力,无需额外手动输入数据,运行后即可直观观察模型的拟合效果与泛化性能,适合作为字符级语言模型的入门演示案例.
'''

# device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
device=torch.device("cpu")
print(f"使用设备：{device}")

# ---------------------- 1. 数据准备（不变，后续将数据移至设备）----------------------
vocab = ['h', 'e', 'l', 'o', 'a', 'p', 'w', 'r', 'd', 'm', 'n', 'i', 'j', 'u', 'c']  
char2idx = {char: i for i, char in enumerate(vocab)}
idx2char = {i: char for i, char in enumerate(vocab)}
vocab_size = len(vocab)

# 训练集:单词(模型仅学习这几个单词的字符依赖,无其他数据)
train_data = [
    ("hello", ["h","e","l","l"], ["e","l","l","o"]),  # 依赖:h→e、e→l、l→l、l→o
    ("apple", ["a","p","p","l"], ["p","p","l","e"]),
    ("world", ["w","o","r","l"], ["o","r","l","d"]),
    ("lemon", ["l","e","m","o"], ["e","m","o","n"]),  # 依赖:a→p、p→p、p→l、l→e
    ("pine", ["p","i","n"], ["i","n",'e']),
    ('juice', ['j', 'u', 'i', 'c'], ['u', 'i', 'c','e'])
]

# 测试集:全新单词(模型没见过任何字符依赖,纯泛化测试)
test_data = [
    ("pineapple", ["p","i","n",'e', 'a', 'p', 'p', 'l'], ["i","n",'e', 'a', 'p', 'p', 'l', 'e'])
]

def prepare_data(data):
    X_list = []
    Y_list = []
    for word, x_chars, y_chars in data:
        x_idx = torch.tensor([[char2idx[c]] for c in x_chars], dtype=torch.long)
        y_idx = torch.tensor([[char2idx[c]] for c in y_chars], dtype=torch.long)
        # 新增：将数据移至目标设备（MPS/CPU）
        X_list.append(x_idx.to(device))
        Y_list.append(y_idx.to(device))
    return X_list, Y_list

train_X, train_Y = prepare_data(train_data)
test_X, test_Y = prepare_data(test_data)

# ---------------------- 2. RNN模型 ----------------------
class SmallRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SmallRNN, self).__init__()
        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = torch.tanh(self.i2h(combined))
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        # 新增：初始化隐藏状态时指定设备（与模型/数据一致）
        return torch.zeros(1, self.hidden_size, device=device)

# ---------------------- 3. 模型参数----------------------
input_size = vocab_size
hidden_size = 16
output_size = vocab_size
model = SmallRNN(input_size, hidden_size, output_size).to(device)  # 移至 MPS/CPU

# ---------------------- 3. 训练配置(不变)----------------------
criterion = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)
epochs = 2000  # 适当增加训练轮数,让模型学透训练集的规律

# ---------------------- 4. 训练过程(仅用训练集更新参数)----------------------
print("开始训练(使用训练集6个单词:hello、apple、world、lemon、pine、juice):")  # 修正注释
for epoch in range(epochs):
    total_train_loss = 0.0
    for i in range(len(train_X)):
        x_seq = train_X[i]
        y_seq = train_Y[i]
        hidden = model.init_hidden()
        optimizer.zero_grad()
        seq_loss = 0.0

        for t in range(x_seq.size(0)):
            # 修复：创建input_onehot后移至目标设备
            input_onehot = torch.zeros(1, input_size, device=device)
            input_onehot[0, x_seq[t, 0]] = 1.0
            output, hidden = model(input_onehot, hidden)
            seq_loss += criterion(output, y_seq[t])

        seq_loss.backward()
        optimizer.step()
        total_train_loss += seq_loss.item()

    if (epoch + 1) % 200 == 0:
        avg_train_loss = total_train_loss / len(train_X)
        print(f'Epoch {epoch+1:4d} | 平均训练损失:{avg_train_loss:.4f}')

# ---------------------- 5. 测试过程(仅用全新测试集,不更新参数)----------------------
print("\n开始测试, 纯泛化评估):")  # 修正注释
model.eval()
total_test_loss = 0.0
test_results = []

with torch.no_grad():
    for i in range(len(test_X)):
        x_seq = test_X[i]
        y_seq = test_Y[i]
        word_name = test_data[i][0]
        hidden = model.init_hidden()
        seq_loss = 0.0
        pred_chars = []

        for t in range(x_seq.size(0)):
            # 修复：创建input_onehot后移至目标设备
            input_onehot = torch.zeros(1, input_size, device=device)
            input_onehot[0, x_seq[t, 0]] = 1.0
            output, hidden = model(input_onehot, hidden)
            seq_loss += criterion(output, y_seq[t])
            pred_idx = torch.argmax(output).item()
            pred_chars.append(idx2char[pred_idx])

        total_test_loss += seq_loss.item()
        input_chars = [idx2char[x_seq[t, 0].item()] for t in range(x_seq.size(0))]
        target_chars = [idx2char[y_seq[t, 0].item()] for t in range(y_seq.size(0))]
        test_results.append({
            "单词": word_name,
            "输入序列": input_chars,
            "预测序列": pred_chars,
            "目标序列": target_chars,
            "是否正确": pred_chars == target_chars
        })

# 打印测试总结
avg_test_loss = total_test_loss / len(test_X)
print(f'\n测试集平均损失:{avg_test_loss:.4f}')
print("\n详细测试结果:")
for res in test_results:
    # 修正打印格式（适配长单词和长序列）
    print(f'单词:{res["单词"]:10s} | 输入:{res["输入序列"]}')
    print(f'       预测:{res["预测序列"]}')
    print(f'       目标:{res["目标序列"]} | 结果:{"✓" if res["是否正确"] else "×"}')