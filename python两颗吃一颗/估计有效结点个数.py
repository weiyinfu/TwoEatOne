def c(n, m):
    s = 1
    j = 1
    while j <= m:
        s = s * (n + 1 - j) / j
        j += 1
    return int(s)


def sum():
    s = 0
    for i in range(1, 4):
        for j in range(1, 4):
            s += c(16, i + j) * c(i + j, i)
    return s


print(sum())
