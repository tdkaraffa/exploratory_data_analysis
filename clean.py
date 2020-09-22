def select_dataframe(file_path: str):
	import pandas as pd
	import os
	import numpy as np
	file_extension = os.path.splitext(file_path)

	ignore_cols = ['Shop Number', 'Clients', 'Score', 'StoreNumber', 'StoreName', 'Address', 'City', 'State',
				   'Zip', 'ShopDate', 'TimeIn', 'TimeOut', 'OverallComments']  # add
	# columns
	# to ignore
	# here

	if file_extension == 'csv':
		dataframe = pd.read_csv(file_path)
		dataframe.drop(ignore_cols, inplace=True, axis=1)
		return dataframe
	elif file_extension == 'xlsx' or 'xls':
		dataframe =  pd.read_excel(file_path)
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

def cat_encoder(dataframe):
	from sklearn.preprocessing import MultiLabelBinarizer
	import pandas as pd
	s = (dataframe.dtypes=='object')
	cat_cols = list(s[s].index)
	delimiters = ['; \n']  # or any other character

	open_text_cols = [
	'REST4. Which business-owned, native platforms do you use to place orders from restaurants? (Please separate each with a comma.)',
	'REST5. Which third-party platforms do you use to place orders from restaurants? (Please separate each with a '
	'comma.)',
	'G4. Which business-owned, native platforms do you use to place orders from grocery stores? (Please separate each with a comma.)',
	'G5. Which third-party platforms do you use to place orders from grocery stores? (Please separate each with a '
	'comma.)',
	'RETAIL4. Which business-owned, native platforms do you use to place orders from retail establishments? (Please '
	'separate each with a comma.)',
	'RETAIL5. Which third-party platforms do you use to place orders from retail establishments? (Please separate '
	'each with a comma.)',
	'C4. Which business-owned, native platforms do you use to place orders from convenience stores? (Please separate '
	'each with a comma.)',
	'C5. Which third-party platforms do you use to place orders from convenience stores? (Please separate each with a comma.)'
	]
	multi_cat_cols = [col for col in cat_cols for d in delimiters if
					  (dataframe[col].str.contains(d).any() and col not in open_text_cols)]
	single_cat_cols = [col for col in cat_cols if col not in multi_cat_cols]
	mlb = MultiLabelBinarizer()
	multi_cat_df = df[multi_cat_cols].copy()
	for col in multi_cat_cols:
		# cleaning
		multi_cat_df[col].fillna('Null', inplace=True) # temporarily replace nans with 'Null' to allow for encoding
		for d in delimiters:
			split = multi_cat_df[col].str.split(d)
			group_responses(split)
			data = mlb.fit_transform(split)
			col_names = [f'{col}: {a}' for a in mlb.classes_]
			encoded = pd.DataFrame(data, columns=col_names)
			encoded.mask(multi_cat_df[col]=='Null', inplace=True)
			encoded.drop([col for col in encoded.columns if 'Null' in str(col)], inplace=True, axis=1)
			multi_cat_df = pd.concat([multi_cat_df, encoded], axis=1)
			multi_cat_df.drop(col, axis=1, inplace=True)

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
#main
df = select_dataframe('Input/survey.xlsx')
cat_encoder(df)