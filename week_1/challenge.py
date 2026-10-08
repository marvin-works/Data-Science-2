def inventory_system(item, goods=[]):
    goods.append(item)
    return goods
print(inventory_system('spoon', 'pots', 'plates'))
print(inventory_system("dish"))


def add_item(item, target=[]):
    target.append(item)
    return target

print(add_item(1)) = [1]
print(add_item(2)) = [1, 2]


def is_same_object(a, b):
    if a is b:
        return True
    else:
        return False
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(is_same_object(list_a, list_b))  # expect: False
print(is_same_object(list_a, list_c))  # expect: True


# x = 5

# def change():
#     global x
#     x = 10   
#     print(x)  
# print(x)

def remove_duplicates_keep_order(items):
    result = []
    seen = set()

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


print(remove_duplicates_keep_order([3, 1, 3, 2, 1, 4]))

