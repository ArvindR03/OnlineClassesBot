from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import time
import datetime
from discord_wh import post_to_server, post_report_server

PATH = "C:\\Software Downloads\\chromedriver.exe"
OPT = Options()
OPT.add_argument('start-maximized')
OPT.add_argument('--start-maximized')
OPT.add_experimental_option('prefs', {
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 1 
})
DRIVER = webdriver.Chrome(PATH, chrome_options=OPT, service_log_path='NUL')

credentials = {
    'user': 'username here',
    'pass': 'password here'
}

DRIVER.get('https://www.microsoft.com/en-gb/microsoft-365/microsoft-teams/group-chat-software')

def signinlink():
    try:
        element = WebDriverWait(DRIVER, 10).until(
            ec.presence_of_element_located((By.LINK_TEXT, 'Sign in'))
        )
        element.click()
        DRIVER.switch_to.window(DRIVER.window_handles[-1])
    except:
        post_to_server("Couldn't fetch sign-in page. 0000")
        DRIVER.quit()

def usercred():
    try:
        element = WebDriverWait(DRIVER, 10).until(
            ec.presence_of_element_located((By.ID, 'i0116'))
        )
        element.send_keys(CREDS['user'], Keys.RETURN)
    except:
        post_to_server('Couldn\'t enter login credentials. 0001')
        DRIVER.quit()

def passcred():
    try:
        element = WebDriverWait(DRIVER, 10).until(
            ec.presence_of_element_located((By.ID, 'passwordInput'))
        )
        element.send_keys(CREDS['pass'], Keys.RETURN)
    except:
        post_to_server('Couldn\'t enter login credentials. 0002')
        DRIVER.quit()

def postcred():
    try:
        element = WebDriverWait(DRIVER, 10).until(
            ec.presence_of_element_located((By.ID, 'idSIButton9'))
        )
        element.click()
    except:
        post_to_server('Couldn\'t post credentials. 0003')
        DRIVER.quit()

def useapplink():
    try:
        element = WebDriverWait(DRIVER, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'use-app-lnk'))
        )
        element.click()
    except:
        post_to_server('Couldn\'t fetch web app. 0004')
        DRIVER.quit()

def accessclass(classname):
    x = False
    time.sleep(5)
    classlist = DRIVER.find_elements_by_class_name('name-channel-type')

    for i in classlist:
        if classname.lower() in i.get_attribute('innerHTML').lower():
            i.click()
            x = True
            break
    if not x:
        post_to_server('Couldn\'t find class team. 0005')

    timeout = 0
    entered = False

    while timeout <= 15:
        try:
            element = WebDriverWait(DRIVER, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'ts-calling-join-button'))
            )
            element.click()
            entered = True
            break
        except:
            time.sleep(50)
            DRIVER.refresh()
            timeout += 1

    if timeout == 16:
        timeout = True

    if not timeout:
        time.sleep(4)
        cam = DRIVER.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        mic = DRIVER.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
        if cam.get_attribute('title') == 'Turn camera off':
            cam.click()
            time.sleep(1)
        if mic.get_attribute('title') == 'Mute microphone':
            mic.click()
            time.sleep(1)
        btn = DRIVER.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        btn.click()

    post_report_server(classname, entered, timeout)

def main(creds):
    run = True
    global CREDS
    CREDS = creds

    signinlink()
    usercred()
    passcred()
    postcred()
    useapplink()

    timetable = {
        'forms': ['12y-ApC', '12y-DiC'],
        '0': ['12y-ApC', '12C-Fm2', '12C-Fm2', '12A-Ch1', '12y-DiC', '12D-Ph1'],
        '1': ['12y-ApC', '12A-Ch1', '12D-Ph1', '12C-Fm2', '12y-DiC', '12y-Up1'],
        '2': ['12y-ApC', '12C-Fm2', '12B-Ma2', 0, 0, 0],
        '3': ['12y-ApC', '12D-Ph1', '12A-Ch1', '12C-Fm2', '12y-DiC', '12C-Fm2'],
        '4': ['12y-ApC', 0, '12D-Ph1', '12A-Ch1', 0, '12C-Fm2']
    }

    lesson_times = ['0835', '0845', '1015', '1125', '1345', '1420']

    while run:
        if str(time.strftime('%H%M', time.gmtime())) in lesson_times:
            index = lesson_times.index(str(time.strftime('%H%M', time.gmtime())))
            day = str(datetime.datetime.today().weekday())
            accessclass(timetable.get(day)[index])
        else:
            time.sleep(30)

    time.sleep(5)

if __name__ == '__main__':
    main(credentials)