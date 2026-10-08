# def add_item(item, total=[]):
#     total.append(item)
#     return total
# print(add_item(1))
# print(add_item(2))
# print(add_item(3))

# list_A = 5
# list_B = 5
# list_C = list_A

# print(list_A == list_B)
# print(list_A is list_B)
# print(list_A == list_C)
# print(list_A is list_C)
# print(list_B == list_C)
# print(list_B is list_C)

# def same_ref(a, b):
#     if a is b:
#         return True
#     else:
#         return False
# print(same_ref("x", "x"))

# x = 300
# y = 300
# print(x is y)


# def add_tag(item, target=None):
#     if target is None:
#         target = []

#     target.append(item)
#     return target
# log1 = add_tag("urgent")
# log2 = add_tag("todo")
# print(log2)
    

# for i in range(5):
#     if i == 3:
#         break
#     print(i)

def first_multipe_of(nums, divisor):
    for n in nums:
        if n % divisor == 0:
            return n
            break
    else:
        return None
print(first_multipe_of([1, 3, 5, 8, 10], 2))

for i in range(4):
    if i == 2:
        break
    print(i)
# 0, 1

for i in range(4):
    if i == 2:
        continue
    print(i)
# 0, 1, 3

for n in [1, 3, 5]:
    if n % 2 == 0:
        print("found even")
        break
else:
    print("no evens found")
# no evens found