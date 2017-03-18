import os

file1 = open('main.txt', 'r').read()
file2 = open('main_diff.txt', 'r').read()

os.system("diff -u main.txt main_diff.txt > new.diff")
os.system("patch main.txt new.diff")