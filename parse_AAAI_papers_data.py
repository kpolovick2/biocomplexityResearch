import csv

# create an empty list that will store an item's tags at each index
tags_by_item = []
# create an empty list that will store an item's topics at each index
topics_by_item = []
# open the csv file
with open('[UCI] AAAI-13 Accepted Papers - Papers.csv', encoding='utf8') as aaai:
    # read the csv file
    csv_aaai = csv.reader(aaai, delimiter=',')
    # for each row in the csv file
    for row in csv_aaai:
        # if the row is not the row containing column names
        if row[3] != 'High-Level Keyword(s)':
            # create a list of tags in the row
            row_tags = row[3].split("\n")
            # append this list to tags_by_item
            tags_by_item.append(row_tags)
            # create a list of the topics in the row
            row_topics = row[2].split("\n")
            # append the list to topics_by_item
            topics_by_item.append(row_topics)

# create an empty list that stores the tags of the data set
tags = []
# for each item in tags_by_item
for item in tags_by_item:
    # for each tag associated with that item:
    for tag in item:
        # if the tag is not already stored
        if tag not in tags:
            # store it
            tags.append(tag)

# create the B matrix
B = []

for item in tags_by_item:
    b_append = [0 for i in range(len(tags))]

    for i in range(len(tags)):
        if tags[i] in item:
            b_append[i] = 1

    B.append(b_append)

topics = []
for item in topics_by_item:
    for topic in item:
        if topic not in topics:
            topics.append(topic)

print(topics_by_item)
print(tags_by_item)
print(tags)
print(topics)
print(B)