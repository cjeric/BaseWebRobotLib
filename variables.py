from selenium import webdriver as _webdriver


# browser = _webdriver.Firefox()
# a='a'

def get_variables(*args):
    if len(args) == 0:
        driver = _webdriver.Firefox()
    elif args[0].lower() == 'ie':
        print ('launch IE')
        driver = _webdriver.Ie()
    else:
        driver = _webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.maximize_window()

    variables = {'browser': driver}
    return variables
