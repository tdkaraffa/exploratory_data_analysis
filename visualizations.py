# create basic visualizations for categorical data
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
		fig, axes = plt.subplots(1, len(demographics.columns), figsize=(40, 16), sharey=True, sharex=True,
								 constrained_layout=True)
		for i, demo_col in enumerate(demographics.columns):
			transposed = working_dataframe.groupby(demo_col)[data_groups[question_key]].mean().T
			transposed.plot.barh(ax=axes[i])
		post_formatting(fig, axes, question_key, data_groups, demographics.columns)
		save_chart(fig)
		plt.close()

# function for saving charts to Output folder
def save_chart(chart):
	import os
	title = chart._suptitle.get_text()
	filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
	os.makedirs(os.path.join('Output', 'Visualizations'), exist_ok=True)
	chart.savefig(os.path.join('Output', 'Visualizations', filename))

# mild pre-formatting to set style for figures
def pre_formatting():
	import seaborn as sns
	sns.set_palette('tab20c')
	sns.set_style({'font.family': ['sans-serif'], 'font.sans-serif': ['Liberation Sans']})

# gratuitous formatting for matplotlib figures
def post_formatting(fig, axes, question_key, data_groups, columns):
	import matplotlib.pyplot as plt
	import seaborn as sns
	from textwrap import wrap
	size = 25 - (min(len(data_groups[question_key]) ** 2 - 9, 7)) # set universal fontsize
	labels = [label.get_text().split(': ', 1)[1] for label in axes[0].get_yticklabels()]
	labels = ["\n".join(wrap(label, 20)) for label in labels] # format labels for bars
	axes[0].set_yticklabels(labels, fontsize=size)
	fig.suptitle(question_key, fontsize=size*1.5)
	for axis, column in zip(fig.axes, columns):
		axis.set_title(column, fontsize=size*1.25)
	for axis in fig.axes:
		# clean up tick marks, etc.
		axis.tick_params(axis='both', length=0)
		sns.despine(bottom=True, right=True, top=True)
		axis.legend(loc='lower right', fontsize=size)
		axis.tick_params(axis='both', length=0)
		for p in axis.patches: # add data labels to bars
			axis.text(s="{:.1%}".format(
				p.get_width()),
				y=p.get_y() + (p.get_height() / 2), fontsize=size,
				x=max(.05, p.get_width() / 2 + p.get_x()),
				color='black', ha='center', va='center', weight='bold')

