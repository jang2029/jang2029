import random

l = [0, 1, 2, 3, 4]
dig = (random.choices(l, k=32))
print (dig)

result = ''.join(str(st) for st in dig )

print (result)

print (''.join(str(st) for st in dig ))