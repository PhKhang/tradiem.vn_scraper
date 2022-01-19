import json
import requests
import sys
import argparse
from lxml import html
from bs4 import BeautifulSoup

# parser = argparse.ArgumentParser(description='Optional app description')
# parser.add_argument('-n', type=int, nargs="?", default=0)
# foo = int(parser.selectport[0])

USERNAME = ""
PASSWORD = "123"

LOGIN_URL = "http://tradiem.vn/Account/Login"
URL = "http://tradiem.vn/XemDiem/BangDiem/1079016/35273/74"

def parseArguments():
    # Optional arguments
    parser.add_argument("-dD", "--debtDad", help="Debt dad.", type=float, default=1000.)
    return args

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='__RequestVerificationToken']/@value")))[0]

    # Create payload
    payload = {
        "UserName": USERNAME, 
        "Password": PASSWORD, 
        "__RequestVerificationToken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//div[@class='shd']/a/text()")
    bruh = tree.xpath("//tbody")
    soup = BeautifulSoup(result.text, "lxml")

    # Testing code
    #print(bucket_names)
    #print(bruh)
    #print(soup)
    #print(result.text)
    #print(html.tostring(tree))

    # if foo > 10:
    #     print('saw the arg')
    #args = parseArguments()
    #print(args.debtDad)

    gdp_table = soup.find("table", attrs={"class": "tb_bangdiem"})
    if gdp_table is None:
        print("No table. Login failed")
    else: print('Login successful!\n')
    gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows
    mon = ['toan', 'vatli', 'hoa', 'sinh', 'tin', 'van', 'su', 'dia', 'anh', 'gdcd', 'congnghe', 'theduc', 'gdqp', 'nghe', 'tuchon']
    diem = {'toan': [],
    'vatli': [],
    'hoa': [],
    'sinh': [],
    'tin': [],
    'van': [],
    'su': [],
    'dia': [],
    'anh': [],
    'gdcd': [],
    'congnghe': [],
    'theduc': [],
    'gdqp': [],
    'nghe':[],
    'tuchon':[]}
    #print(gdp_table_data[7].text)
    print(soup.find("td", attrs={"class": "noborder text_center"}).text, '\t', soup.find_all("td", attrs={"class": "noborder"})[3].text)
    print(soup.find_all("td", attrs={"class": "noborder"})[5].text, '\t',  soup.find_all("td", attrs={"class": "noborder"})[2].text, '\t', soup.find_all("td", attrs={"class": "noborder"})[4].text)

    #print(json.dumps(gdp_table_data[0].text))
    
    # Extract data
    for x in range(0, len(gdp_table_data)):
        for y in range(0, len(gdp_table_data[x].find_all('td'))):
            print(gdp_table_data[x].find_all('td')[y].text, end='\t')
            if y==1: print(end='\t')
            diem[mon[x]].append(gdp_table_data[x].find_all('td')[y].text)
        print()
    diemjson = json.dumps(diem, indent=2)
    
    #print(diemjson)

if __name__ == '__main__':
    main()
