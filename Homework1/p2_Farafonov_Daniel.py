def find_Pythagorean(n):
    triples = []
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a * a + b * b == c * c:
                    triples.append((a, b, c))
    return triples


n = int(input("Enter n: "))
for triple in find_Pythagorean(n):
    print(triple)
