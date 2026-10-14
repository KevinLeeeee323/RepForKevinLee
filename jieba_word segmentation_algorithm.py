'''
jieba 分词.
当一段连续文本, 有大量词典里存在的词, 使用DAG(Directed Acyclic Graph, 有向无环图)的方式进行处理.
图中:
    节点为: 对应的下标: 0, 1, 2, ...n-1
    边为 i->j, 如果 文本的子字符串 s[i...j](s_i, s_i+1, ... s_j-1)在字典中

e.g.: s="你好生活", 你<->0, 好<->1, 生<->2, 活<->3, 构成的 DAG 中:
    节点: 0, 1, 2, 3
    边: 
        0->1, 因为 你 在字典中
        0->2 你好 在字典中
        1->2 因为 好 在字典中
        1->3 因为 好生 在字典中
        2->3 因为 生 在字典中
        2->4 因为 生活 在字典中
        3->4 因为 活 在字典中
    由此构成了 DAG.
    DAG 中每一条起点为 0, 终点为 n(这里 n=4)的路径, 都是一种划分方式.
    e.g.  0->1->3->4 为 "你 / 好生 / 活"
          0->2->4 为 "你好 / 生活"
    因此, 可以遍历所有的路径, 从中选出最合理的.
    这里合理可以定义为, 该路径中分词出现频率之乘积, 或者, 频率的对数之和.

    需要注意的是, DAG规定有哪些分词方式可供选择, 而目标函数则定义什么样的分词更合理.
    比如在这里, 就定义"最大化所有分词词语的概率乘积"为"最合理的分词方式".
    完全可以定义其他目标函数。例如：
        - 最少词数： 倾向于将较长的连续字符划分成一个词。
        - 最大化词频之积： 倾向于选择词频较高的组合。
        - 最大化词语得分之和： 为每个候选词设置一个分数，再最大化总分。
        - 考虑上下文： 不仅考虑单个词的频率，还考虑相邻词之间的搭配概率。
    这些目标函数可能得到不同的分词结果。
    但有一点需要注意：目标函数改变后，是否还能用动态规划高效求解，需要进一步分析。
    并不是任意目标函数都适合使用同一种 DP 状态转移。


若某一段连续文本，DAG 扫描后**所有起始位置都不存在任何≥2 个字的词典词条**，
DAG 仅能生成连续的单字候选边，无法找到任何多字候选词，
则判定该连续区间为**OOV 未登录词片段**（词典未收录的新词、人名、专有名词等）。
针对该 OOV 片段，jieba 将其单独截取，启用HMM + Viterbi做 B/M/E/S 字符级序列标注：
将分词任务转化为给每个汉字打标签（B 词首、M 词中、E 词尾、S 单字词）。
HMM 依靠预训练的初始状态概率、状态转移概率、字符发射概率，
通过 Viterbi 动态规划解码，输出概率最大的 BEMS 标签序列；
再根据标签还原词语边界，完成未登录新词识别。
    
以下部分的参数说明:
s: 待分词的字符串, 长度为 n.
wd: 
    word_dict, wd 中各个词典的频率, wd[word]=p, 值为概率, 也就是词频, 默认在[0, 1]之间;
    假设 word_dict 中收录了所有的单字, 让每个 s[i:i+1](也就是 s[i])都可以在字典中找到

但实际以下只实现了 DAG 情形的 jieba 分词, 没有管 HMM+Viterbi 算法负责的部分
而且默认没有考虑很多工程排除 bug 的边界情况, 比如 word_dict 中概率<0 ...
'''

import math

