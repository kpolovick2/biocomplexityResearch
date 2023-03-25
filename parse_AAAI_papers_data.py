import csv

tags = []
with open('[UCI] AAAI-13 Accepted Papers - Papers.csv', encoding='utf8') as aaai:
    csv_aaai = csv.reader(aaai, delimiter=',')
    for row in csv_aaai:
        if row[3] != 'High-Level Keyword(s)':
            row_tags = row[3].split("\n")
            tags.append(row_tags)

print(tags)