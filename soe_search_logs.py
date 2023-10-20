'''
This Python script is offered with no formal support from Stack Overflow. 
If you run into difficulties, reach out to the person who provided you with this script.
'''

# Standard library imports
import argparse
import csv
import time

# Third party imports
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def main():

    args = get_args()
    s = create_session(args.url)
    search_logs = get_search_logs(s, args.url)
    export_search_logs_to_csv(search_logs)


def get_args():

    parser = argparse.ArgumentParser(
        prog='soe_search_metrics.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Gathers search logs from Stack Overflow for Teams and exports them to a CSV '
                    'file.',
        epilog = 'Example for Stack Overflow Enterprise: \n'
                 'python3 soe_search_logs.py --url "https://SUBDOMAIN.stackenterprise.co"\n\n')
    parser.add_argument('--url', 
                        type=str,
                        help='[REQUIRED] Base URL for your Stack Overflow for Teams instance')

    return parser.parse_args()


def create_session(base_url):

    # setup selenium driver for Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=500,800")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    # get login page
    driver.get(base_url)

    # wait for user to log in
    while True:
        try:
            # element names for selenium: https://selenium-python.readthedocs.io/locating-elements.html
            driver.find_element("class name", "s-user-card")
            break
        except:
            time.sleep(1)
    
    # pass cookies to requests session before closing selenium driver
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.close()
    driver.quit()
    
    return s


def get_search_logs(s, base_url):

    logs_url = base_url + '/developer/logs/3'
    
    page_count = get_page_count(s, logs_url + '?page=1&pagesize=50')
    search_logs = []
    for page in range(1, page_count + 1):
        print(f'Getting search logs from page {page} of {page_count}')
        page_url = logs_url + f'?page={page}&pagesize=50'
        response = get_page_response(s, page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        log_entries = soup.find_all('tr') 
        search_logs += get_logs_from_page(log_entries)

    return search_logs


def get_page_count(s, url):

    response = get_page_response(s, url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find_all('a', {'class': 's-pagination--item js-pagination-item'})
    try:
        page_count = int(pagination[-2].text)
    except IndexError: # only one page
        page_count = 1

    return page_count


def get_page_response(s, url):

    response = s.get(url)
    if response.status_code == 200:
        return response
    else:
        print(f'Error getting page {url}')
        print(f'Response code: {response.status_code}')
        return None


def get_logs_from_page(log_entries):
    
        search_logs = []
        for entry in log_entries:
            if entry.find('th'):
                continue

            columns = entry.find_all('td')
            log_entry = {
                'timestamp': entry.find('span', {'class': 'relativetime'})['title'],
                'query': columns[2].text,
                'user_id': columns[4].text
            }
            search_logs.append(log_entry)
        
        return search_logs


def export_search_logs_to_csv(search_logs):

    file_name = 'search_logs.csv'

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = list(search_logs[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for log in search_logs:
            writer.writerow(log)

    print(f'Search logs exported to {file_name}')

if __name__ == '__main__':

    main()
