import os
import re

with open("998-整理.txt", "w", encoding='utf8') as f:
    for i in os.listdir():
        if re.match("\d{2,}.*\.py", i):
            if int(re.search("\d+", i).group()) > 900:
                continue
            f.write(i + "\n")
