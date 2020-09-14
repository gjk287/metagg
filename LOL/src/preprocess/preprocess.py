class Preprocess(object):
	def __init__(self, original_df):
		self.original_df = original_df
		self.preprocessed_df = None
		self.date_range = [-1, 0, 1]
