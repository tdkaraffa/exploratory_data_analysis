def main():
	from clean import select_dataframe, choose_demographics, group_cols_by_type, cat_encoder
	from visualizations import visualize
	import pandas as pd
	from sklearn.preprocessing import OneHotEncoder
	from sklearn.preprocessing import MultiLabelBinarizer

	# -------------------------------------------------------------------------------------------------------------------- #
	# USER-SPECIFIED INPUTS
	file = 'Input/survey.xlsx'
	columns_to_ignore = ['Shop Number', 'Clients', 'Score', 'StoreNumber', 'StoreName', 'Address', 'City', 'State',
						 'Zip', 'ShopDate', 'TimeIn', 'TimeOut', 'OverallComments']
	delimiters = ['; \n']  # user-specified
	open_text_cols = ['Q50', 'Q51', 'Q91', 'Q92', 'Q132', 'Q133', 'Q173', 'Q174']  # user-specified
	words_to_combine_on = ['N/A', 'Other']  # user-specified
	demographics_columns = ['Q2', 'Q3', 'Q4']
	# -------------------------------------------------------------------------------------------------------------------- #

	dataframe = select_dataframe(file, columns_to_ignore)
	demographics_df = choose_demographics(dataframe, demographics_columns)
	multi_cat_cols, single_cat_cols, num_cat_cols, open_text_cols = group_cols_by_type(dataframe, delimiters,
																					   open_text_cols)
	multi_cat_model = MultiLabelBinarizer()  # define model used to encode
	multi_cat_label_term = 'classes_'  # specify the parameter to obtain encoded labels
	single_cat_model = OneHotEncoder(handle_unknown='ignore', sparse=False)  # define model used to encode
	single_cat_label_term = 'categories_'  # specify the parameter to obtain encoded labels

	multi_cat_encoded_df = cat_encoder(dataframe[multi_cat_cols], multi_cat_model, multi_cat_label_term,
									   delimiters=delimiters, combine=words_to_combine_on)
	single_cat_encoded_df = cat_encoder(dataframe[single_cat_cols], single_cat_model, single_cat_label_term,
										combine=words_to_combine_on)
	num_cat_df = dataframe[num_cat_cols].copy()
	open_text_df = dataframe[open_text_cols]
	full_dataframe = pd.concat([multi_cat_encoded_df, single_cat_encoded_df, num_cat_df])

	visualize(multi_cat_encoded_df, demographics_df)
	visualize(single_cat_encoded_df, demographics_df)

	import pickle
	pickle.dump(full_dataframe, open("full_data.p", "wb"))
	pickle.dump(multi_cat_encoded_df, open("multi_cat_data.p", "wb"))
	pickle.dump(single_cat_encoded_df, open("single_cat_data.p", "wb"))
	pickle.dump(num_cat_df, open("num_data.p", "wb"))
	pickle.dump(demographics_df, open("demos_data.p", "wb"))

if __name__ == "__main__":
	main()
