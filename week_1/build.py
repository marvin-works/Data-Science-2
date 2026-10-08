# def running_total():
#     counter = 0

#     def make_counter(number):
#         nonlocal counter
#         counter += number
#         return counter
#     return make_counter

# counter = running_total()
# print(counter(5))   # 5
# print(counter(3))   # 8
# print(counter(10))  # 18



def remove_duplicates_keep_order(items):
    result = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


print(remove_duplicates_keep_order([3, 1, 3, 2, 1, 4]))

def remove_duplicates_keep_order(items):
    result = []
    seen = set()

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


print(remove_duplicates_keep_order([3, 1, 3, 2, 1, 4]))