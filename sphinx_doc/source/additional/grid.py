def hori(c,s):
    for i in range(c):
        print('+', end = '')
        for j in range(s):
            print('-', end ='')
    print('+')
    
def verti(c,s):
    for i in range(c):
        print('|', end = '')
        for j in range(s):
            print(' ',end = '')
    print('|')

def grid(r,c,s):
    for i in range(r):
        hori(c,s)
        for j in range(s):
            verti(c,s)
    hori(c,s)

grid(5,6,5)