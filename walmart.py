from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

product = 'Mucinex'

options = Options()
options.headless = True
with webdriver.Chrome(
        executable_path='/Users/MatteoZanoni/Desktop/Prove/chromedriver',
        options=options) as driver:
    driver.get(f'http://www.walmart.com/search/?query={product}')
    soup = BeautifulSoup(driver.execute_script(
        "return document.body.outerHTML;"), 'html.parser')
    items = soup.find_all('div', class_='search-result-gridview-item')
    if len(items) == 0:
        print('Not found')
    else:
        for item in [items[0]]:
            full_name = item.find(
                'a', class_='product-title-link').get('title')
            link = 'http://www.walmart.com' + \
                item.find('a', class_='product-title-link').get('href')
            currency = item.find('span', class_='price-currency').text
            price_unit = item.find('span', class_='price-characteristic').text
            price_decs = item.find('span', class_='price-mantissa').text
            price = round(int(price_unit) + float(int(price_decs)/100), 2)

            print(f'{full_name} -> {price}{currency}')
            print(link)
