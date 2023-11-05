# from bs4 import BeautifulSoup


# with open('Amazon.com_ TCL 10L, Unlocked Android Smartphone with 6.53_ FHD + LCD Display, 48MP Quad Rear Camera System, 64GB+6GB RAM, 4000mAh Battery - Arctic White _ Cell Phones & Accessories.html', 'r', encoding='utf-8') as file:
#     html_source = file.read()
# soup = BeautifulSoup(html_source, 'html.parser')

# img_tags = soup.select('img')
# print(img_tags)
# for img in img_tags:
#     src = img.get('src')
#     if src:
#         print("Image URL:", src)

#------------------------------------------------------------
# perfect
from bs4 import BeautifulSoup
import re

import requests

url = 'https://www.amazon.com/HP-Ryzen-5500U-Graphics-15-ef2099nr/dp/B0C1PQL8QB/ref=sr_1_10?qid=1698341913&s=computers-intl-ship&sr=1-10&th=1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
# print(response.text)
# Load and parse the saved HTML source
# with open('Amazon.com_ TCL 10L, Unlocked Android Smartphone with 6.53_ FHD + LCD Display, 48MP Quad Rear Camera System, 64GB+6GB RAM, 4000mAh Battery - Arctic White _ Cell Phones & Accessories.html', 'r', encoding='utf-8') as file:
#     html_source = file.read()

# soup = BeautifulSoup(html_source, 'html.parser')
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
# Use a regular expression to find image URLs that start with "https," end with ".jpg," and contain "_AC"
image_urls = soup.find_all('img')
# image_urls = soup.find_all('img')
# print(image_urls)
# Extract and print the matched image URLs
for img in image_urls:
    src = img.get('src')
    if src:
        if src[-4:] == ".jpg":

            print( src)








# import requests

# # The URL of the web page you want to save
# url = 'https://www.amazon.com/TCL-Unlocked-Android-Smartphone-Display/dp/B087LYQ22N/ref=sr_1_1_sspa?crid=17OSYBMPPLBAI&dchild=1&keywords=smartphone&qid=1611056472&s=electronics&sprefix=smart%2Celectronics-intl-ship%2C250&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExWTVBTDNGWU9JR0pDJmVuY3J5cHRlZElkPUEwNDQ0MTQyMlRLVUE2MDFGSjhFQSZlbmNyeXB0ZWRBZElkPUEwMzE2MjI3MU1HMVlXSko2RjRTUSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# # Send an HTTP GET request to the URL
# response = requests.get(url, headers=headers)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Get the HTML content of the page
#     html_content = response.text

#     # Define a file name to save the HTML source
#     file_name = 'webpage.html'

#     # Open the file in write mode and save the HTML content
#     with open(file_name, 'w', encoding='utf-8') as file:
#         file.write(html_content)

#     print(f'HTML source saved to {file_name}')
# else:
#     print(f'Failed to retrieve the web page. Status code: {response.status_code}')