def my_jieba_word_segmentation(s:str, wd:dict):

    # 此为暴力遍历版本的 jieba 分词, 复杂度相对很大, 为 O(2^n)

    # 构建DAG, 复杂度O(n^2)
    n=len(s)
    edges=[[] for _ in range(n)]
    for i in range(n):
        edges[i].append(i+1)
        for j in range(i+2, n+1):
            sub_str=s[i:j]
            if sub_str in wd:
                edges[i].append(j)

    # 构造所有路径, 复杂度 O(2^n)
    paths=[]
    def dfs(u:int, path:list[int]):
        if u==n:
            paths.append(path.copy())
            return
        for v in edges[u]:
            path.append(v)
            dfs(v, path)
            path.pop()

    dfs(0, [0])

    # 得分统计+选出最有可能的分词方式, 涉及到了排序, 复杂度 O(nlog n)
    def get_score_log(path):
        ans=0
        for id1, id2 in zip(path, path[1:]):
            ans+=math.log(wd[s[id1:id2]]) 
            # wd统计出来s[id1, id2]的得分(概率之积再取对数)
        return ans
    paths.sort(key=lambda x: get_score_log(x), reverse=True)

    # 返回分词结果, 复杂度O(n)
    best_path=paths[0]
    split_words=[]
    for id1, id2 in zip(best_path, best_path[1:]):
        split_words.append(s[id1:id2])
    return split_words

    # 综上, 该算法各部分中复杂度取最大值, 总复杂度 O(2^n), 难以接受


def standard_jieba_word_segmentation(s:str, wd:dict):

    # 此为动态规划遍历版本的 jieba 分词, 复杂度相对较小, 仅为 O(n^2)
    # wd: word_dict, wd 中各个词典的频率, wd[word]=p, 值为概率.
    # 假设 word_dict 中收录了所有的单字, 让每个 s[i:i+1](也就是 s[i])都可以在字典中找到

    # 构建DAG, 复杂度O(n^2), n 是字符串长度
    n=len(s)
    edges=[[] for _ in range(n)]
    for i in range(n):
        edges[i].append(i+1)
        for j in range(i+2, n+1):
            sub_str=s[i:j] 
            # 这里的切片, 是对原有字符串的复制, 可能导致复杂度进一步提升
            if sub_str in wd:
                edges[i].append(j)

    # 直接使用动态规划, 算出所有路径中概率/分数最大的那一条
    dp=[0.0 for _ in range(n+1)]
    split=[-1 for _ in range(n+1)]
    # dp[i]: 从下标 i 开始, 以下标 n 结尾的所有路径中的得分最大值
    # dp[i]=max_j^{s[i:j]得分+dp[j]}
    # split[i]=j0: j0 就是让上式取到 max 值的 j, 也就是分词处

    split[n]=n
    for i in range(n-1, -1, -1):
        max_score=-float('inf')
        for j in edges[i]:
            score=math.log(wd[s[i:j]])+dp[j]
            if score>max_score:
                max_score=score
                split[i]=j
        '''
        如果人为限制候选词的最大长度为 L，则每个位置最多检查 L 个后继位置。
        此时，在忽略字符串切片和词典查询的具体成本时，DAG 构建和 DP 的时间复杂度均为 O(n * L)。
        '''
        dp[i]=max_score

    split_words=[]
    i=0
    while i<n:
        word=s[i:split[i]]
        split_words.append(word)
        i=split[i]
    return split_words
                     

if __name__ == "__main__":
    word_dict1 = {
        "我":0.01,
        "爱":0.01,
        "生":0.001,
        "活":0.001,
        "我爱":0.005,
        "生活":0.02
    }
    sentence1 = "我爱生活"
    split_words1= my_jieba_word_segmentation(sentence1, word_dict1)
    split_words1= standard_jieba_word_segmentation(sentence1, word_dict1)
    print(split_words1)

    word_dict2 = {
        "研": 0.001,
        "究": 0.001,
        "研究生": 0.008,
        "命":0.001,
        "研究":0.01,
        "生":0.001,
        "生命":0.01,
        "起源":0.01,
        "起":0.001,
        "源":0.001
    }
    sentence2 = "研究生命起源"
    split_words2= my_jieba_word_segmentation(sentence2, word_dict2)
    split_words2= standard_jieba_word_segmentation(sentence2, word_dict2)
    print(split_words2)