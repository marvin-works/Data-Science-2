'''class Dog:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

    def bark(self):
        return f"{self.name} still barks at {self.age} years old"

    def bred(self):
        return f"It is a {self.breed} dog"

my_dog = Dog("Tyler", 5, "Gold retriever")
print(my_dog.bred())
print(my_dog.bark())'''

'''class Bad:
    items = []              # class attribute — SHARED across every instance

    def add(self, item):
        self.items.append(item)

a = Bad()
b = Bad()
a.add("x")
print(b.items)   # ['x']  <- b never touched, but sees a's change — same shared list

class Good:
    def __init__(self):
        self.items = []      # instance attribute — separate list per instance

    def add(self, item):
        self.items.append(item)

import random
print(type(random.randint(1, 5)))

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

c1 = Counter()
c2 = Counter()
print(c1.increment())
print(c1.increment())
print(c2.increment())


# Q3 — spot the bug, using tonight's class-attribute trap
class ShoppingCart:
    items = []

    def add_item(self, item):
        self.items.append(item)

cart1 = ShoppingCart()
cart2 = ShoppingCart()
cart1.add_item("apple")
print(cart2.items)


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
            self.items.append(item)
    
cart1 = ShoppingCart()
cart2 = ShoppingCart()
cart1.add_item("apple")
print(cart2.items)

# Q4
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hi, I'm {self.name}"

p = Person("Marv")
print(p.greet())'''

'''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner 
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self,amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        else:
            self.balance -= amount
            print(f"${amount} withdraw successfully")
            return self.balance

acc = BankAccount("Marv", 100)
print(acc.deposit(50))     
print(acc.withdraw(30))    
try:
    print(acc.withdraw(500))
except ValueError as err:
    print(f"Error: {err}")
        
    '''

def add_score(score, scores=[]):
    scores.append(score)
    return scores

print(add_score(90))
print(add_score(85))


for i in range(3):
    if i == 1:
        continue
    print(i)
else:
    print("done")

count = 0
def bump():
    global count
    count += 1
bump()

nums = [3, 1, 2]
x = sorted(nums)
print(nums)
print(x)

result = [n * n for n in range(10) if n % 2 == 1]
print(result)

result = []

for n in range(10):
    if n % 2 == 1:
        result.append(n * n)

print(result)

try:
    d = {"a": 1}
    print(d["b"])
except KeyError:
    print("missing key")
finally:
    print("done")

class Team:
    players = []
    def add(self, name):
        global players
        self.players.append(name)


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        result = self.width * self.height
        return result

my_box = Rectangle(5, 8)
print(my_box.area())