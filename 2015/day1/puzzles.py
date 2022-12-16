inp = open('input').read()
print(len(inp) - 2*inp.count(')'))
print([i for i in range(len(inp)) if (len(inp[:i]) - 2*inp[:i].count(')')) == -1][0])