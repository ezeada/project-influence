from collections import defaultdict
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt


# Personal File System (pwd your Datasets in Terminal)
# path = "/mnt/c/Git/project-influence/Language_Model_Responses/Arman_BATCH_1.csv"

def loadBatch(path_to_csv, count_dict, prob_list, shot):
    df = pd.read_csv(path_to_csv)

    for index, row in df.iterrows():
        rslt = []
        country = [row[1]]
        if 'Sierra_Leone' in country:
            country.append('Sierra')
        if row[2] in country:
            rslt = [row[1], shot, row[3]]
        else:
            for i in range(2, 10):
                if row[2 * i] in country:
                    rslt = [row[1], shot, row[(2 * i) + 1]]
        if len(rslt) == 0:
            rslt = [row[1], shot, 0.0]
        prob_list.append(rslt)

    for country in count_dict:
        df_country = df[df['Given Country'] == country]

        num_follow_pattern = len(df_country[df_country['Completion 1'] == country])
        if country == 'Sierra_Leone':
            num_follow_pattern += len(df_country[df_country['Completion 1'] == 'Sierra'])

        # count_dict[country][1] += num_follow_pattern
        num_total = len(df_country)
        count_dict[country][2] += num_total

        num_deviates = num_total - num_follow_pattern
        count_dict[country][1] += num_deviates



def graphFunc():
    # num_shots = ['One', 'Two', 'Three', 'Four', 'Five']
    num_shots = ['One', 'Two', 'Three', 'Four']
    counts = []
    probs = []
    count = 0
    for shot in num_shots:

        directory = f"Language_Model_Responses/{shot}_Shot_Data/"
        pathlist = Path(directory).rglob('*.csv')
        for path in pathlist:
            count_dict = {'France': ['France', 0, 0], 'India': ['India', 0, 0], 'Sierra_Leone': ['Sierra_Leone', 0, 0],
                          'Singapore': ['Singapore', 0, 0], 'USA': ['USA', 0, 0]}
            # because path is object not string
            path_in_str = str(path)
            loadBatch(path_in_str, count_dict, probs, shot)
            result = [[country, shot, count_dict[country][1] / count_dict[country][2]] for country in count_dict]
            counts.extend(result)
    column_names = ['Country', 'Shots', 'Percentage Deviations']
    print(len(counts))
    print(len(probs))
    df = pd.DataFrame(counts, columns=column_names)
    g = sns.catplot(x="Shots",
                    y="Percentage Deviations",
                    kind="bar",
                    capsize=0.05,
                    col="Country",
                    data=df)
    plt.xlabel("Shots")
    plt.ylabel("Percentage Deviations")
    plt.show()
    df.to_csv(f'Analytics/Deviations.csv')

    column_names2 = ['Country', 'Shots', 'Probability']
    df2 = pd.DataFrame(probs, columns=column_names2)
    graph = sns.catplot(x="Shots",
                        y="Probability",
                        kind="bar",
                        capsize=0.05,
                        col="Country",
                        data=df2)
    plt.xlabel("Number of Shots")
    plt.ylabel("Probabilities")
    plt.show()
    df2.to_csv(f'Analytics/Probabilities.csv')


if __name__ == "__main__":
    graphFunc()
