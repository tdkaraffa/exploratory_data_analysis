# ---------------------------------------------------------#
# load data for working, delete this block eventually
import pickle

full_data = pickle.load(open("full_data.p", "rb"))
single_cat_data = pickle.load(open("single_cat_data.p", "rb"))
multi_cat_data = pickle.load(open("multi_cat_data.p", "rb"))
num_data = pickle.load(open("num_data.p", "rb"))
demo_df = pickle.load(open("demos_data.p", "rb"))
# ---------------------------------------------------------#



def visualize(dataframe, demographics):
	import matplotlib.pyplot as plt
	import seaborn as sns
	import pandas as pd
	import numpy as np
	
	prefixes = np.unique([string.split(':', 1)[0] for string in dataframe.columns])
	data_groups = {prefix: [question for question in dataframe.columns if prefix == question.split(':', 1)[0]] for
				   prefix in prefixes}
	working_dataframe = pd.concat([demographics, dataframe], axis=1)
	for question_key in data_groups:
		pre_formatting()
		fig, axes = plt.subplots(1, len(demographics.columns), figsize=(50, 30), sharey=True, sharex=True,
								 constrained_layout=True)
		for i, demo_col in enumerate(demographics.columns):
			transposed = working_dataframe.groupby(demo_col)[data_groups[question_key]].mean().T
			transposed.plot.barh(ax=axes[i])
		post_formatting(fig, axes, question_key, demographics.columns)
		plt.show()

def pre_formatting():
	import seaborn as sns
	sns.set_palette('tab20c')
	sns.set_style({'font.family': ['sans-serif'], 'font.sans-serif': ['Liberation Sans']})

def post_formatting(fig, axes, question_key, columns):
	import matplotlib.pyplot as plt
	import seaborn as sns
	from textwrap import wrap
	labels = [label.get_text().split(': ', 1)[1] for label in axes[0].get_yticklabels()]
	labels = ["\n".join(wrap(label, 20)) for label in labels]
	axes[0].set_yticklabels(labels)
	fig.suptitle(question_key)
	for axis, column in zip(fig.axes, columns):
		axis.set_title(column)
	for axis in fig.axes:
		axis.tick_params(axis='both', length=0)
		axis.invert_yaxis()
		sns.despine(bottom=True, right=True, top=True)
		axis.legend(loc='lower right')
		axis.tick_params(axis='both', length=0)
		for p in axis.patches:
			axis.text(s="{:.1%}".format(
				p.get_width()),
				y=p.get_y() + (p.get_height() / 2),
				x=max(.03, p.get_width() / 2 + p.get_x()),
				color='black', ha='center', va='center', weight='bold')

visualize(multi_cat_data, demo_df)
