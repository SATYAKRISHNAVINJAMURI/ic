import os

filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
for f in filelist:
    os.remove(f)