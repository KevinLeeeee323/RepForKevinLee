import heapq
from queue import PriorityQueue
from queue import Empty
from typing import Iterable

def heap_sort_heapq(iter)->list:
    '''
    # 基于heapq实现的堆排序. 
    # 参数: 一个可迭代对象
    # 返回值: 排序后的可迭代对象

    这里的 heap 是小顶堆.
    https://docs.python.org/zh-cn/3.14/library/heapq.html 
    常用函数:
    heapq.heapify(x)
        将列表 x 转换为最小堆，在线性时间内原地修改。

    heapq.heappush(heap, item)
        将值 item 推至 heap 中，保持最小堆的不变性。

    heapq.heappop(heap)
        从 heap 弹出并返回最小的项，保持最小堆的不变性。 
        如果堆为空，则会引发 IndexError。 
        要访问最小的项而不弹出它，可以使用 heap[0]。
    
    AI tips: PriorityQueue 是线程安全的, 而 heapq 非线程安全.
    
    基于以上, 可以写出 heap_sort 的代码:
    '''
    
    h=[]
    for value in iter:
        heapq.heappush(h, value) # 逐步添加元素时, 始终保持小顶堆

    sorted_iter=[]
    for cnt in range(len(h)):
        sorted_iter.append(heapq.heappop(h))
    return sorted_iter

    '''
    以上四行一个更简单的写法:
    return [heapq.heappop(h) for i in range(len(h))]
    '''
    
def heap_sort_prique(iter:Iterable)->list:
    
    '''
    基于 queue.PriorityQueue 实现的堆排序. 
    参数 iter: 一个可迭代对象
    返回值 sorted_iter: 排序后的可迭代对象

    以下内容来自 queue.py, 其中的 PriorityQueue类的 get, put 底层是通过 heapq 的函数实现的
    所以实际上基于 heapq 和 PriorityQueue 实现的这两种堆排序, 在单线程模式下没什么区别
    class PriorityQueue(Queue):
        def _init(self, maxsize):
            self.queue = []

        def _qsize(self):
            return len(self.queue)

        def _put(self, item):
            heappush(self.queue, item)

        def _get(self):
            return heappop(self.queue)
    '''

    prique=PriorityQueue()
    for item in iter:
        prique.put(item)

    sorted_iter=[]
    while True:
        try:
            sorted_iter.append(prique.get(block=False))
        except Empty:
            break
    # 多线程场景下可能因 “判空后队列被其他线程取空” 导致阻塞.
    #  try-except (AI 的修改): 兼容多线程.

    return sorted_iter

    
if __name__=='__main__':
    iter=[9, 8, 7, 5, 23, 1]
    print('before sort', iter)
    print('sort with heapq version heap_sort:', heap_sort_heapq(iter))
    print('sort with PriorityQueue version heap_sort:', heap_sort_prique(iter))
    



    

