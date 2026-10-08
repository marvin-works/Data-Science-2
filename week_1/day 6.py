# try:
#     value = int(input("Enter a number: "))
#     result = 10 / value
# except ValueError:
#     print("That wasn't a valid number")
# except ZeroDivisionError:
#     print("Can't divide by zero")

# try:
#     value = int("42")
# except ValueError:
#     print("bad input")
# else:
#     print("this runs only if no exception happened:", value)
# finally:
#     print("this always runs, exception or not — used for cleanup")



# def withdraw(balance, amount):
#     if amount > balance:
#         raise ValueError("Insufficient funds")
#     return balance - amount
# print(withdraw(balance=20,amount=4))

# try:
#     x = int("abc")
# except ValueError:
#     print("caught it")
# finally:
#     print("cleanup")

# # Q4
# def check_age(age):
#     if age < 0:
#         raise ValueError("Age cannot be negative")
#     return age

# try:
#     check_age(-5)
# except ValueError as e:
#     print(f"Error: {e}")

# # Q1
# try:
#     x = int("abc")
# except ValueError:
#     print("caught it")
# finally:
#     print("cleanup")

# # Q2
# try:
#     result = [1, 2, 3][10]
# except IndexError:
#     print("out of range")
# except ValueError:
#     print("bad value")

# # Q4
# def check_age(age):
#     if age < 0:
#         raise ValueError("Age cannot be negative")
#     return age

# try:
#     check_age(-5)
# except ValueError as e:
#     print(f"Error: {e}")

# # Q5 — trace this carefully, order matters
# try:
#     print("A")
#     x = 1 / 0
#     print("B")
# except ZeroDivisionError:
#     print("C")
# else:
#     print("D")
# finally:
#     print("E")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    except TypeError:
        return None
    finally:
        print("Attempted division")

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide(10, "a"))

def weird():
    try:
        return 1
    finally:
        return 2

print(weird())

try:
    number = input("Enter a number: ")
    print(1/number)
except ZeroDivisionError:
    print("Division by zero not possible")
except ValueError:
    print("ValueError not possible")
except Exception:
    print("Exception not possible")
finally:
    print("Finally finished")
