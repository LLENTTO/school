import re

with open('row.txt', 'r', encoding='utf-8') as file:
    receipt_text = file.read()

item_pattern = re.compile(
    r'(\d+)\.\n(.+?)\n(\d{1,3}(?:\s\d{3})*),000 x (\d{1,3}(?:\s\d{3})*),00\n(\d{1,3}(?:\s\d{3})*),00',
    re.DOTALL
)

total_pattern = re.compile(r'ИТОГО:\n(\d{1,3}(?:\s\d{3})*),00')

def clean_number(num):
    return int(num.replace(" ", ""))

items = item_pattern.findall(receipt_text)
for item in items:
    item_num = item[0]
    name = item[1].strip()
    quantity = clean_number(item[2])
    unit_price = clean_number(item[3])
    total_price = clean_number(item[4])

    print(f"Item {item_num}: {name} - Quantity: {quantity}, Unit Price: {unit_price}, Total: {total_price}")

total = total_pattern.search(receipt_text)
if total:
    print(f"Total: {clean_number(total.group(1))}")
