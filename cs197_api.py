
import requests


res = requests.post("https://api.ai21.com/studio/v1/j1-large/complete", 
headers={"Authorization" : "ZPtVIXs3vcoKAd85YI5OSRlqJOtSfIpU"},
json={
    "prompt" : "Complete with prompt...",
    "numResults" : 1,
    "maxTokens" : 5,
    "stopSequences" : ["."],
    "topKReturn" : 0,
    "temperature" : 0.3
})

assert res.status_code == 200

data = res.json()

## Depends on if we're using DataFrame with pandas or just 
# raw excel maniupulation for this week



