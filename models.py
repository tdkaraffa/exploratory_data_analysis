import pickle

full_data = pickle.load(open("full_data.p", "rb"))
single_cat_data = pickle.load(open("single_cat_data.p", "rb"))
multi_cat_data = pickle.load(open("multi_cat_data.p", "rb"))
num_data = pickle.load(open("num_data.p", "rb"))
demo_df = pickle.load(open("demos_data.p", "rb"))

features = demo_df.drop('Overall', axis=1).columns.tolist()
def random_forest(encoded_dataframe):
	pass

