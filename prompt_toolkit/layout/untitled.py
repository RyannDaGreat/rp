def CommonPrefix(s1, s2):
	# 0.21143    seconds
    out = ''
    for i, j in zip(s1, s2):
        if i != j:
            break
        out += i
    return out

def slow_longest_common_prefix(seq1, seq2):
	# TICTOC: 0.63711    seconds
    start = 0
    while start < min(len(seq1), len(seq2)):
        if seq1[start] != seq2[start]:
            break
        start += 1
    return seq1[:start]



 >>> longest_common_suffix('12345abcd','876323abcd')
ans = abcd
 >>> longest_common_suffix('adofoieabcd','29348psaabcd')
ans = abcd
 >>> longest_common_suffix('adofoieabcd','29348psaabqcd')
ans = cd
 >>> longest_common_suffix([1,2,3,4,5],[7,6,3,4,5])
ans = [3, 4, 5]
 >>> longest_common_suffix([1,2,3,4,5],[7,3,3,4,3,6,3,4,5])
ans = [3, 4, 5]
