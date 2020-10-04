#---------------------------------------------------------#
#load data for working, delete this block eventually
import pickle
full_data = pickle.load(open("full_data.p", "rb"))
single_cat_data = pickle.load(open("single_cat_data.p", "rb"))
multi_cat_data = pickle.load(open("multi_cat_data.p", "rb"))
num_data = pickle.load(open("num_data.p", "rb"))
demo_df = pickle.load(open("demos_data.p", "rb"))
# end delete block
#---------------------------------------------------------#


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_style('whitegrid')
def visualize(dataframe, demographics):
	prefixes = np.unique([string.split(':', 1)[0] for string in dataframe.columns])
	data_groups = {prefix: [question for question in dataframe.columns if prefix==question.split(':', 1)[0]]
				   for prefix in prefixes}

	working_dataframe = pd.concat([demographics, dataframe], axis=1)

	for question_key in data_groups:
		fig, axes = plt.subplots(1, len(demographics.columns), figsize=(50, 30), sharey=True, sharex=True,
								 constrained_layout=True)
		for i, demo_col in enumerate(demographics.columns):
			chart = working_dataframe.groupby(demo_col)[data_groups[question_key]].mean().T.plot.barh(ax=axes[i])
		labels = [label.get_text().split(': ', 1)[1] for label in axes[0].get_yticklabels()]
		axes[0].set_yticklabels(labels)
		fig.suptitle(question_key)
		plt.show()
visualize(multi_cat_data, demo_df)