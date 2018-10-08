s = '1111000000002222'
ss = 0
pow = 1
for i in s:
    if i == '1':
        ss += pow
    elif i == '2':
        ss += pow + pow
    pow *= 3
print(ss)
