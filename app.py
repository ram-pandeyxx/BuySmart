from flask import Flask, render_template, request
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import threading
import time


app = Flask(__name__, '/static')

def flipkart(title2):
    flipkartProductArr = []
    title = ''
    indPrice = ''
    Photo = ''
    link = ''
    productClassName = "_75nlfW"
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    
    flipkartURL = f"https://www.flipkart.com/search?q={title2}"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
    driver.get(flipkartURL)

    try:
        productname = driver.find_element(By.CSS_SELECTOR, f".{productClassName} div.col.col-7-12 div")
        classTest = productname.get_attribute("class")
        if classTest == "KzDlHZ":
            title = productname.text
    except:
        pass
    try:
        productname = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .wjcEIp")
        classTest = productname.get_attribute("class")
        if classTest == "wjcEIp":
            title = productname.text
    except:
        pass

    try:
        price = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .hl05eU div")
        indPrice = str(price.get_attribute("textContent")[1:])
    except:
        pass

    try:
        photo = driver.find_element(By.CSS_SELECTOR, f".{productClassName} ._4WELSP img")
        Photo = photo.get_attribute("src")
    except:
        pass

    try:
        link = driver.find_element(By.CSS_SELECTOR, f".{productClassName} a").get_attribute("href")
    except:
        pass
    
    driver.quit()

    flipkartProductArr.append(title)
    flipkartProductArr.append(indPrice)
    flipkartProductArr.append(Photo)
    flipkartProductArr.append(link)
    time.sleep(1)
    
    return flipkartProductArr

def amazon(title2):
    amazonProductArr = []
    titleA = ''
    indPriceA = ''
    photo = ''
    linkA = ''
    amazont = ''
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    
    amazonURL = f"https://www.amazon.in/s?k={title2}"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
    driver.get(amazonURL)
    
    try:
        titleA = driver.find_element(By.CSS_SELECTOR, ".s-title-instructions-style h2 a span")
        amazont = titleA.text
    except:
        pass
    
    try:
        priceA = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen")
        indPriceA = str(priceA.get_attribute("textContent")[1:])
    except:
        pass
    
    try:
        linkA = driver.find_element(By.CSS_SELECTOR, ".aok-relative span a").get_attribute("href")
    except:
        pass
    
    try:
        photo = driver.find_element(By.CSS_SELECTOR, ".aok-relative span a div img").get_attribute("src")
    except:
        pass
    
    driver.quit()
    
    amazonProductArr.clear()
    amazonProductArr.append(linkA)
    amazonProductArr.append(amazont)
    amazonProductArr.append(indPriceA)
    amazonProductArr.append(photo)
    time.sleep(1)
    
    return amazonProductArr

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    title2 = request.form['Name']
    
    flipkart_result = []
    amazon_result = []
    
    thread1 = threading.Thread(target=lambda q, arg1: q.append(flipkart(arg1)), args=(flipkart_result, title2))
    thread2 = threading.Thread(target=lambda q, arg1: q.append(amazon(arg1)), args=(amazon_result, title2))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    flipkart_result = flipkart_result[0]
    amazon_result = amazon_result[0]
    
    return render_template('index.html', 
                           name=flipkart_result[0], 
                           price=flipkart_result[1], 
                           image=flipkart_result[2], 
                           link=flipkart_result[3],
                           name2=amazon_result[1],
                           price2=amazon_result[2],
                           image2=amazon_result[3],
                           link2=amazon_result[0])


if __name__ == "__main__":
    app.run(debug=True)

