a = [0] * 3
b = [1] * 5
c = [2] * 8

a_i = iter(a)
b_i = iter(b)
c_i = iter(c)

while True:
    try:
        print(next(a_i))
        print(next(b_i))
        print(next(c_i))
    except StopIteration:
        print("!!!")
        break
