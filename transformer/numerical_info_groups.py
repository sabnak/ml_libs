from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from sklearn.feature_extraction import DictVectorizer


class NumericalIntoGroupsSplitter(BaseEstimator, TransformerMixin):
	"""Transform any numeric data into given n_groups
	Groups indices start with 1
	If expand_x is True, then original X will be expanded, otherwise - replaced

	Parameters
	----------
	n_groups : int
			Quantity of groups to split
	expand_X : bool, optional
			Expand or replace original X

	Attributes
	----------
	self.groups_ : list
			A list mapping feature groups to feature indices

	Examples
	--------
	>>> from mllib.transformer import NumericalIntoGroupsSplitter

	>>> a = np.random.randint(1, 100, (5, 2))
	>>> t = NumericalIntoGroupsSplitter(3)

	>>> t.fit(a)
	>>> t.groups_
	[
		[
			[-inf, 45],
			[82, 86],
			[89, inf]
		],
		[
			[-inf, 25],
			[27, 57],
			[83, inf]
		]
	]

	>>> t.transform(a)
	array([
		[86, 83,  2,  3],
		[82, 18,  2,  1],
		[45, 25,  1,  1],
		[13, 27,  1,  2],
		[89, 57,  3,  2]
	])


	"""

	def __init__(self, n_groups, expand_X=True):

		self.n_groups = n_groups
		self.groups_ = []
		self.expand_X = expand_X

	def fit(self, X):

		for i, col in enumerate(X.T):

			row_split = np.array_split(sorted(col), self.n_groups)

			self.groups_.append([])

			for x in row_split:
				if not x.all():
					break
				self.groups_[i].append([x[0], x[-1]])

			self.groups_[-1][0][0], self.groups_[-1][-1][1] = -float("inf"), float("inf")

		return self

	def transform(self, X):

		new_array = np.empty_like(X)

		for (row_i, cell_i), v in np.ndenumerate(X):

			for space_index, space in enumerate(self.groups_[cell_i]):

				if space[0] <= v <= space[1]:
					new_array[row_i][cell_i] = space_index + 1  # avoid group 0
					break

		return np.c_[X, new_array] if self.expand_X else new_array


def split_numerical_into_groups(X, **kwargs):
	"""
	Syntax sugar for splitting 1-D array through NumericalIntoGroupsSplitter class

	Parameters
	----------
	n_groups : int
			Quantity of groups to split
	expand_X : bool, optional
			Expand or replace original X
	"""

	_ = NumericalIntoGroupsSplitter(**kwargs)

	return _.fit_transform(np.reshape(X, (len(X), -1)))[:, 1:]

