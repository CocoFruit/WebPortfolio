out = []
while 1:
    clr = input()
    if clr[0] == "#":
        continue
    elif clr == "STOP":
        break
    else:
        out.append(clr)


for i in range(len(out)-1):
    print(f'<h1 style="background:linear-gradient({out[i]},{out[i+1]});">{out[i]}</h1>')