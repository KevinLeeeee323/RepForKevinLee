my_list=[1, 2, 3, 4, [2, 3, 4]]

print('当前的 my_list:', my_list)
test=my_list
test[4]=[10]
# test[4].append(5)
# print(id(test[4]), id(my_list[4]))
print('test', test)
print('my_list', my_list)

# test[4].append(5)
# print('test', test)
# print('my_list', my_list)

