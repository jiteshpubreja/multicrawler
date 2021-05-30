import re
from langdetect import detect


def SentenceCleaner(line):
    line = re.sub(r"(')(\w+)(')", r" \1 \2 \3 ", line)
    line = re.sub(r'[.?!]$', ' .', line)
    line = re.sub(r'[)]', ' ) ', line)
    line = re.sub(r'[(]', ' ( ', line)
    line = re.sub(r'["]', ' " ', line)
    line = re.sub(r'[“]', ' “ ', line)
    line = re.sub(r'[!]', ' ! ', line)
    line = re.sub(r',[^\d\w]', ' , ', line)
    line = re.sub(r'[,]', ' , ', line)
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'[-]', ' - ', line)
    return line


def tokenizer(data):
    textData = re.sub("[?]", " ? END", data)
    textData = re.sub("[।] [\"]", "। END", textData)
    textData = re.sub("[।]", "। END", textData)
    textData = re.sub("[|]", "| END", textData)
    textData = re.sub("[\n]", " END", textData)
    textData = re.sub("\r\n", " END", textData)
    Sen = re.split("END", textData)
    sentences = '\n'.join([SentenceCleaner(i)
                           for i in Sen if len(i.strip()) > 1])
    return sentences


def clean_en_pa(primary_data, secondary_data, primary_lang,secondary_lang):
    temp_primary_data = []
    temp_secondary_data = []
    for i in primary_data:
        temp_count = []
        for j in i.split():
            print(i.split())
            try:
                if detect(j) == secondary_lang:
                    temp_count.append(secondary_lang)
                else:
                    temp_count.append(primary_lang)
            except:
                continue
        if temp_count.count(secondary_lang) < 3:
            temp_primary_data.append(i)
    for i in secondary_data:
        temp_count = []
        for j in i.split():
            try:
                if detect(j) == secondary_lang:
                    temp_count.append(secondary_lang)
                else:
                    temp_count.append(primary_lang)
            except:
                continue
        if temp_count.count(primary_lang) < 3:
            temp_secondary_data.append(i)
        
    return '\n'.join([i for i in temp_primary_data]), '\n'.join([i for i in temp_secondary_data])
