s = """
D N A
3
""".strip('\n').split('\n')

alphabet, n = s[0].split(), int(s[1])

def generate(n, prefix=""):
    print prefix
    if n == 0:
        return
    for c in alphabet:
        generate(n - 1, prefix + c)

generate(n)
