import re
pattern = r'a*b*'
test_string = "abbb"

if re.fullmatch(pattern, test_string):
    print("Match found!")
else:
    print("No match found.")