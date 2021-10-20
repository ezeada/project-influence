
import requests
import pandas as pd
import json

res = requests.post("https://api.ai21.com/studio/v1/j1-jumbo/complete", 
headers={"Authorization" : "Bearer ZPtVIXs3vcoKAd85YI5OSRlqJOtSfIpU"},
json={
    "prompt" : "Input: Alex \n Name: Alex \n Country: USA \n Input: Jawi \n Name: Jawi \n Country: USA \n Input: Arman \n Name: Arman \n Country: ",
    "numResults" : 1,
    "maxTokens" : 10,
    # Higher temperature means greater sampling
    # temperature = 0 means, output the value with the highest probability
    "temperature" : 0
})



data = res.json()
completions = data["completions"][0]
id = data["id"]

with open('GeneratedData/data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

with open('GeneratedData/completions.json', 'w') as f:
    json.dump(completions, f, ensure_ascii=False)

print(id)
print(completions["data"]["text"])
