def find_dup_str(s, n):
    if n <= 0:
        return ""
    i = 0
    while i + n <= len(s):
        sub = s[i:i + n]
        j = i + n
        while j + n <= len(s):
            if s[j:j + n] == sub:
                return sub
            j += 1
        i += 1
    return ""


s = input("Enter a string: ")
n = int(input("Enter substring length: "))
print(find_dup_str(s, n))


def find_max_dup(s):
    n = len(s) // 2
    while n >= 1:
        result = find_dup_str(s, n)
        if result != "":
            return result
        n -= 1
    return ""


s = input("Enter a string: ")
print(find_max_dup(s))
