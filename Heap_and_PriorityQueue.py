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


'''
    为什么实际上, heapq或者 PriorityQueue 都可以接受一个元组作为输入?

    Python 中元组的比较是按元素顺序依次比较，直到找到第一个不同的元素:
    先比较元组第 0 位元素，若相等则比较第 1 位，以此类推;只有所有元素都相等，元组才相等。

    # 元组比较示例
    print((1, "任务A") < (2, "任务B"))  # True（第0位1<2）
    print((2, "任务C") < (2, "任务B"))  # False（第0位相等，第1位"C">"B"）
    print((3, 1, "a") < (3, 2, "b"))   # True（第0位相等，第1位1<2）

    
    因此, 可以像下面这样, 把元组作为输出(但要保证元组的第一个元素是一个数值, 表明优先级, 这样才符合优先队列的优先之含义)
    注意, PriorityQueue 底层基于 heapq 的小顶堆编写, 因此但要保证元组的第一个元素数值越小, 排序越靠前
    from queue import PriorityQueue
    pq = PriorityQueue()
    # 入队 tuple：(优先级, 任务内容)
    pq.put((2, "普通任务"))
    pq.put((1, "紧急任务"))
    pq.put((1, "更紧急任务"))  # 优先级相同，比较第二个元素

    # 出队结果：按元组规则排序
    while not pq.empty():
        print(pq.get())
    # 输出：
    # (1, '更紧急任务') （第0位相等，第1位"更紧急任务"<"紧急任务"）
    # (1, '紧急任务')
    # (2, '普通任务')

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

    '''
    为什么 PriorityQueue 中的方法是_get, 但是上面代码中调用的, 是 get()方法?
    _get/_put 是 PriorityQueue 内部的 “私有方法”（下划线开头）,
    而 get()/put() 是对外暴露的 “公有接口”
    PriorityQueue 的父类 Queue 中:
        def get(self, block=True, timeout=None):
            ...

            item=self._get()
            self.not_full.notify()
            return item
    get 方法会继承给 PriorityQueue.
    PriorityQueue 并没有重写这个 get 方法, 因此仍然同 Queue 中的 get 方法.
    在 PriorityQueue 调用get方法时, 内部_get 会是 PriorityQueue 自己的_get方法.
    (虽然 Queue 中也有_get 方法, 但是被PriorityQueue子类的_get方法所重写了)
    '''

    return sorted_iter

    
if __name__=='__main__':
    iter=[9, 8, 7, 5, 23, 1]
    print('before sort', iter)
    print('sort with heapq version heap_sort:', heap_sort_heapq(iter))
    print('sort with PriorityQueue version heap_sort:', heap_sort_prique(iter))
