import json
import requests
import os
import time
import datetime

api_tokens = []

with open("api_tokens.txt", "r") as file:
    for line in file:
        api_tokens.append(line.strip())
        #print(api_tokens)

api_url_base = 'https://api.customer-alliance.com/statistics/v2/subcategory-overview.json'

d = ","

#Dynamische Date Range für laufenden und Vormonat
startdyn = str(datetime.date.today().replace(day=1))[:10]
next_month = datetime.date.today().replace(day=28) + datetime.timedelta(days=4)
enddyn = str(next_month - datetime.timedelta(days=next_month.day))[:10]
end_last_dyn = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
start_last_dyn = end_last_dyn.replace(day=1)

#startdyn = '2020-05-01'
#enddyn = '2020-05-31'
#start_last_dyn = '2020-06-01'
#end_last_dyn = '2020-06-30'

print(startdyn)
print(enddyn)
print(start_last_dyn)
print(end_last_dyn)

category = ["average", "price", "service", "room", "break", "clean"]

if os.path.exists("Review_Data_" + startdyn + "-" + enddyn + ".txt"):
        os.remove("Review_Data_" + startdyn + "-" + enddyn + ".txt")
else:
    print("No existing actual data file.")

if os.path.exists("Review_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt"):
        os.remove("Review_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt")
else:
    print("No existing last month data file.")

def pull_data(api_token):
    headers = {'X-CA-AUTH': api_token}
    api_url = api_url_base + api_url_add
    global response
    response = requests.get(api_url, headers=headers)
    return response

counter = 0
error_counter1 = 0
error_list1 = []
for api_token in api_tokens:
    for cat in category:
        api_url_add = '?start=' + startdyn + '&end=' + enddyn + '&category=' + cat

        if counter == 30:
            time.sleep(15)
            counter = 0
        pull_data(api_token)
        counter = counter + 1
        print(counter)
        print(response.headers)
        print(response.content)
        if response.status_code == 200:
            data = json.loads(response.text)
            print(api_token)

            review_count = data["reviewCount"]
            rating_value = data["averageRating"]

            with open("Review_Data_" + startdyn + "-" + enddyn + ".txt", "a") as file:
                file.write(api_token + d + cat + d + startdyn + d + enddyn + d + str(review_count) + d + str(rating_value) + "\n")
                print(api_token + d + cat + d + startdyn + d + enddyn + d + str(review_count) + d + str(rating_value))
        else:
            error_counter1 = error_counter1 + 1
            error_list1.append(response.status_code)
            print(api_token)

counter = 0
error_counter2 = 0
error_list2 = []
for api_token in api_tokens:
    for cat in category:
        api_url_add = '?start=' + str(start_last_dyn) + '&end=' + str(end_last_dyn) + '&category=' + cat

        if counter == 30:
            time.sleep(15)
            counter = 0
        pull_data(api_token)
        counter = counter + 1
        print(counter)
        print(response.headers)
        print(response.content)
        if response.status_code == 200:
            data = json.loads(response.text)
            #print(api_token)

            review_count = data["reviewCount"]
            rating_value = data["averageRating"]

            with open("Review_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt", "a") as file:
                file.write(api_token + d + cat + d + str(start_last_dyn) + d + str(end_last_dyn) + d + str(review_count) + d + str(rating_value) + "\n")
                print(api_token + d + cat + d + str(start_last_dyn) + d + str(end_last_dyn) + d + str(review_count) + d + str(rating_value))
        else:
            error_counter2 = error_counter2 + 1
            error_list2.append(response.status_code)


print("Update abgeschlossen")
print("Count of error actual month: " + str(error_counter1))
print(error_list1)
print("Count of error previous month: " + str(error_counter2))
print(error_list2)

