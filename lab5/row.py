import re

with open('row.txt', 'r', encoding='utf-8') as file:
    receipt_text = file.read()

item_pattern = re.compile(r'(\d+)\.\n(.+?)\n(\d+,\d{3}) x (\d+,\d{2})\n(\d+,\d{2})', re.DOTALL)
total_pattern = re.compile(r'ИТОГО:\n(\d+,\d{3},\d{2})')

items = item_pattern.findall(receipt_text)
for item in items:
    print(f"Item {item[0]}: {item[1].strip()} - Quantity: {item[2]}, Unit Price: {item[3]}, Total: {item[4]}")

total = total_pattern.search(receipt_text)
if total:
    print(f"Total: {total.group(1)}")