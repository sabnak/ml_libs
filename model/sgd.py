from sklearn.base import clone
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import SGDRegressor


def SGD_with_early_stoppind(
				X_train,
				y_train,
				X_val,
				y_val,
				n_epochs=1000,
				stopping_coef=None,
				model_class=SGDRegressor,
				metric_function=mean_squared_error,
				metric_function_params=None,
				random_state=None,
				**kwargs
):

	model_params = dict(
		max_iter=1,
		warm_start=True,
		penalty=None,
		learning_rate="constant",
		eta0=0.0005,
		random_state=random_state
	)

	model_params.update(kwargs)

	model = model_class(**model_params)

	minimum_val_error = float("inf")
	best_epoch = None
	best_model = None
	stagnation_counter = 0
	epochs_pass = 0

	if metric_function_params is None:
		metric_function_params = dict()

	for epoch in range(n_epochs):
		model.fit(X_train, y_train)
		y_val_predict = model.predict(X_val)
		val_error = metric_function(y_val, y_val_predict, **metric_function_params)

		epochs_pass += 1

		if val_error < minimum_val_error:
			minimum_val_error = val_error
			best_epoch = epoch
			best_model = clone(model)
			stagnation_counter = 0
		else:
			stagnation_counter += 1

		if stopping_coef and (stagnation_counter / n_epochs) > stopping_coef:
			break

	return best_model, dict(
		best_epoch=best_epoch,
		minimum_val_error=minimum_val_error,
		epochs_pass=epochs_pass
	)
