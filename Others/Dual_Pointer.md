## 一些双指针的题目的模板

### 基础模板
> LeetCode 1869
> 给你一个二进制字符串 s 。如果字符串中由 1 组成的 最长 连续子字符串 严格长于 由 0 组成的 最长 连续子字符串，返回 true ；否则，返回 false 。
例如，s = "110100010" 中，由 1 组成的最长连续子字符串的长度是 2 ，由 0 组成的最长连续子字符串的长度是 3 。
注意，如果字符串中不存在 0 ，此时认为由 0 组成的最长连续子字符串的长度是 0 。字符串中不存在 1 的情况也适用此规则。

```python
class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        i=0
        len_1_max=0
        len_0_max=0
        n=len(s)
        while i<n:
            j=i
            while j<n and s[j]==s[i]:
                j+=1
            if s[i]=='1':
                len_1_max=max(len_1_max, j-i)
            else:
                len_0_max=max(len_0_max, j-i)
            i=j
        return len_1_max>len_0_max
```

解读: 外层 `while i`, 内层 `while j`, 每操作完一次, `i=j`将i 调到下一处位置.
Tips: 代码中`if s[i]=='1':`如果是访问`s[j]`, 需要先检验`j<n`, **以免数组越界访问**
适用题目类型: 约束较少的遍历
其他应用场景: LeetCode 2414, 1446, 485

另一种写法:
> LeetCode 2511
> 给你一个长度为 n ，下标从 0 开始的整数数组 forts ，表示一些城堡。forts[i] 可以是 -1 ，0 或者 1 ，其中：
-1 表示第 i 个位置 没有 城堡。
0 表示第 i 个位置有一个 敌人 的城堡。
1 表示第 i 个位置有一个你控制的城堡。
现在，你需要决定，将你的军队从某个你控制的城堡位置 i 移动到一个空的位置 j ，满足：
0 <= i, j <= n - 1
军队经过的位置 只有 敌人的城堡。正式的，对于所有 min(i,j) < k < max(i,j) 的 k ，都满足 forts[k] == 0 。
当军队移动时，所有途中经过的敌人城堡都会被 摧毁 。
请你返回 最多 可以摧毁的敌人城堡数目。如果 无法 移动你的军队，或者没有你控制的城堡，请返回 0 。
示例 1：
输入：forts = [1,0,0,-1,0,0,0,0,1]
输出：4
解释：
    - 将军队从位置 0 移动到位置 3 ，摧毁 2 个敌人城堡，位置分别在 1 和 2 。
    - 将军队从位置 8 移动到位置 3 ，摧毁 4 个敌人城堡。
4 是最多可以摧毁的敌人城堡数目，所以我们返回 4 。
示例 2：
输入：forts = [0,0,1,-1]
输出：0
解释：由于无法摧毁敌人的城堡，所以返回 0 。

分析: 只要统计每一对出现的(-1, 1)或者(1, -1)之间出现的最多的0的个数就行.

```python
class Solution:
    def captureForts(self, forts: List[int]) -> int:
        cnt=0
        i=0
        n=len(forts)
        while i<n:
            if forts[i]!=0:
                j=i+1
                while j<n and forts[j]==0:
                    j+=1
                if j<n and forts[j]+forts[i]==0:
                    cnt=max(cnt, j-i-1)
                i=j
            else:
                i+=1
        return cnt
```
解读: 
相比于基础模板, 这里i 跳动的逻辑更直观一些. 符合条件`if forts[i]!=0`就进行计数等操作, 如果不满足就让`i+=1`.
Tips: `while j<n and forts[j]==0`这里访问了 j, 为了避免越界, 要先检验`j<n`.