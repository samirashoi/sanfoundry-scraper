from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pprint

def get_quiz_data(url):
    options = Options()
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    options.headless =True

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    js = "Array.from(document.getElementsByClassName('collapseomatic_content')).forEach((elem) => {elem.style.display = 'block'});"
    browser.execute_script(js)

    quiz_title = browser.find_element_by_class_name('entry-title').text.split('–', 1)[-1].strip()

    all_ps = browser.find_element_by_class_name('entry-content').find_elements_by_tag_name('p')
    questions = list()
    options_s = list()
    for p in all_ps:
        if re.match(r'\d{1,2}\. ',p.text):
            
            question_with_options = p.text.strip('View Answer').strip()
            question_with_options = re.split(r'\d{1,2}\. ', question_with_options, 1)[1]
            question_with_options_list = re.split(r'\n\w{1}\) ', question_with_options, re.A)
            question, options = question_with_options_list[0].strip(), question_with_options_list[1:] 
    
            questions.append(question.strip())
            options_s.append(options)

    answers = list()
    explanations = list()
    all_collapsible_content = browser.find_elements_by_class_name('collapseomatic_content')
    for div in all_collapsible_content:
        answer = re.match(r'Answer:\s*(.)\n', div.text).group(1)
        explanation = re.search(r'Explanation:\s*(.*)', div.text).group(1)
        answer = ord(answer.strip()) - ord('a') + 1
    
        answers.append(answer)
        explanations.append(explanation.strip())

    browser.quit()

    number_of_ques = len(questions)

    quiz_dictionary = {}
    quiz_dictionary['topic'] = quiz_title.strip()
    quiz_dictionary['questions'] = list()
    for i in range(number_of_ques):
        quiz_dictionary_question = dict()
        quiz_dictionary_question['question'] = questions[i]
        quiz_dictionary_question['options'] = options_s[i]
        quiz_dictionary_question['answer'] = answers[i]
        quiz_dictionary_question['explanation'] = explanations[i]
        quiz_dictionary['questions'].append(quiz_dictionary_question)

    return(quiz_dictionary)

if __name__=='__main__':
    url = input('Enter Sanfoundry URL for scraping quiz data: ')
    
    example_url = 'https://www.sanfoundry.com/computer-networks-mcqs-basics/' 

    url = example_url if url == "" else url
    
    start = time.time()
    q_d = get_quiz_data(url)
    pprint.pprint(q_d)
    end = time.time()

    print(f'Time elapsed: {end-start}')