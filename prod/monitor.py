import requests
from xml.etree import ElementTree
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from selenium import webdriver

driver = webdriver.Chrome()

#ip addr of cyber q and the page with all the xml data
cyberq = 'http://192.168.1.61/status.xml'
tempPage = 'http://192.168.1.61'

meat_temps = []
pit_temps = []
pit_set_temps = []
meat_set_temps = []

plt.ion()



def getData():
    #render the patches
    red_patch = mpatches.Patch(color='red', label='Pit Temp')
    blue_patch = mpatches.Patch(color='skyblue', label='Internal Temp')
    orange_patch = mpatches.Patch(color='orange', label='Pit Set Temp')
    purple_patch = mpatches.Patch(color='purple',label='Internal Temp Set')
    plt.legend(handles=[red_patch, orange_patch, blue_patch, purple_patch])

    driver.get(tempPage)
    pit_set_temps.append(int(driver.execute_script("return TempHTMLToPIC(document.mainForm._COOK_SET.value)")))
    meat_set_temps.append(int(driver.execute_script("return TempHTMLToPIC(document.mainForm._FOOD1_SET.value)")))
    #get the xml response
    response = requests.get(cyberq)

    #get the time
    x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]

    root = ElementTree.fromstring(response.content)

    for child in root:
        if child.tag == 'COOK_TEMP':
            pit_temps.append(int(child.text)/10)
            print("Cook Temp: ",int(child.text)/10)
        if child.tag == 'FOOD1_TEMP':
            meat_temps.append(int(child.text)/10)
            print("Food Temp: ",int(child.text)/10)


    plt.plot(meat_temps,color='skyblue')
    plt.plot(pit_temps,color='red')
    plt.plot(pit_set_temps,color='orange')
    plt.plot(meat_set_temps,color='purple')
    plt.gcf().autofmt_xdate()
    plt.ylabel('Temp(F)')
    plt.xlabel('Time(Seconds Since Execution)')
    plt.draw()
    plt.pause(1)

while 1:
    try:
        getData()
    except:
        print("Some Exception. Keep going. ")
    time.sleep(1)