import json
import requests
import os
import datetime

startdyn = str(datetime.date.today().replace(day=1))[:10]
next_month = datetime.date.today().replace(day=28) + datetime.timedelta(days=4)
enddyn = str(next_month - datetime.timedelta(days=next_month.day))[:10]
end_last_dyn = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
start_last_dyn = end_last_dyn.replace(day=1)

#startdyn = '2020-05-01'
#enddyn = '2020-05-31'
#start_last_dyn = '2020-06-01'
#end_last_dyn = '2020-06-30'

api_tokens = []

with open("api_tokens.txt", "r") as file:
    for line in file:
        api_tokens.append(line.strip())

base_url = "https://api.customer-alliance.com/statistics/v2/portal-overview.json?"

if os.path.exists("Portal_Data_" + str(startdyn) + "-" + str(enddyn) + ".txt"):
        os.remove("Portal_Data_" + str(startdyn) + "-" + str(enddyn) + ".txt")
else:
    print("No existing actual data file.")

if os.path.exists("Portal_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt"):
        os.remove("Portal_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt")
else:
    print("No existing last month data file.")

def pull_data(api_token):
    headers = {'X-CA-AUTH': api_token}
    api_url = base_url + add_url
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    print(response.headers)
    if response.status_code == 200:
        global data
        data = json.loads(response.text)
        return data

for api_token in api_tokens:
    add_url = "start=" + str(startdyn) + "&end=" + str(enddyn)
    pull_data(api_token)

    portal_names = []

    for key in data['portalStats']:
        portal_names.append(key)
        # print(portal_names)

    for portal_name in portal_names:
        try:
            portal_detail = data['portalStats'][portal_name]
            # print(data['portalStats'][portal_name])
            review_count = (portal_detail['reviewCount'])
            review_rating_weighted = (portal_detail['averageRating']) * review_count
            with open("Portal_Data_" + str(startdyn) + "-" + str(enddyn) + ".txt", "a") as file:
                file.write(str(api_token) + ',' + str(startdyn) + ',' + str(enddyn) + ',' + str(portal_name) + ',' + str(review_count) + ',' + str(review_rating_weighted) + "\n")
            print(str(api_token) + ',' + str(startdyn) + ',' + str(enddyn) + ',' + str(portal_name) + ',' + str(review_count) + ',' + str(review_rating_weighted))
        except KeyError:
            pass

for api_token in api_tokens:
    add_url = "start=" + str(start_last_dyn) + "&end=" + str(end_last_dyn)
    pull_data(api_token)

    portal_names = []

    for key in data['portalStats']:
        portal_names.append(key)
        # print(portal_names)

    for portal_name in portal_names:
        try:
            portal_detail = data['portalStats'][portal_name]
            # print(data['portalStats'][portal_name])
            review_count = (portal_detail['reviewCount'])
            review_rating_weighted = (portal_detail['averageRating']) * review_count
            with open("Portal_Data_" + str(start_last_dyn) + "-" + str(end_last_dyn) + ".txt", "a") as file:
                file.write(str(api_token) + ',' + str(start_last_dyn) + ',' + str(end_last_dyn) + ',' + str(portal_name) + ',' + str(review_count) + ',' + str(review_rating_weighted) + "\n")
            print(str(api_token) + ',' + str(start_last_dyn) + ',' + str(end_last_dyn) + ',' + str(portal_name) + ',' + str(review_count) + ',' + str(review_rating_weighted))
        except KeyError:
            pass