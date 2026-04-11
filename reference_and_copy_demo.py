'''
    一个示例代码, 展示了引用(reference)赋值, 浅拷贝(shallow copy), 深拷贝(deep copy)的差别.
    里面还涉及到了关于可变对象/不可变对象, 即可变性(variability)的讨论与讲解.

    关注赋值, 浅拷贝, 深拷贝在内存图上的变化

    赋值(test=my_list)操作:
        实际是给 my_list 起了一个别名 test
    浅拷贝(test=my_list.copy):
        是让 my_list 和 test 中每个元素都指向相同的对应的对象
    深拷贝(test_deepcopy=copy.deepcopy(my_list_restore)):
        直接生成了和 test 完全一样的 my_list, 但二者的每个元素虽然数值相同, 但指向的是完全不同的东西.
        但对于不可变对象（比如数字 1、字符串 "hello"、元组），深拷贝通常并不会真的去克隆它，而是依然让大家指向同一个。
        为什么？ 因为不可变对象反正是改不了的，克隆一份纯属浪费内存。所以深拷贝是“按需克隆”。


    如果你以后在写代码时拿不准，只需要用下面这行代码“照妖镜”：
    print(id(a) == id(b))
    如果返回 True：说明它们是同一个对象（赋值），改一个必动另一个。

    如果返回 False：说明它们是不同对象（拷贝）。此时再看操作：
        a[0] = x：改第一层，互不影响。
        a[0].append(x)：改深层，看是深拷贝还是浅拷贝
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

    内存图如下所示
    my_list ────────┐
                    │
                    ▼
                [ 索引0: 1, 索引1: 2, 索引2: 3, 索引3: 4, 索引4: ● ,  索引5: 5]
                    ▲                                         │
                    │                                         ▼
    test ───────────┘                                     [2, 3, 4]

    关键点:
    只有一个“大篮子”：内存中只存在一个外层列表对象。
    两个标签：my_list 和 test 就像两个遥控器，按的是同一台电视机。
    
    
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
print('当前的 my_list:', my_list, '\n')
test=my_list.copy()
test[4].append(5)
print('修改后的test', test)
print('修改 test后, 此时的my_list', my_list)
'''
浅拷贝中, 更深层次的结构仍是和原变量共享的. 修改拷贝后变量更深层的内容, 修改会同步到原变量上.
浅拷贝(list.copy())的核心特性是只拷贝列表 “第一层结构”，嵌套的可变元素仍共享引用.

浅拷贝的新列表 test 第一层是独立于 my_list 的，因此这个赋值只影响 test, 不影响原列表 my_list 的第一层(my_list[4] 仍指向原来的 [2,3,4])

执行浅拷贝后:
my_list ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
               │      │      │      │      │
               ▼      ▼      ▼      ▼      ▼
             (1)    (2)    (3)    (4)   [2, 3, 4] <── 嵌套列表对象A
               ▲      ▲      ▲      ▲      ▲
               │      │      │      │      │
test    ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
my_list[4] 和 test[4] 都指向同一个列表对象A [2, 3, 4]

test[4].append(5) → my_list 同步变化
    这是修改嵌套的可变元素本身，而非修改新列表的第一层：
    test[4] 指向的是原列表 my_list[4] 共享的那个嵌套列表 [2,3,4](浅拷贝只拷贝第一层，嵌套元素仍共享引用);
    append(5) 是对这个嵌套列表的「原地修改」(可变对象的特性), 因此所有指向它的引用(my_list[4]、test[4])都会感知到变化。

    内存图如下:
    my_list ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
                    │      │      │      │      │
                    ▼      ▼      ▼      ▼      ▼
                   (1)    (2)    (3)    (4)   [2, 3, 4, 5] <── 嵌套列表对象A (被修改了)
                    ▲      ▲      ▲      ▲      ▲
                    │      │      │      │      │
        test   ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]

