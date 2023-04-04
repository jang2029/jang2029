s1 = [1, 2, 3, 4, 5, 6]
s2 = [4, 5, 6, 7, 8, 9]




print (list(set(s1) | set(s2)))
print (list(set(s1) & set(s2)))
print (set(s1) - set(s2))
print (tuple(set(s1) - set(s2)))
print (list(set(s1) - set(s2)))



