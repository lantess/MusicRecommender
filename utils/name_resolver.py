import os

DIR = '../data/wav.prod'
DEST = 'data/wav.prod/done'

for file in os.listdir(DIR):
    if file.find('.wav') == -1:
        continue
    new_file = file.replace('.wav', '')\
        .replace('\'', '')\
        .replace('!', '') \
        .replace('.avi', '')\
        .replace('.vmw', '')\
        .replace('"', '')
    while new_file.find('(') != -1 and new_file.find(')'):  #usunięcie tekstu w nawiasach
        new_file = new_file[:new_file.find('(')]+new_file[new_file.find(')')+1:]
    while new_file.find('[') != -1 and new_file.find(']'):  # usunięcie tekstu w nawiasach kwadratowych
        new_file = new_file[:new_file.find('[')] + new_file[new_file.find(']') + 1:]
    if new_file.find('-') != -1:
        print(new_file)