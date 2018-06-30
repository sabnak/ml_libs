from matplotlib import pyplot as plt
import numpy as np
from collections import OrderedDict


def visualize_relations(dataset, y, y_value_list=None, columns=None, max_values=10, n_cols=3, colors=None, **kwargs):
	"""
	Visualize relations between class and categorical attributes

	:param dataset: Pandas DataSet.
	:param y: str. Class to exam
	:param y_value_list: list or None. List of class values to exam. If None - exam all
	:param columns: list or None. List of attributes to exam. If None - exam all
	:param max_values: int. Max unique values of attributes to exam
	:param n_cols: int. Columns in final plot
	:param colors: dict or None. Color for each class value. If None - default
	:param kwargs: dict. Additional plotting options
	:return: None
	"""
	params = dict(rot=0)
	params.update(kwargs)

	if not columns:
		columns = [x for x in dataset if x != y]

	n_rows = int(np.ceil(len(columns) / n_cols))

	_, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(20, 5 * n_rows), squeeze=False)

	for column, ax in zip(columns, axes.flatten()):

		ax.set_title(column)
		r = dataset.get([y, column]).groupby([y, column]).size()

		unique_values = dataset.get(column).unique()

		if len(unique_values) > max_values:
			continue

		groups = dict()
		column_names = []

		for (y_value, col_name), group_size in r.items():
			if col_name not in column_names:
				column_names.append(col_name)

			if y_value_list and y_value not in y_value_list:
				continue

			if y_value not in groups:
				groups[y_value] = OrderedDict((n, 0) for n in unique_values)
			groups[y_value][col_name] = group_size

		plots = []
		plots_names = []
		ind = np.arange(len(column_names))
		width = .35
		offset = 0

		for y_value, col in groups.items():
			plots.append(ax.bar(
				ind + offset,
				col.values(),
				width=.35,
				color=None if not colors or y_value not in colors else colors[y_value],
				label=column
			))
			offset += width
			plots_names.append(y_value)

		ax.set_xticks(ind + width / 2)
		ax.set_xticklabels(column_names)
		plt.legend(plots, plots_names, fontsize=20)

	plt.suptitle("{}: {}".format(y, y_value_list if y_value_list else "ALL"))

