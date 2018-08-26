from itertools import islice
def fib():
    
    cur = 0
    prev = 1
    
    while True:
        yield cur
        prev, cur = cur, cur + prev

f = fib()
a = list(islice(f, 0, 10))
print (a)



