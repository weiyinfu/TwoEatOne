import os

cnt = 100
with open("998-整理.txt", encoding='utf8') as f:
    for i in f.readlines():
        i = i.strip()
        if not i: continue
        oldname = i
        newname = "%d%s" % (cnt, i[i.index("-"):])
        cnt += 1
        os.rename(oldname, newname)
