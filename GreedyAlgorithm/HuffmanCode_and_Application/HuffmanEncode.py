import heapq
from typing import Optional
'''
Node 类的 __init__ 方法参数注解中，直接使用 left:Node|None 类型时，
这个类还没完成完整定义（Python 解析代码是从上到下的），导致解释器不认识 Node, 会报错

可以通过导入 typing 模块的 Optional 并且写成下面那样来解决这个问题
其中, Optional[T] 等价于 T|None, T 代表一个类的名字
'''


'''
[实现内容]
    通过 python 实现的构造 Huffman 树.
    由于很多内容是调库, 所以没几行代码就写完了.
    最终返回一个所有存储字符对应的Huffman 编码的字典 huffman_dict

[复杂度分析]
    假设一共有 n 个需要生成 Huffman 编码的结点, 则构建的 Huffman 树中实际有 2*n-1 个结点.

    1. 时间复杂度分析：
    - 构建树：n个叶子节点，需合并n-1次，每次堆操作O(logk)（k为当前堆大小，最大2n-1），总复杂度O(nlogn)；
    - 生成编码：遍历2n-1个节点，复杂度O(n)；
    - 整体复杂度：O(nlogn)（由堆操作主导）。
    2. 空间复杂度：O(n)（存储n个叶子节点+堆空间+编码字典）。
'''

class Node:
    def __init__(self, char:str|None, freq:float, left:Optional['Node'], right:Optional['Node']) -> None:
        self.char=char
        self.freq=freq
        self.left=left
        self.right=right

    def __lt__(self, other:Optional['Node']):
        return self.freq < other.freq
    
    '''
    heapq 只能对可比较的类型（如数字、元组）排序，而自定义类默认没有比较规则.
    如果没有上面的__lt__方法, 则 heapq 在 push, pop 时不知道依据什么维护/构建最小堆. 
    换而言之, 没有确定"最小"到底是是什么最小?

    解决方法:
    重写 __lt__（小于）方法，定义 Node 实例的比较规则（按 freq 从小到大），这样 heapq 就能正确排序
    '''

def build_huffman_tree(char_list:list[tuple[float, str]]):
    # char_list[i]=(freq, char) # 频率, 字符. 字符可以是None, 频率 \in [0, 1]

    # 通过维护最小堆, 构建 Huffman 树, 每次取频率最小的两个节点合并
    if not char_list:
        return None
    lower_bound_heap=[] # 最小堆
    for freq, char in char_list:
        heapq.heappush(lower_bound_heap, Node(char, freq, None, None))

    while len(lower_bound_heap)>=2:
        v1=heapq.heappop(lower_bound_heap)
        v2=heapq.heappop(lower_bound_heap)
        merged=Node(char=None, freq=v1.freq+v2.freq, left=v1, right=v2)
        heapq.heappush(lower_bound_heap, merged)

    return heapq.heappop(lower_bound_heap)


def gen_huffman_code(root:Optional[Node], huffman_code:str, huffman_dict:dict):
    if root is not None:
        # 这里选择了前序遍历, 但实际上前序/中序/后序/按层次遍历Huffman树不影响最终生成的Huffman编码
        if root.left==None and root.right==None:
            #print(f'\'{root.char}\', {root.freq:.2}, {huffman_code}')
            huffman_dict[root.char]=huffman_code
        gen_huffman_code(root.left, huffman_code+'0', huffman_dict)
        gen_huffman_code(root.right, huffman_code+'1', huffman_dict)


if __name__ == '__main__':

    # 字符频率列表：(频率, 字符)
    char_freq = [(0.45, 'a'), (0.13, 'b'), (0.12, 'c'), (0.16, 'd'), (0.09, 'e'), (0.05, 'f')]
    
    # 构建哈夫曼树
    root = build_huffman_tree(char_freq)
    huffman_dict=dict()
    gen_huffman_code(root, '', huffman_dict)
    print(huffman_dict)