
words = []
with open("/usr/share/hunspell/en_US.dic", mode="r") as f:
    for word in f:
        word = word.rstrip().split("/")[0]
        if len(word) >= 3:
            words.append(word)

hashes = []
with open("0x0C6EF9E1", mode="r") as f:
    for l in f:
        start = "  Solved: "
        if l.startswith(start):
            hashes.append((0,l[len(start):].rstrip()))

for i in range(len(hashes)):
    score, hash = hashes[i]
    for word in words:
        if (hash.startswith(word+"_")) or ("_"+word+"_" in hash) or (hash.endswith("_"+word)):
            score = score + 100 * len(word)
        if word in hash:
            score = score + 1 * len(word)
    hashes[i] = (score, hash)

def compare(i1, i2):
    if i1[0] != i2[0]:
        return i1[0] < i2[0]
    else:
        return sorted([i1[1], i2[1]], key=str.lower)[0] == i1[0]

for h in sorted(hashes):
    print("{: >6}\t{}".format(h[0], h[1]))

