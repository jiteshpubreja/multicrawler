# import packages
from bs4 import BeautifulSoup
import requests
import os
from cleaner import tokenizer
from langdetect import detect

# finding provided user defined environment as .env file and load it


def crawler(link,primary_lang, secondary_lang):
    secondary_out = ''
    primary_out = ''
    # sending get request to link
    data = requests.get(link)
    # Getting content and parse html data
    soup = BeautifulSoup(data.content, 'html.parser')
    data_list = []
    # user_choice = input(f'Want to explore all links in link {link}?("y/n") : ')
    data_links = [link['href'] for link in soup.find_all('a', href=True)]
    data_links.append(link)
    data = requests.get(link)
    soup = BeautifulSoup(data.content, 'html.parser')
    tags = list(set([tag.name for tag in soup.find_all()]))
    for tag in tags:
        for inf in soup.find_all(tag):
            text_data = inf.text
            data_list.append(text_data)
    str_data = tokenizer(' '.join([i for i in data_list]))
    data_list = list(set(str_data.split('\n')))
    for line in data_list:
        try:
            if detect(line) == secondary_lang:
                secondary_out = secondary_out+line+'\n'
            if detect(line) == primary_lang:
                primary_out = primary_out+line+'\n'
        except:
            continue
    return secondary_out, primary_out
    # if detect(line) == 'pa':
    #     pa_out.write(line+'\n')
    # else:
    #     en_out.write(line+'\n')
    # pa_out.write('\n'.join([i for i in data_list]))


def crawl_links(link):
    # sending get request to link
    data = requests.get(link)
    # Getting content and parse html data
    soup = BeautifulSoup(data.content, 'html.parser')
    data_links = []
    # user_choice = input(f'Want to explore all links in link {link}?("y/n") : ')
    for i in soup.find_all('a', href=True):
        if i['href'].startswith('h'):
            data_links.append(i['href'])
        else:
            data_links.append(link+i['href'])
    data_links.append(link)
    return data_links


if __name__ == "__main__":
    link = 'http://www.punjabiuniversity.ac.in/Pages/Page.aspx?dsenc=AboutUnv'
    print(crawler(link))
