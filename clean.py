def select_dataframe(file_path: str, ignore_cols):
	import pandas as pd
	import os
	import numpy as np
	file_extension = os.path.splitext(file_path)
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


def group_responses(series, words_to_combine_on):  # user-specified
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


def cat_encoder(cat_dataframe, model, model_label_term, d=None, combine=None):  # combines the above two
	# functions into one
	# cat_data_frame: section of main dataframe to encode
	# model: predetermined sklearn model
	# model_label_term: model-specific parameter to obtain encoded labels
	# d: optional list of delimiters
	# combine: optional list of words with which to combine similar responses
	import pandas as pd
	import numpy as np
	working_dataframe = cat_dataframe.fillna('null')  # temporarily replace NA with 'null' as needed for encoding
	final_data = np.array(np.arange(len(working_dataframe))).reshape(-1, 1)  # initialize array/list for later
	# appending
	final_columns = ['index']
	# iterate through columns, encoding data and collecting column names, and ensuring missing values are accounted for
	for column in working_dataframe:
		if d:  # only execute this loop if delimiters are specified, only for multi-cat
			for d in d:
				split = working_dataframe[column].str.split(d)
		else:  # otherwise, reshape data for model
			split = working_dataframe[column].values.reshape(-1, 1)
		if combine:
			group_responses(split, combine)  # groups similar responses, like those containing "Other" or "N/A"
		data = model.fit_transform(split)
		labels = getattr(model, model_label_term)  # get categories/classes from model to label encoded data
		if len(labels) == 1:  # handles single cat columns, because of how categories_ method of OneHotEncoder returns
			labels = labels[0]
		encoded_columns = [f'{column}: {a}' for a in labels]
		mask = working_dataframe[column] != 'null'
		encoded_data = [row if m else [np.nan] * len(row) for row, m in zip(data, mask)]
		# undo insertion of 'null' placeholders to keep missing values that are intentionally blank
		try:
			null_index = list(labels).index('null')
			encoded_data = np.delete(encoded_data, null_index, axis=1)
			del encoded_columns[null_index]
		except ValueError:
			pass
		# append newly encoded data to pre-existing arrays
		final_data = np.append(final_data, encoded_data, axis=1)
		final_columns = np.append(final_columns, encoded_columns)
	# return all encoded data in a single dataframe
	return pd.DataFrame(data=final_data, columns=final_columns)
