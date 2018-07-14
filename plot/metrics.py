import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


def plot_learning_curves(model, X, y, cost_function_name="RMSE", axis=None):
	X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=10)
	train_errors, val_errors = [], []

	if cost_function_name == "RMSE":
		cost_function = mean_squared_error
	else:
		raise ValueError("Unsupported cost function: {}".format(str(cost_function_name)))

	for m in range(1, len(X_train)):
		model.fit(X_train[:m], y_train[:m])
		y_train_predict = model.predict(X_train[:m])
		y_val_predict = model.predict(X_val)
		train_errors.append(cost_function(y_train[:m], y_train_predict))
		val_errors.append(cost_function(y_val, y_val_predict))

	plt.figure(figsize=(10, 5))
	plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="train")
	plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label="val")
	plt.legend(loc="upper right", fontsize=14)
	plt.xlabel("Training set size", fontsize=14)
	plt.ylabel(cost_function_name, fontsize=14)

	if axis:
		plt.axis([0, 80, 0, 3])