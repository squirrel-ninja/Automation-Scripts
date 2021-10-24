import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import random
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def config():
    firefox_options = Options()
    firefox_options.add_argument("--disable-logging")
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--window-size=1920x1080")
    return firefox_options


def setup(url, class_name, no_of_questions, no_of_options):
    driver = webdriver.Firefox(options=config())
    driver.get(url)
    options = driver.find_elements_by_class_name(class_name)
    form_page = {}
    for i in range(1, no_of_questions+1):
        form_page[i] = {}
        for j in range(1, no_of_options[i]+1):
            form_page[i][j] = options.pop(0)

    return driver, form_page

def compute_response_table(no_of_responses, response_percent_table):
    """
    no_of_responses -> No of responses you need to generate
    response_percent_table -> {
        1: {
            1: 60,
            2: 40
        },
        2: {
            1: 5,
            2: 75,
            3: 18,
            4: 2
        },
        3: {
            1: 5,
            2: 20,
            3: 25,
            4: 30,
            5: 20
        },
        4: {
            1: 45,
            2: 40,
            3: 10,
            4: 2,
            5: 3

        }
    }

    """
    output = {}
    temp1 = {}
    for i in response_percent_table:
        temp1[i] = {}
        output[i] = []
        for j in response_percent_table[i]:
            temp = []
            #print(i,j)
            num = (response_percent_table[i][j]*no_of_responses)/100
            if num > 0 and num < 1:
                num = 1
            else:
                num = round(num)
            temp1[i][j] = num
            output[i].extend([j for i in range(num)])
        
        for i in output:
            if len(output[i]) < no_of_responses:
                output[i].extend([1 for i in range(no_of_responses-len(output[i]))])
            elif len(output[i]) > no_of_responses:
                output[i] = output[i][:no_of_responses]

    print("Response summary, option wise count: ", temp1)
    return output

        

def fill_random_response(no_of_responses, url, no_of_questions, option_layout):
    for i in range(no_of_responses):
        setup_hook, form_page_layout = setup(
            url,
            no_of_questions,
            option_layout
        )
        for j in form_page_layout:
            question_options = list(form_page_layout[j].keys())
            option_to_be_filled = np.random.choice(question_options, size=1, replace=False)[0]
            form_page_layout[j][option_to_be_filled].click()
        submit_button = setup_hook.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "exportButtonContent", " " ))]')
        submit_button.click()
        print("Submitted form ", i+1, "time")
        setup_hook.quit()

def fill_biased_response(no_of_responses, options_percentage, url, no_of_questions, option_layout):
    response_options = compute_response_table(no_of_responses, options_percentage)
    """
    option layout -> {1:2,2:4,3:5,4:5} -> Key is the question number, and value is the number of options
    """
    for i in range(no_of_responses):
        setup_hook, form_page_layout = setup(
            url,
            no_of_questions,
            option_layout
        )
        time.sleep(1.5) # -> needed so that page is fully loaded and can be scrolled into view
        for j in form_page_layout:
            question_options = list(form_page_layout[j].keys())
            option_to_be_filled = response_options[j][i]
            form_page_layout[j][option_to_be_filled].click()
        submit_button = setup_hook.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "exportButtonContent", " " ))]')
        setup_hook.execute_script("arguments[0].click();", submit_button)
        print("Submitted form ", i+1, "time")
        setup_hook.quit()


l = {
    1: {
        1: 60,
        2: 40
    },
    2: {
        1: 5,
        2: 75,
        3: 18,
        4: 2
    },
    3: {
        1: 5,
        2: 20,
        3: 25,
        4: 30,
        5: 20
    },
    4: {
        1: 45,
        2: 40,
        3: 10,
        4: 2,
        5: 3

    }
}

if __name__ == '__main__':
    # Code to use either of the two functions
