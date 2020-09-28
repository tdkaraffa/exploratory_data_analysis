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
	multi_cat_dataframe = dataframe[[col for col in cat_cols for d in delimiters if
									 (dataframe[col].str.contains(d).any() and col not in open_text_cols)]].copy()
	single_cat_dataframe = dataframe[
		[col for col in cat_cols if col not in multi_cat_dataframe.columns and col not in open_text_cols]].copy()
	num_cat_dataframe = dataframe[num_cols]
	open_text_dataframe = dataframe[open_text_cols]
	return multi_cat_dataframe, single_cat_dataframe, num_cat_dataframe, open_text_dataframe


def multi_cat_encoder(multi_cat_dataframe, delimiters):
	from sklearn.preprocessing import MultiLabelBinarizer
	import pandas as pd
	mlb = MultiLabelBinarizer()
	multi_cat_dataframe.fillna('null', inplace=True)  # temporarily replace nans with 'Null' to allow for encoding
	for column in multi_cat_dataframe:
		for d in delimiters:
			split = multi_cat_dataframe[column].str.split(d)
			group_responses(split)
			data = mlb.fit_transform(split)
			encoded_dataframe = pd.DataFrame(data, columns=[f'{column}: {a}' for a in mlb.classes_])
			encoded_dataframe.index = multi_cat_dataframe.index
			#encoded_dataframe.mask(multi_cat_dataframe[column] == 'null', inplace=True)
			encoded_dataframe.drop([col for col in encoded_dataframe.columns if 'null' in str(col)], inplace=True,
								   axis=1)
			multi_cat_dataframe = pd.concat([multi_cat_dataframe, encoded_dataframe], axis=1)
			multi_cat_dataframe.drop(column, axis=1, inplace=True)
	return multi_cat_dataframe


def one_hot_encoder(single_cat_dataframe):
	from sklearn.preprocessing import OneHotEncoder
	import pandas as pd
	oh = OneHotEncoder(handle_unknown='ignore', sparse=False)
	single_cat_dataframe.fillna('null', inplace=True)
	for column in single_cat_dataframe:
		group_responses(single_cat_dataframe[column])
		data = oh.fit_transform(single_cat_dataframe[column].values.reshape(-1, 1)).astype(int)
		encoded_dataframe = pd.DataFrame(data, columns=[f'{column}: {a}' for a in oh.categories_[0]])
		encoded_dataframe.index = single_cat_dataframe.index
		#encoded_dataframe.mask(single_cat_dataframe[column] == 'null', inplace=True)
		encoded_dataframe.drop([col for col in encoded_dataframe.columns if 'null' in str(col)], inplace=True, axis=1)
		single_cat_dataframe = pd.concat([single_cat_dataframe, encoded_dataframe], axis=1)
		single_cat_dataframe.drop(column, axis=1, inplace=True)
	return single_cat_dataframe

# to do: use mask to drop 'null' from original column, and use drop to remove 'null' columns from encoded_dataframe
# 		and ensure drops from original dataframe are correct (should it be dropping from the encoded? double check
#		output for duplicates
