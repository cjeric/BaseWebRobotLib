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
    user = 'chengjie_jack'
    pwd = 'Eric890420WY'
    smtp_server = 'smtp.126.com'
    variables = {'browser': driver,
                 'user': user,
                 'pwd': pwd,
                 'smtp_server': smtp_server}
    return variables
