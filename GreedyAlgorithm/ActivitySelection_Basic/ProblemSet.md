**问题进阶版本见`DynamicPrograming/ActivitySelection_Advance`**

## 问题描述
出租一块场地, 这块场地可以在不同时间被不同的活动所使用. 但是, **每个时间段**只能由一个活动占用, 也就是说, 两个活动的时间**不能有冲突**(给定每个活动的起始时间和终止时间).

给定一系列活动, 求在这一段时间内, 怎样安排能够让这一段时间承办**尽可能多**的活动?

## 形式化定义
对于集合$S={a_1, a_2, ... a_N}$, 其中$a_i$代表第 i 个活动.
记活动$a_i$起始时间$s_i$, 终止时间$f_i$.
求下列问题最值:
$$
\max{|S'|} \\
\quad \text{s.t.} S'\subset S,\\ \quad 
\forall\ a_i, a_j \in S',\quad i\neq j,\quad
s_i \geq f_j\left(\text{活动 } a_i \text{ 排在 } a_j \text{ 后面}\right) 
\quad \text{或} \quad 
s_j \geq f_i\left(\text{活动 } a_j \text{ 排在 } a_i \text{ 后面}\right)
$$

