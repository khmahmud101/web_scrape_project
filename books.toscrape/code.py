import requests
import csv
from bs4 import  BeautifulSoup
import sys
import logging
from html import unescape


def get_content(url):
    ''' Receice page url and return content of that page '''
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def get_next_page(url,content):
    ''' find next page url '''


    next_page = content.find(class_='next')
    if next_page == None:
        return None
    next_page = next_page.find('a').get_text()
    next_page_url = url.rfind("/")
    return url[0:next_page_url+1] + next_page


def scrape_book_info(category_name,book_name,book_url):
    ''' Reiceve category_name,book_name,book_url, crawl book url and return book details and store them in book_dict'''
    book_dict ={}
    category_name = category_name.replace("\n","")
    category_name = category_name.replace(" ","")
    book_dict["Category"] = category_name

    book_name = unescape(book_name)
    book_dict["Book Name"] = book_name
    book_dict["Book URL"] = book_url

    print("Scraping Book" + book_name)
    logging.info("Scraping: " + book_url)

    content = get_content(book_url)

    # Book Image url Insert in book_dict
    book_other_info = content.find(class_="table table-striped")
    #print(book_other_info)
    book_other_info = book_other_info.find_all('td')


    book_dict["UPC"] = book_other_info[0].get_text()
    book_dict["Price"] = book_other_info[2].get_text()
    book_dict["Availability"] = book_other_info[5].get_text()

    csv_writer.writerow(book_dict)




def crawl_category(category_name,category_url):
    ''' Receive category name and url, Crawl every category and return their book name and book details page url '''
    while True:
        content = get_content(category_url)
        #print(content)
        books_info = content.find_all(class_='product_pod')
        #book_info_final = book_info.find('h3')
        #print(books_info)

        for book_info in books_info:
            book_info_final = book_info.find('h3')
            book_name = book_info_final.find('a').get_text()
            book_url = book_info_final.find('a').get('href')
            book_url = book_url.replace("../../../","")
            book_url = "http://books.toscrape.com/catalogue/" + book_url
            #print(book_name)
            #print(book_url)
            scrape_book_info(category_name,book_name,book_url)
        next_page = get_next_page(category_url,content)
        if next_page is None:
            break
        category_url = next_page






def crawl_website():
    ''' crawl_website is the main function that coordinates whole scraping task '''
    url = 'http://books.toscrape.com/'
    content = get_content(url)
    if content == None:
        logging.critical("Got empty content from" + url)
        sys.exit(1)
    category_items = content.find(class_='side_categories')
    category_items_list = category_items.find_all('a')
    category_items_list = category_items_list[1:]
    for category_item in category_items_list:
        category_name = category_item.get_text()

        category_url = category_item.get('href')
        category_url = url + category_url
        #print(category_name)
        #print(category_url)
        crawl_category(category_name,category_url)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='toscrape_crawl.log',level=logging.DEBUG)
    fields_name = ["Category", "Book Name","Book URL","UPC","Price","Availability"]
    with open('bool_list.csv',"w",encoding="ISO-8859-1") as csvf:
        csv_writer = csv.DictWriter(csvf,fieldnames = fields_name)
        csv_writer.writeheader()

        crawl_website()
        print("Crawling Done!")
