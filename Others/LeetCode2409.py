'''
LeetCode 2409: https://leetcode.cn/problems/count-days-spent-together/description/

Alice 和 Bob 计划分别去罗马开会。
给你四个字符串 arriveAlice ，leaveAlice ，arriveBob 和 leaveBob 。
Alice 会在日期 arriveAlice 到 leaveAlice 之间在城市里（日期为闭区间），
而 Bob 在日期 arriveBob 到 leaveBob 之间在城市里（日期为闭区间）。
每个字符串都包含 5 个字符，格式为 "MM-DD" ，对应着一个日期的月和日。

请你返回 Alice和 Bob 同时在罗马的天数。
你可以假设所有日期都在 同一个 自然年，而且 不是 闰年。
每个月份的天数分别为：[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 。
'''


'''
这道题有如下几个可以注意的地方:
1. 月+日 映射到 连续整数, 即从这一年的第一天开始, 是当前第几天.
    由于这道题规定了在同一年, 因此不用考虑年的事. 
    为更高效率地做这个映射, 可以用前缀和. 见下面的 pre_days 数组, 以及对应的转换方式.
2. 映射完之后, 问题就转变成了 [A_begin, A_end]和[B_begin, B_end]两个闭区间的交集上有多少个整数.
   其中两个区间一共四个端点都是整数.
   统计方法见下:
    if A_begin>B_end or A_end<B_begin:
        return 0
    else:
        return min(B_end, A_end)-max(A_begin, B_begin)+1
'''

class Solution:
    def countDaysTogether(self, arriveAlice: str, leaveAlice: str, arriveBob: str, leaveBob: str) -> int:

        def to_date(s):
            return map(int, s.split('-'))
        arr_A_m, arr_A_d=to_date(arriveAlice)
        lea_A_m, lea_A_d=to_date(leaveAlice)
        arr_B_m, arr_B_d=to_date(arriveBob)
        lea_B_m, lea_B_d=to_date(leaveBob)

        days=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        pre_days=[0]
        for day in days:
            pre_days.append(pre_days[-1]+day)
        A_begin=pre_days[arr_A_m-1]+arr_A_d
        A_end=pre_days[lea_A_m-1]+lea_A_d
        B_begin=pre_days[arr_B_m-1]+arr_B_d
        B_end=pre_days[lea_B_m-1]+lea_B_d

        if A_begin>B_end or A_end<B_begin:
            return 0
        else:
            return min(B_end, A_end)-max(A_begin, B_begin)+1

if __name__=='__main__':   

    # test examples
    arriveAlice = "09-01"; leaveAlice = "10-19"
    arriveBob = "6-19"; leaveBob = "10-20"
    print(Solution().countDaysTogether(arriveAlice, leaveAlice, arriveBob, leaveBob))
