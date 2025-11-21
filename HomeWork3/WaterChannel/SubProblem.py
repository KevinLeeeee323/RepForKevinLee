'''
[问题描述]
    一个集合 U = {1, 2, 3, ..., m}(干旱区的 m 个城市)
    一个集合族 S = {S_1, S_2, ..., S_n},其中每个 S_i \\subset U(第 i 个蓄水厂能覆盖的干旱城市集合)

    目标：选择最少的 S_i,使得这些 S_i 的并集等于 U(覆盖所有元素)

[具体例子]
    假设：
    U = {1, 2, 3, 4, 5}(5个干旱城市)
    S_1 = {1, 2, 3}
    S_2 = {2, 4}  
    S_3 = {3, 4, 5}
    S_4 = {1, 5}
    问题：选最少的集合覆盖所有 1~5 号城市。

[请你思考]
    1. 贪心策略：每次选择哪个集合？为什么？
    2. 这个策略总是最优的吗？能否构造反例？
    3. 时间复杂度如何？
    4. 如何实现这个贪心算法？
'''


'''
先考虑一定能够覆盖到的情况. 存在覆盖不到的情况先不考虑.

最著名的集合覆盖贪心算法是： 每次选择能覆盖最多未覆盖元素的集合
被称为Greedy Set Cover Algorithm
发展历程:1974年由 David S. Johnson 在论文《Approximation algorithms for combinatorial problems》中首次证明; 
        1975年 László Lovász 也独立给出了类似分析
        (以上待考证)


我的想法:
按照长度对这些集合进行降序排序
然后从长度最长的开始选, 边选边维护一个统计覆盖情况的数组. 如果选了这个之后, 未覆盖到的元素个数没有减少, 那就不选. 如果有减少, 那就选.
'''

def SetCover_WithoutCost(universe: set, subsets: list[set]) -> tuple[list[set], set]:
    """
    集合覆盖贪心算法实现
    
    参数:
        universe: 全集U(待覆盖的所有元素集合)
        subsets: 子集族S(每个元素是一个子集,类型为set)
    
    返回:
        selected_subsets: 选中的子集组合(覆盖全集的最小近似解)
        covered_elements: 最终覆盖的元素集(若未完全覆盖,可查看未覆盖元素)
    """

    # 初始化:未覆盖元素 = 全集,选中子集为空,总成本为0
    uncovered = universe.copy()  # 避免修改原始全集
    selected_subsets = []

    # 贪心循环:直到所有元素被覆盖或无更多子集可选择
    while uncovered and subsets:
        # 计算每个子集的“覆盖当前未覆盖的元素的数量”(优先级指标)
        best_subset = None
        max_covered_cnt = -1  # 统计当前轮次中, 能覆盖最多为覆盖元素的子集

        for idx, subset in enumerate(subsets):
            # 该子集能覆盖的“未覆盖元素”数量
            covered_cnt = len(subset & uncovered)
            if covered_cnt == 0:
                continue  # 该子集无新覆盖元素,跳过

            # 选择覆盖未覆盖元素最多的子集
            if covered_cnt > max_covered_cnt:
                max_covered_cnt=covered_cnt
                best_subset = subset
                best_idx = idx  # 记录最优子集的索引,后续移除

        if best_subset is None: # 若没有找到能覆盖新元素的子集,退出循环(部分覆盖)
            break

        # 选中该子集:更新选中列表, 未覆盖元素
        selected_subsets.append(best_subset)
        uncovered -= best_subset  # 移除已覆盖的元素

        subsets.pop(best_idx) # 移除已选中的子集(避免重复选择), pop 方法传入要被移除的元素的id

    if not uncovered:
        print('fully covered')
    else:
        print('uncovered')
    return selected_subsets, (universe - uncovered)


# ------------------------------ 示例验证 ------------------------------
if __name__ == "__main__":
    
    U = {1, 2, 3, 4, 5}
    S_1 = {1, 2, 3}
    S_2 = {2, 4}  
    S_3 = {3, 4, 5}
    S_4 = {1, 5}

    subsets = [S_1, S_2, S_3, S_4]  # 子集族
    selected, covered = SetCover_WithoutCost(U, subsets)
    print(f"全集:{U}")
    print(f"选中的子集(共{len(selected)}个):{selected}")
    print(f"是否完全覆盖:{covered == U}\n")

