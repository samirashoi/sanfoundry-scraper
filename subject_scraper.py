from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pprint
from topic_scaper import get_topic_data

def get_subject_data(url, sample=False):
    options = Options()
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    # options.headless =True

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    subject_title = re.split("Questions and Answers", browser.find_element_by_class_name('entry-title').text)[0].strip() 


    domains = browser.find_elements_by_tag_name('h4')
    domain_names =[]
    for domain in domains:
        domain_names.append(re.split(r'Questions.* on', domain.text)[-1].strip())

    tables = browser.find_elements_by_tag_name('table')
    table_links_hrefs = []
    for table in tables:
        table_links_per_domain = table.find_elements_by_tag_name('a')
        table_links_hrefs_per_domain = []
        for link in table_links_per_domain:
            table_links_hrefs_per_domain.append(link.get_attribute('href'))
        table_links_hrefs.append(table_links_hrefs_per_domain)

    browser.quit()

    # Small Dataset 
    smol_dom_names = domain_names[:2]
    smol_table_links = table_links_hrefs[:2]
    smol_dictionary = dict(zip(smol_dom_names, smol_table_links))

    # Temporary Dataset
    temp_dictionary = dict(zip(domain_names, table_links_hrefs))

    # Final Dataset
    subject_dictionary = dict()
    subject_dictionary['subject'] = subject_title
    subject_dictionary['domains'] = list()

    if sample:
        temp_dictionary = smol_dictionary

    domain_counter = 0
    for domain in temp_dictionary:
        dom_dict = dict()
        dom_dict['domain'] = domain
        links = temp_dictionary[domain]
        topic_counter = 0
        quiz_topics = list()
        for link in links:    
            quiz_topic = get_topic_data(link)
            quiz_topics.append(quiz_topic)
            topic_counter += 1
            print(f'{topic_counter} topics parsed')
            time.sleep(2)
        dom_dict['topics'] = quiz_topics  
        subject_dictionary['domains'].append(dom_dict)
        domain_counter += 1
        print(f'{domain_counter} domains parsed')
    
    return subject_dictionary


if __name__ == '__main__':
    url = input('Enter subject URL from sanfoundry.com: ')
    example_url = 'https://www.sanfoundry.com/computer-network-questions-answers/'
    url = example_url if url == "" else url


    start = time.time()
    subject_dictionary = get_subject_data(url, sample=True)
    end = time.time()
    pprint.pprint(subject_dictionary)
    print(f"Time Elapsed: {end-start}")
