from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymsteams
import json
import random
import time
import schedule

# To give the webpage time to load, as my internet is slow.
pageRefreshTime = 30
counter = 0

# The send_message function uses pymsteams and notifies a certain group of the forum question
def send_message(topic, link, person, mslink, test=True, messenger="msteams"):
    if "m" in messenger:
        myTeamsMessage = pymsteams.connectorcard(mslink)
        myTeamsMessage.text("New Question: '" + topic + "' Assigned to:" + person + " At: " + link)
        if test:
            myTeamsMessage.printme()
        else:
            myTeamsMessage.send()
    elif "s" in messenger:
        print()

# Main function for checking webpage
def check(webpage, driver, people, mslink, sendmessage=False):
    global counter
    num_people = len(people)
    webid = webpage.split('=')[1]
    time.sleep(5)
    data = {}

    # Reads file to see whether or not the forum discussion has been seen before and therefor is not 'new'
    try:
        with open('data_' + webid + '.txt') as j_file:
            data = json.load(j_file)
    except FileNotFoundError:
        data = {}

    # The forum website is structured with a discussion element being a tablet and each
    # topic/question posted becomes a row of that table. elems references the entire table.
    elems = driver.find_elements_by_class_name('discussion')
    newData = {}

    # For each discussion in the discussions table
    for elem in elems:
        # Get the data (td) from each table row
        tds = elem.find_elements_by_tag_name('td')
        replies = 0
        topic = ""
        href = ""

        # Three pieces of data in the table row that are important, the topic name, its
        # hyperlink to the discussion, and the amount of replies (to see whether or not the
        # question has been tended to).
        for index, td in enumerate(tds):
            if index == 1:
                topic = td.text
                href = td.find_element_by_tag_name('a').get_attribute('href')
            if index == 3:
                replies = int(td.text)
        if href is not None:
            if "discuss" in href:
                splits = href.split('=')
                idNum = splits[len(splits) - 1]
                # Never seen before
                if data.get(idNum) is None:
                    # No replies yet
                    if replies == 0:
                        print(time.ctime(), webid, "New topic with no replies!", elem.text)
                        data[idNum] = {
                            'topic': elem.text,
                            'link': href,
                            'assigned': people[counter % num_people]
                        }
                        counter += 1
                        newData[idNum] = data[idNum]

                    # There are replies, don't notify, but take note
                    else:
                        print(time.ctime(), webid, "New topic with replies!\n", elem.text)
                        data[idNum] = {
                            'topic': elem.text,
                            'link': href,
                            'assigned': "Resolved"
                        }

    if newData == {}:
        print(time.ctime(), webid, "No new data")
    else:
        with open('data_' + webid + '.txt', 'w') as j_file:
            json.dump(data, j_file)

    for dat in newData:
        send_message(newData[dat]['topic'], newData[dat]['link'], newData[dat]['assigned'], mslink)

    if sendmessage:
        for dat in newData:
            send_message(newData[dat]['topic'], newData[dat]['link'], newData[dat]['assigned'], mslink, test=False)
        

with open('config' + '.json', "r") as json_file:
    data = json.load(json_file)

people = data["assignees"]
num_people = len(people)
temp = people
random.shuffle(temp)
people = temp

forums = data["forums"]
mslink = data["msteams"]

assert mslink != ""
assert len(forums) > 0
if len(people) == 0:
    people.append("Anyone")

everyT = input("Run every X minutes [10]:")
if everyT == "":
    everyT = 10
else:
    everyT = int(everyT)

uname = input("Username:")
pwd = input("Password:")

driver = webdriver.Firefox()
driver.get(forums[0])

assert "Stellenbosch" in driver.title
username = driver.find_element_by_name("username")
username.clear()
username.send_keys(uname)

password = driver.find_element_by_name("password")
password.clear()
password.send_keys(pwd)

password.send_keys(Keys.RETURN)

time.sleep(5)

def checker():
    for i in range(len(forums)):
        webpage = forums[i]
        driver.get(webpage)
        check(webpage, driver, people, mslink, True)
        time.sleep(pageRefreshTime)

schedule.every(everyT).minutes.do(checker)

checker()
while 1:
    schedule.run_pending()
    time.sleep(1)

driver.quit()