import re

# 1. Match 'a' followed by zero or more 'b'
s = input()
print(bool(re.fullmatch(r"ab*", s)))


# 2. Match 'a' followed by two to three 'b'
s = input()
print(bool(re.fullmatch(r"ab{2,3}", s)))


# 3. Find sequences of lowercase letters joined with underscore
s = input()
print(re.findall(r"[a-z]+_[a-z]+", s))


# 4. Find sequences of one uppercase letter followed by lowercase letters
s = input()
print(re.findall(r"[A-Z][a-z]+", s))


# 5. Match 'a' followed by anything, ending in 'b'
s = input()
print(bool(re.fullmatch(r"a.*b", s)))


# 6. Replace all spaces, commas, and dots with colon
s = input()
print(re.sub(r"[ ,.]"," :", s))


# 7. Convert snake_case string to camelCase
s = input()
def camel(m):
    return m.group(1).upper()
print(re.sub(r"_([a-z])", camel, s))


# 8. Split a string at uppercase letters
s = input()
print(re.split(r"(?=[A-Z])", s))


# 9. Insert spaces between words starting with capital letters
s = input()
print(re.sub(r"([A-Z])", r" \1", s).strip())


# 10. Convert camelCase string to snake_case
s = input()
print(re.sub(r"([A-Z])", r"_\1", s).lower())