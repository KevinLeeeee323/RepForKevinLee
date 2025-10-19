import numpy as np

# 奖励矩阵，-1表示不可达，0表示可达但无即时奖励，100表示到达目标
R = -1*np.ones((8,8))
R[0,4]=R[4,0]=0
R[4,5]=R[5,4]=0
R[1,5]=R[5,1]=0
R[1,2]=R[2,1]=0
R[2,3]=R[3,2]=0
R[2,6]=R[6,2]=0
R[7,6]=R[6,7]=0
R[5,6]=R[6,5]=0
R[2,3]=100

Q = np.zeros(shape=np.shape(R))

# 学习参数
gamma = 0.8

goal = 3

for episode in range(1000):
# 随机选择初始状态
    current_state = np.random.randint(0, np.shape(R)[0])
    
    # 直到到达目标状态
    while current_state != goal:
        # 找出所有不为-1的状态
        possible_actions = []
        for action in range(np.shape(R)[0]):
            if R[current_state, action] >= 0:
                possible_actions.append(action)
        
        action = np.random.choice(possible_actions)
        Q[current_state, action] = R[current_state, action] + gamma * np.max(Q[action, :])
        
        # 转移到下一个状态
        current_state = action

print("训练后的Q矩阵:")
print(Q)

# 根据Q矩阵找到最优路径
def find_path(start_state):
    path = [start_state]
    current_state = start_state
    
    while current_state != goal:
        # 选择Q值最大的动作
        next_state = np.argmax(Q[current_state, :])
        path.append(int(next_state))
        current_state = next_state
        # 防止循环
        if len(path) > 10:
            break
            
    return path

# 测试从各个状态出发的最优路径
print("\n最优路径:")
for state in range(6):
    if state != goal:
        path = find_path(state)
        print(f"状态{state}路径为{path}")