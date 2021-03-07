a = [10,20,30,40,50,60,70,80,90,100]
x = int(input())
pos = 0
while pos < len(a) and a[pos] >= x:
    pos += 1
print(pos + 1)
