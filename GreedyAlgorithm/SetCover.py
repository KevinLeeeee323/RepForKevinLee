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

    最著名的集合覆盖贪心算法是： 每次选择能覆盖最多未覆盖元素的集合
    被称为Greedy Set Cover Algorithm
'''


def SetCover_WithCost(universe: set, subsets: list[set], costs: list[float] = None) -> tuple[list[set], float, set]:
    """
    集合覆盖贪心算法实现(支持带成本和无成本场景)
    
    参数:
        universe: 全集U(待覆盖的所有元素集合)
        subsets: 子集族S(每个元素是一个子集,类型为set)
        costs: 每个子集对应的成本(可选,默认None表示无成本,所有子集成本为1)
    
    返回:
        selected_subsets: 选中的子集组合(覆盖全集的最小近似解)
        total_cost: 选中子集的总成本(无成本时为选中子集的个数)
        covered_elements: 最终覆盖的元素集(若未完全覆盖,可查看未覆盖元素)
    """
    # 初始化:未覆盖元素 = 全集,选中子集为空,总成本为0
    uncovered = universe.copy()  # 避免修改原始全集
    selected_subsets = []
    total_cost = 0.0

    # 处理成本参数:无成本时默认每个子集成本为1
    if costs is None:
        costs = [1.0 for _ in subsets]
    # 校验:子集数与成本数必须一致
    assert len(subsets) == len(costs), "子集数与成本数不匹配！"

    # 贪心循环:直到所有元素被覆盖或无更多子集可选择
    while uncovered and subsets:
        # 计算每个子集的“单位成本覆盖数”(优先级指标)
        best_subset = None
        best_efficiency = -1.0  # 单位成本覆盖的未覆盖元素数(初始为-1,确保至少选择一个有效子集)
        best_cost = 0.0

        for idx, subset in enumerate(subsets):
            # 该子集能覆盖的“未覆盖元素”数量
            covered_count = len(subset & uncovered)
            if covered_count == 0:
                continue  # 该子集无新覆盖元素,跳过

            # 计算单位成本覆盖数(效率):覆盖数 / 成本(越大越优)
            efficiency = covered_count / costs[idx]

            # 选择效率最高的子集(若效率相同,选成本最低的；成本也相同选第一个)
            if (efficiency > best_efficiency) or \
               (efficiency == best_efficiency and costs[idx] < best_cost):
                best_efficiency = efficiency
                best_subset = subset
                best_cost = costs[idx]
                best_idx = idx  # 记录最优子集的索引,后续移除

        # 若没有找到能覆盖新元素的子集,退出循环(部分覆盖)
        if best_subset is None:
            break

        # 选中该子集:更新选中列表、总成本、未覆盖元素
        selected_subsets.append(best_subset)
        total_cost += best_cost
        uncovered -= best_subset  # 移除已覆盖的元素

        # 移除已选中的子集(避免重复选择)
        subsets.pop(best_idx)
        costs.pop(best_idx)

    if not uncovered:
        print('fully covered')
    else:
        print('uncovered')
    return selected_subsets, total_cost, (universe - uncovered)


# ------------------------------ 示例验证 ------------------------------
if __name__ == "__main__":
    # 示例1:无成本场景(仅追求“子集个数最少”)
    print("=== 示例1:无成本集合覆盖 ===")
    universe1 = {1, 2, 3, 4, 5, 6}  # 全集
    subsets1 = [
        {1, 2, 3},
        {4, 5, 6},
        {1, 4},
        {2, 5},
        {3, 6}
    ]  # 子集族
    selected1, cost1, covered1 = SetCover_WithCost(universe1, subsets1)
    print(f"全集:{universe1}")
    print(f"选中的子集(共{len(selected1)}个):{selected1}")
    print(f"总成本(子集个数):{cost1}")
    print(f"是否完全覆盖:{covered1 == universe1}\n")

    # 示例2:带成本场景(追求“总成本最低”)
    print("=== 示例2:带成本集合覆盖 ===")
    universe2 = {"a", "b", "c", "d", "e"}  # 全集
    subsets2 = [
        {"a", "b", "c"},  # 成本3
        {"c", "d"},       # 成本2
        {"d", "e"},       # 成本2
        {"a", "e"}        # 成本3
    ]  # 子集族
    costs2 = [3.0, 2.0, 2.0, 3.0]  # 每个子集的成本
    selected2, cost2, covered2 = SetCover_WithCost(universe2, subsets2, costs2)
    print(f"全集:{universe2}")
    print(f"选中的子集:{selected2}")
    print(f"总成本:{cost2:.1f}")
    print(f"是否完全覆盖:{covered2 == universe2}\n")

    # 示例3:部分覆盖场景(无子集能覆盖所有元素)
    print("=== 示例3:部分覆盖场景 ===")
    universe3 = {10, 20, 30, 40}
    subsets3 = [
        {10, 20},
        {20, 30}
    ]
    selected3, cost3, covered3 = SetCover_WithCost(universe3, subsets3)
    print(f"全集:{universe3}")
    print(f"选中的子集:{selected3}")
    print(f"覆盖的元素:{covered3}")
    print(f"未覆盖的元素:{universe3 - covered3}")