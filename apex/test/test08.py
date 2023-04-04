
def print_vector(x,y,z):
    print(f"<{x} , {y} , {z}>")


tuple_vexc = ('a','b','c')
print_vector(*tuple_vexc)

list_vec =['e','f','z']
print_vector(*list_vec)

print([a for a in list_vec])

print(''.join( str(i) for i in list_vec ))