import re

with open("input") as file:
    inp = file.read()


vals = list(map(lambda k: int(k), re.sub('\n*[a-z]+', ' 0', inp).split()))
sums = []
for i in range(len(vals)//40):
    cycle_num = (i * 40 + 20)
    sums.append((sum(vals[0:cycle_num-1])+1)*cycle_num)

print(sum(sums))


print(vals)
current_x = 1
crt_x = 0
pixels = []
for i in range(len(vals)):
    current_x += vals[i-1]
    pixel = '#' if abs(crt_x - current_x) < 2 else '.'
    crt_x = (crt_x+1) % 40
    pixels.append(pixel)


for i in range(6):
    print(''.join(pixels[i*40:(i+1)*40]))
