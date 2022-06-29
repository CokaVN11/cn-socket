from sys import getsizeof

a:tuple
a = (1, "Lake Place", "Choose me", 1)
for i in a:
    print(getsizeof(i))
print(getsizeof(a))