import sys
import re

raw_data_path = sys.argv[1]
raw_data = ''

with open(raw_data_path, 'r') as f:
    raw_data = f.read()
clean_data = raw_data.replace('|\n', '\n')
with open('try.txt', 'w') as f:
    f.write(clean_data)

