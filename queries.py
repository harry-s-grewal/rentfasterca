import requests
import time
import os
import pandas as pd

def query_rentfaster(city='Toronto', province='ON'):
    results_df = pd.DataFrame()
    page = 0
    while True:
        location = province.lower() + '/' + city.lower()
        cookies = {'lastcity': location}
        url = 'https://www.rentfaster.ca/api/search.json?cur_page={}'.format(page)
        response = requests.post(url, cookies=cookies, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["listings"] == []:
            if page != 0:
                if os.path.exists(city_name + '.csv'):
                    city_name = city_name + str(city+province)
                results_df.to_csv(city_name + '.csv')
            break
        results_df = results_df.append(pd.DataFrame(data["listings"]))
        city_name = data["listings"][0]["city"]
        page += 1
        time.sleep(10)