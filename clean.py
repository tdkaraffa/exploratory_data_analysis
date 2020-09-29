def select_dataframe(file_path: str, ignore_cols):
	import pandas as pd
	import os
	import numpy as np
	file_extension = os.path.splitext(file_path)
	# add
	# columns
	# to ignore
	# here
	if file_extension == 'csv':
		dataframe = pd.read_csv(file_path)
		dataframe.drop(ignore_cols, inplace=True, axis=1)
		return dataframe
	elif file_extension == 'xlsx' or 'xls':
		dataframe = pd.read_excel(file_path)
		dataframe.drop(ignore_cols, inplace=True, axis=1)
		return dataframe
	else:
		return 'use excel or csv'


def group_responses(series):
	words_to_combine_on = ['N/A', 'Other']
	for word in words_to_combine_on:
		for row in series:
			if type(row) == list:
				for i, e in enumerate(row):
					if word in row[i]:
						row[i] = word
			elif type(row) == str:
				if word in row:
					row = word


def group_cols_by_type(dataframe, delimiters, open_text_cols):
	s = (dataframe.dtypes == 'object')
	cat_cols = list(s[s].index)
	n = (dataframe.dtypes == 'number')
	num_cols = list(n[n].index)
	multi_cat_cols = [col for col in cat_cols for d in delimiters if
					  (dataframe[col].str.contains(d).any() and col not in open_text_cols)]
	single_cat_cols = [col for col in cat_cols if col not in multi_cat_cols and col not in open_text_cols]
	return multi_cat_cols, single_cat_cols, num_cols, open_text_cols


def multi_cat_encoder(multi_cat_dataframe, delimiters):
	from sklearn.preprocessing import MultiLabelBinarizer
	import pandas as pd
	import numpy as np
	mlb = MultiLabelBinarizer()
	working_dataframe = multi_cat_dataframe.fillna('null')  # temporarily replace nans with 'Null' to allow for
	# encoding
	final_data = np.array(np.arange(len(working_dataframe))).reshape(-1, 1)
	final_columns = ['index']
	for d in delimiters:
		for column in working_dataframe:
			split = working_dataframe[column].str.split(d)
			group_responses(split)
			data = mlb.fit_transform(split)
			encoded_columns = [f'{column}: {a}' for a in mlb.classes_]
			mask = working_dataframe[column] != 'null'
			encoded_data = [row if m else [np.nan] * len(row) for row, m in zip(data, mask)]
			try:
				null_index = list(mlb.classes_).index('null')
				encoded_data = np.delete(encoded_data, null_index, axis=1)
				del encoded_columns[null_index]
			except ValueError:
				pass
			final_data = np.append(final_data, encoded_data, axis=1)
			final_columns = np.append(final_columns, encoded_columns)
	final_dataframe = pd.DataFrame(data=final_data, columns=final_columns)
	return final_dataframe


def one_hot_encoder(single_cat_dataframe):
	from sklearn.preprocessing import OneHotEncoder
	import pandas as pd
	import numpy as np
	oh = OneHotEncoder(handle_unknown='ignore', sparse=False)
	working_dataframe = single_cat_dataframe.fillna('null')
	final_data = np.array(np.arange(len(working_dataframe))).reshape(-1, 1)
	final_columns = ['index']
	for column in working_dataframe:
		group_responses(working_dataframe[column])
		data = oh.fit_transform(working_dataframe[column].values.reshape(-1, 1)).astype(int)
		encoded_columns = [f'{column}: {a}' for a in oh.categories_[0]]
		mask = working_dataframe[column] != 'null'
		encoded_data = [row if m else [np.nan] * len(row) for row, m in zip(data, mask)]
		try:
			null_index = list(oh.categories_[0]).index('null')
			encoded_data = np.delete(encoded_data, null_index, axis=1)
			del encoded_columns[null_index]
		except ValueError:
			pass
		final_data = np.append(final_data, encoded_data, axis=1)
		final_columns = np.append(final_columns, encoded_columns)
	final_dataframe = pd.DataFrame(data=final_data, columns=final_columns)
	return final_dataframe

#to do
# any cleaning for numerical columns
# potentially combine mlb & oh encoders into one function, or at least a mojority of them into one
# 	with the dataframe, model, and columns (oh.categories_[0] and mlb.classes_) passed into the function