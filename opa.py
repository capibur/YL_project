def g(i):
    while True:
        yield i
for i in range(8):
    print(g(i))