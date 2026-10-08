def squares():
    squares = []

    for n in range(5):
        squares.append(n**2)
    return squares

print(squares())


squares = [n ** 2 for n in range(5)]
print(squares)
#[expression for item in iterable]

def evens():
    evens = []

    for n in range(10):
        if n % 2 == 0:
            evens.append(n)
            
    return evens

print(evens())

# [expression for item in iterable if condition]

def labels():
    labels = []

    for n in range(5):
        if n % 2 == 0:
            labels.append("even")
        else:
            labels.append("odd")
    return labels
print(labels())

labels = ["even" if n % 2 == 0 else "odd" for n in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']


# Dictionary comprehension

def squares_dict():
    squares = {}

    for n in range(5):
        squares[n] = n**2
    return squares
print(squares_dict())

# sets comprehesnions
def remainders():
    remainders = set()

    for n in range(10):
        remainders.add(n % 3)
    return remainders
print(remainders())


result = [x * 2 for x in range(6) if x % 2 == 0 ]

words = ["cat", "elephant", "dog", "giraffe"]

def classify_words_length(words):
    result = {}

    for word in words:
        if len(word) > 4:
            result[word] = True
        else:
            result[word] = False
    return result
print(classify_words_length(words))


words = ["cat", "elephant", "dog", "giraffe"]
Answer = { word: True if len(word) > 4 else False for word in words}
print(Answer)