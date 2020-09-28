
from clean import select_dataframe, group_cols_by_type, multi_cat_encoder, one_hot_encoder
# main


columns_to_ignore = ['Shop Number', 'Clients', 'Score', 'StoreNumber', 'StoreName', 'Address', 'City', 'State', 'Zip',
				   'ShopDate', 'TimeIn', 'TimeOut', 'OverallComments']

dataframe = select_dataframe('Input/survey.xlsx', columns_to_ignore)

delimiters = ['; \n'] # user-specified
open_text_cols = ['Q50', 'Q51', 'Q91', 'Q92', 'Q132', 'Q133', 'Q173', 'Q174'] # user-specified

multi_cat_df, single_cat_df, num_cat_df, open_text_df = group_cols_by_type(dataframe, delimiters, open_text_cols)

multi_cat_encoder(multi_cat_df, delimiters)
one_hot_encoder(single_cat_df)

