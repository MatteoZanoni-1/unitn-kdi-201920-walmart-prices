from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np


def main():
    df = create_dataframe()
    options = Options()
    options.headless = True
    with webdriver.Chrome(
            executable_path='/Users/MatteoZanoni/Desktop/Prove/chromedriver',
            options=options) as driver:
        df = df.apply(lambda row: get_product(row, driver), axis=1)
        df.to_json('walmart_products.json', orient='records')


def get_product(series, driver):
    if not series.todo:
        return series
    try:
        driver.get(
            f'http://www.walmart.com/search/?query={series.original_name}')
        soup = BeautifulSoup(driver.execute_script(
            "return document.body.outerHTML;"), 'html.parser')
    except Exception:
        return series
    items = soup.find_all('div', class_='search-result-gridview-item')
    if len(items) == 0:
        series.found = False
    else:
        try:
            item = items[0]
            full_name = item.find(
                'a', class_='product-title-link').get('title')
            link = 'http://www.walmart.com' +\
                item.find('a', class_='product-title-link').get('href')
            price_unit = item.find(
                'span', class_='price-characteristic').text
            price_decs = item.find('span', class_='price-mantissa').text
            price = round(int(price_unit) + float(int(price_decs)/100), 2)
            rating = item.find(
                'span', class_='seo-avg-rating').text
            series.found = True
            series.found_name = full_name
            series.price = price
            series.rating = rating
            series.link = link
            print(f'found {series.original_name}')
        except Exception:
            series.found = False
            print(f'{series.original_name} not found')
    series.todo = False
    return series


def create_dataframe():
    df = pd.read_json(
        '../unitn-kdi-201920-data-selection/labels.json', orient='records')
    df.rename({'title': 'original_name'}, inplace=True, axis=1)
    df['todo'] = True
    df['found'] = np.nan
    df['found_name'] = np.nan
    df['price'] = np.nan
    df['rating'] = np.nan
    df['link'] = np.nan
    return df


if __name__ == "__main__":
    main()
