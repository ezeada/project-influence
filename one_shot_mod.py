# Makes a POST request to the API, return a json file under GeneratedData, can be modified later with pandas library
# where the completions are suitable to place in a DataFrame. 
#
#   TODO 1: Generate a randomize prompt generator from the database created by @carolyn ++
#   TODO 2: Implement a database to hold the data generated by this API ~
#   TODO 3: Automate the requests by running it along the background ++
# ADAEZE: Modified to be in order of country

import requests
import pandas as pd
import json
import time
import random 
import numpy as np

# to keep track of which country we're on
name_Number = 0

#to keep track of number for debugging
debug_count = 0

# number of times language model deviates
deviations = 0

#Personal File System (pwd your Datasets in Terminal)
#path = "/mnt/c/Git/project-influence/Datasets/France.xlsx"

def queryAPI(prompt):
    res = requests.post("https://api.ai21.com/studio/v1/j1-jumbo/complete", 
    headers={"Authorization" : "Bearer ZPtVIXs3vcoKAd85YI5OSRlqJOtSfIpU"},
    json={
        "prompt" : prompt,
        "numResults" : 1,
        "maxTokens" : 1,
        "topKReturn" : 10,
        # Higher temperature means greater sampling
        # temperature = 0 means, output the value with the highest probability
        "temperature" : 0
    })

    data = res.json()
    tokens = [t['generatedToken']['token'] for t in data['completions'][0]['data']['tokens']]
    response = ''.join(tokens).replace("<|newline|>", '\n').replace('_', ' ')
    probability = data["completions"][0]['data']['tokens'][0]['generatedToken']['logprob']
    
    id = data["id"]
    
    print(prompt)
    print(response)
    print(np.exp(probability))
    #print(id)

    #response is in the form '_response'
    return(response[1:], probability)

    #with open('Language_Model_Responses/data.json', 'w') as f:
    #    json.dump(data, f, ensure_ascii=False)

    #with open('Language_Model_Responses/completions.json', 'w') as f:
    #    json.dump(completions, f, ensure_ascii=False)

def loadData(country_name, isAll=False):
    if isAll:
        lst_dfs = []
        lst_countries = ['France', 'India', 'Sierra_Leone', 'Singapore', 'USA']
        for country in lst_countries:
            df = pd.read_excel(f"Datasets/{country}.xlsx", usecols='A,B')
            lst_dfs.append(df.assign(Country = country))
        return pd.concat(lst_dfs)

    else:
        path = f"Datasets/{country_name}.xlsx"
        return pd.read_excel(path, usecols='A,B') 

def sampleFromData(country_name):
    lst_data = []
    df_country = loadData(country_name)
    df_all = loadData(country_name, True)
    train_name = df_country.sample(replace=True)['Name'].values[0]
    lst_data.append((train_name, country_name))
    test_data = df_all.sample(replace=True)
    lst_data.append((test_data['Name'].values[0], test_data['Country'].values[0]))
    return lst_data

def dataCollection(country_name, result_lst):
    lst_train = sampleFromData(country_name)
    #One-shot Learning
    prompt = createPrompt_1(lst_train[0][0], lst_train[0][1], lst_train[1][0])
    test_country = lst_train[1][1]    
    train_country = lst_train[0][1]
    (response, probability) = queryAPI(prompt)
    global debug_count 
    debug_count+= 1
    print(debug_count)

    if (train_country != response):
        global deviations
        deviations += 1
    #Tuples of ('Given Country', 'Response', 'Real Country', and 'Probability')
    result_lst.append((train_country, response, test_country, np.exp(probability)))

def createPrompt_1(train_name1, train_country1, test_name):
    prompt = f'''Input: {train_name1}
    Name: {train_name1}
    Country: {train_country1}

    Input: {test_name}
    Name: {test_name}
    Country:'''
    return prompt


# def testFunc():
#     dataCollection('USA', 1)

if __name__ == "__main__":
    BATCH_SIZE = 100
    ITERATION = 1
    lst_countries = ['France', 'India', 'Sierra_Leone', 'Singapore', 'USA']
    
    while(True):
        result_lst = []
        
        for i in range(BATCH_SIZE):
            dataCollection(lst_countries[name_Number], result_lst)
            time.sleep(3)
        print(lst_countries[name_Number] + ' Deviations: ' + str(deviations))
        name_Number += 1
        df = pd.DataFrame(result_lst, columns=['Given_Country', 'Response', 'Real_Country', 'Probability'])
        df.to_csv(f'Language_Model_Responses/Adaeze_BATCH_{ITERATION}.csv')
        print(f"Completed Iteration: {ITERATION}")
        ITERATION += 1