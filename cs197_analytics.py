from collections import defaultdict
import pandas as pd
import numpy as np


#Personal File System (pwd your Datasets in Terminal)
#path = "/mnt/c/Git/project-influence/Language_Model_Responses/Arman_BATCH_1.csv"

def loadBatch(path_to_csv):
    df = pd.read_csv(path_to_csv)
    country_data = defaultdict(float)
    lst_countries = ['France', 'India', 'Sierra_Leone', 'Singapore', 'USA']

    for country in lst_countries:
        print(f"Calculating for {country}")
        df_country = df[df['Given_Country'] == country]
 
        num_correct_guess = len(df_country[df_country['Response'] == df_country['Real_Country']])

        num_deviates = len(df_country[df_country['Response'] != df_country['Given_Country']])

        num_total = len(df_country)
        
        #country_data[country] = [num_total, num_deviates, num_correct_guess]
        
        print(f"For {country} in this batch -- Total: {num_total}, Number of Deviations: {num_deviates}, Number of Correct Guesses: {num_correct_guess} \n")


def testFunc():
    for i in range(1, 6):
        print(f"Calculating for Batch {i}")
        path = f"/mnt/c/Git/project-influence/Language_Model_Responses/Arman_BATCH_{i}.csv"
        loadBatch(path)
    
if __name__ == "__main__":
    testFunc()