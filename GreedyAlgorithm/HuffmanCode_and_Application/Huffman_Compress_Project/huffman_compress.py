import heapq
from typing import Optional
import json
import os
from tqdm import tqdm

class Node:
    '''
    构成 Huffman 树的结点
    '''
    def __init__(self, char:str|None, freq:float, left:Optional['Node'], right:Optional['Node']) -> None:
        self.char=char
        self.freq=freq
        self.left=left
        self.right=right

    def __lt__(self, other):
        return self.freq < other.freq
    '''
    重写 __lt__(小于)方法，定义 Node 实例的比较规则(按 freq 从小到大)，这样 heapq 就能正确排序
    '''

def build_huffman_tree(char_list:list[tuple[float, str]]):
    '''
    通过维护最小堆, 构建 Huffman 树, 每次取频率最小的两个节点合并
    char_list: (freq, char)元组对组成的列表, 存储 char 及其频率 freq
    '''
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
        if root.left==None and root.right==None:
            #print(f'\'{root.char}\', {root.freq:.2}, {huffman_code}')
            huffman_dict[root.char]=huffman_code
        gen_huffman_code(root.left, huffman_code+'0', huffman_dict)
        gen_huffman_code(root.right, huffman_code+'1', huffman_dict)


def get_char_freq(file_dir: str) -> list[tuple[float, str]]:
    """
    统计文本文件中每个字符的频率
    file_dir: 待压缩文本文件路径(.txt)
    返回[(频率, 字符)] 
    """
    # 读取文本文件
    try:
        with open(file_dir, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error. {file_dir} Not Found")
        return []
    except Exception as e:
        print(f"Fail to Read File{e}")
        return []

    # 统计每个字符的出现次数
    char_count = {}
    total_chars = len(text)
    if total_chars == 0:
        print("错误：文件为空")
        return []

    for char in text:
        char_count[char] = char_count.get(char, 0) + 1

    # 计算频率, 生成 (频率, 字符) 元组列表
    char_freq_list = []
    for char, count in char_count.items():
        freq = count / total_chars
        char_freq_list.append((freq, char))

    return char_freq_list


def gen_output(input_text_path: str, huffman_dict: dict, output_path: str, output_dict_path: str):
    """
    生成 Huffman 编码后的二进制文件，并保存编码字典(用于解压)

    input_text_path: 原始文本文件路径
    huffman_dict: 字符->Huffman编码的字典
    output_path: 编码后的文件路径
    output_dict_path: 编码字典保存路径(.json)
    """

    # 读取原始文本
    with open(input_text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 将文本转换为二进制编码字符串
    binary_str = '' # 最终输出的文本(只是 01 串)
    for char in tqdm(text):
        binary_str += huffman_dict[char]  # 每个字符替换为对应的编码写入输出文件

    # 保存编码字典
    with open(output_dict_path, 'w', encoding='utf-8') as f:
        json.dump(huffman_dict, f, ensure_ascii=False, indent=2)

    # 二进制字符串转为字节(8位一组)，不足补0，记录补0的位数
    padding_bits = (8 - len(binary_str) % 8) % 8  # 计算需要补的0的位数
    binary_str += '0' * padding_bits

    # 按8位分割，转成字节
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        byte_array.append(int(byte, 2))

    # 保存二进制文件(开头写入补0的位数，用于解压时还原)
    with open(output_path, 'wb') as f:
        f.write(padding_bits.to_bytes(1, byteorder='big'))  # 第1字节记录补0位数
        f.write(byte_array)

    print(f"压缩完成！")
    print(f"原始文件大小：{os.path.getsize(input_text_path)} 字节")
    print(f"编码后二进制文件大小：{os.path.getsize(output_path)} 字节")
    print(f"编码字典保存路径：{output_dict_path}")


if __name__ == '__main__':

    INPUT_TXT_PATH = "Pride_and_Prejudice.txt"  # 待压缩文本
    OUTPUT_PATH = "text.huff"  # 压缩后的文件
    OUTPUT_DICT_PATH = "huffman_dict.json"  # 编码字典

    # 统计字符频率
    char_freq = get_char_freq(INPUT_TXT_PATH)
    if not char_freq:
        exit(1)

    # 构建哈夫曼树
    root = build_huffman_tree(char_freq)
    huffman_dict = dict()
    gen_huffman_code(root, '', huffman_dict)
    print("Gen Huffman Encoding Dict:")
    print(huffman_dict)

    # 计算平均编码长度
    avg_length = sum(len(huffman_dict[char]) * freq for freq, char in char_freq)
    print(f"平均编码长度：{avg_length:.2f} 位/字符")

    # 生成压缩文件
    gen_output(INPUT_TXT_PATH, huffman_dict, OUTPUT_PATH, OUTPUT_DICT_PATH)