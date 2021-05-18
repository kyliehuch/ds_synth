with open('test.txt') as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

print(data)
