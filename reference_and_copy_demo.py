'''
    一个示例代码, 展示了引用(reference)赋值, 浅拷贝(shallow copy), 深拷贝(deep copy)的差别.
    里面还涉及到了关于可变对象/不可变对象, 即可变性(variability)的讨论与讲解.
'''

my_list=[1, 2, 3, 4, [2, 3, 4]]
print('my_list', my_list)
_list=my_list
_list.append(5)
print('_list', _list)
print('my_list', my_list)
'''
    以上: 通过引用赋值修改_set, 修改也同时作用到了 my_list 上.
    这是因为, 引用赋值'a=b'这种语句生成了 b 的同一个指针 a.
    如果b的类型是可变对象, 那么对 a 的修改会同步到 b 上.
    python 中, 列表, 字典, 集合等都是可变对象. 整数, 字符串, 元组不可变.
    tips:
        特殊情况:元组内的可变元素
        如果不可变对象（如元组）内部包含可变子元素，引用赋值后可以修改这个子元素的内容, 但元组本身的结构仍不可改
        
        # 元组（不可变）内嵌套列表（可变）
        original = (1, [2, 3])
        new_var = original

        # 修改元组内的可变子元素
        new_var[1].append(4)  

        # 原元组的子元素内容变了（但元组的结构/长度仍不可改）
        print(original)  # (1, [2, 3, 4])
'''


'''
如果想通过引用赋值修改元变量, 那需要保证原变量的类型是可变对象.
下面的例子中, 整数 a 类型 int 不是可变对象, 因此没法通过修改_b 来修改 a.
'''
print('\n')
a=5
print('a', a)
_b=a
_b=10
print('a', a)
print('_b', _b)

print('\n')
test=my_list.copy()
test[4]=[10]
print('test', test)
print('my_list', my_list)

test[4].append(5)
print('test', test)
print('my_list', my_list)
'''
    以上: 验证浅拷贝.
    test 是 my_list 的浅拷贝.
    浅拷贝(list.copy())的核心特性是只拷贝列表 “第一层结构”，嵌套的可变元素仍共享引用.

    情况 1: test[4] = [10] → my_list 不变
    这是修改新列表的 “第一层结构”，而非修改嵌套元素本身：
    test[4] = [10] 的本质：给新列表 test 的第 5 个位置重新赋值，让它指向一个全新的列表 [10];
    浅拷贝的新列表 test 第一层是独立于 my_list 的，因此这个赋值只影响 test, 不影响原列表 my_list 的第一层(my_list[4] 仍指向原来的 [2,3,4])
    
    但是, 浅拷贝中, 更深层次的结构仍是和原变量共享的. 修改拷贝后变量更深层的内容, 修改会同步到原变量上.

    test[4].append(5) → my_list 同步变化
    这是修改嵌套的可变元素本身，而非修改新列表的第一层：
    test[4] 指向的是原列表 my_list[4] 共享的那个嵌套列表 [2,3,4](浅拷贝只拷贝第一层，嵌套元素仍共享引用);
    append(5) 是对这个嵌套列表的「原地修改」(可变对象的特性), 因此所有指向它的引用(my_list[4]、test[4])都会感知到变化。

    
'''

import copy
'''
但是, 如果是用深拷贝:(见下面的例子)
这里重新创建一个 my_list_restore, 是为了防止上面代码影响 my_list, 造成例子上的混乱
无论如何, 都不会修改 my_list_restore.
深拷贝能让拷贝前后的两个变量完全独立, 彻底隔离修改, 永不同步.
'''
print('\n')
my_list_restore=[1, 2, 3, 4, [2, 3, 4]]
test_deepcopy=copy.deepcopy(my_list_restore) # deepcopy需要调库
test_deepcopy[4]=[10]
print('test_deepcopy', test_deepcopy)
print('my_list_restore', my_list_restore)

test_deepcopy[4].append(5)
print('test_deepcopy', test_deepcopy)
print('my_list_restore', my_list_restore)