如果先执行了下面的 test[4]=[10], 由于此时 test[4] 和 my_list[4]指向不同的对象(见下图), 此时若再执行 test[4].append(5), 则不会同步修改 my_list[5]
'''

test[4]=[10]
print('\ntest', test)
print('my_list', my_list)
'''
执行 test[4] = [10] 后:
my_list ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
               │      │      │      │      │
               ▼      ▼      ▼      ▼      ▼
             (1)    (2)    (3)    (4)   [2, 3, 4, 5] (对象A)
               ▲      ▲      ▲      ▲
               │      │      │      │
test    ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
                                           │
                                           ▼
                                         [ 10 ]      (对象B)
赋值操作('=') 改变的是「指向关系」，而不是修改对象本身.
'''

test[0]=99
print('\ntest', test)
print('my_list', my_list)
'''
这里改变了test[0]指向的东西, 由 1 改成了 99
test[0] = 99：这是一个赋值操作（Rebinding）。
把 test 索引 0 的那个“钩子”，从数字 1 上拔下来，挂到了数字 99 上。
关键点：你并没有改变数字 1 本身（数字在 Python 中是不可变的），你只是换了钩子的指向。

对于 test[4].append(5)：这是一个原地修改（Mutating）
并没有拔掉 test[4] 的钩子，而是顺着钩子找到了那个“列表房间”，进去往里面塞了一个 5。
因为 my_list[4] 也挂在这个房间的门上，所以它也看到了变化。
'''



# 切片赋值
ac = [1, 2, [3, 4, 5]]
bd = [9, 8, 7, 22]

ac[2:] = bd
'''
发生了什么？
ac 还是原来的 ac，地址不变
bd 还是原来的 bd
系统临时创建一个 bd 的切片副本（浅拷贝）
把副本里的元素 逐个塞进 ac[2], ac[3], ac[4]

始终不改变 bd
'''




import copy
'''
但是, 如果是用深拷贝:(见下面的例子)
这里重新创建一个 my_list_restore, 是为了防止上面代码影响 my_list, 造成例子上的混乱
无论如何, 都不会修改 my_list_restore.
深拷贝能让拷贝前后的两个变量完全独立, 彻底隔离修改, 永不同步.

执行深拷贝test_deepcopy=copy.deepcopy(my_list_restore) 后, 内存关系如下所示:
my_list_restore (对象1) ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
                              │      │      │      │      │
                              ▼      ▼      ▼      ▼      ▼
                            [ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 2, 3, 4 ] (嵌套列表A)


test_deepcopy   (对象2) ──→ [ 索引0, 索引1, 索引2, 索引3, 索引4 ]
                              │      │      │      │      │
                              ▼      ▼      ▼      ▼      ▼
                            [ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 2, 3, 4 ] (嵌套列表B)

可以验证, id(test_deepcopy[4])!=id(my_list_restore[4]), 二者完全不同
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



# 以下是一些额外增加的内容:
# 在 Python 中：当执行 func(a) 时，相当于函数内部有一个局部变量 nums，执行了 nums = a。
# 此时，nums 和 a 是两个指向同一个内存地址的独立指针

def try_to_change_by_assignment(nums):
    # 逻辑：我不要原来的钥匙了，我重新创建一个新列表并把钥匙给 nums
    nums = [99, 100] 

a = [1, 2]
try_to_change_by_assignment(a)
print(a)  # 结果：[1, 2] —— 没变！
'''
这里面的执行顺序相当于:
a = [1, 2]
nums=a,
nums = [99, 100] 
那么 nums 最开始和a指向同一个地址, 但后面 nums指向了[99, 100], 和 a 解耦了, 因此二者不一样了
'''

def try_to_change_by_mutation(nums):
    # 逻辑：我拿着传进来的钥匙，进屋加了个家具
    nums.append(3)

a = [1, 2]
try_to_change_by_mutation(a)
print(a)  # 结果：[1, 2, 3] —— 变了！
'''
这里面的执行顺序相当于:
a = [1, 2]
nums=a,
nums.append(3)
那么 nums和a指向同一个地址, 操作也就是同步的
'''
