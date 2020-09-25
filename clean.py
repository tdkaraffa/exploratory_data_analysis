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
			for i, e in enumerate(row):
				if word in row[i]:
					row[i] = word


def group_cols_by_type(dataframe, delimiters, open_text_cols):
	s = (dataframe.dtypes == 'object')
	cat_cols = list(s[s].index)
	n = (dataframe.dtypes == 'number')
	num_cols = list(n[n].index)
	multi_cat_dataframe = dataframe[[col for col in cat_cols for d in delimiters if
									 (dataframe[col].str.contains(d).any() and col not in open_text_cols)]].copy()
	single_cat_dataframe = dataframe[[col for col in cat_cols if col not in multi_cat_dataframe.columns]].copy()
	num_cat_dataframe = dataframe[num_cols]
	open_text_dataframe = dataframe[open_text_cols]
	return multi_cat_dataframe, single_cat_dataframe, num_cat_dataframe, open_text_dataframe


def multi_cat_encoder(multi_cat_dataframe, delimiters):
	from sklearn.preprocessing import MultiLabelBinarizer
	import pandas as pd
	mlb = MultiLabelBinarizer()
	from sklearn.pipeline import Pipeline
	multi_cat_dataframe.fillna('null', inplace=True)  # temporarily replace nans with 'Null' to allow for encoding
	for col in multi_cat_dataframe:
		for d in delimiters:
			split = multi_cat_dataframe[col].str.split(d)
			group_responses(split)
			data = mlb.fit_transform(split)
			col_names = [f'{col}: {a}' for a in mlb.classes_]
			encoded = pd.DataFrame(data, columns=col_names)
			print(encoded.sum())
			encoded.mask(multi_cat_dataframe[col] == 'null', inplace=True)
			print(encoded.sum())
			encoded.drop([col for col in encoded.columns if 'null' in str(col)], inplace=True, axis=1)
			print(encoded.sum())
			multi_cat_dataframe = pd.concat([multi_cat_dataframe, encoded], axis=1)
			multi_cat_dataframe.drop(col, axis=1, inplace=True)
	return multi_cat_dataframe

	# start here
	'''single_cat_cols = [col for col in dataframe.columns if col not in cat_cols_and_responses.keys()]
	from sklearn.preprocessing import OneHotEncoder
	oh_encoder = OneHotEncoder(handle_unknown='ignore', sparse=True)
	oh_cols = pd.DataFrame(oh_encoder.fit_transform(df[single_cat_cols]))
	oh_cols.index = df[single_cat_cols].index
	df.drop(single_cat_cols, inplace=True, axis=1)
	pd.concat([df, oh_cols], axis=1)
	print(df)'''


from sklearn.pipeline import Pipeline
