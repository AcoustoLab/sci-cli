# sci-cli

Create a new model named `model` in experiments folder in `experiments/model` directory.
```
python -m sci_cli.cookiecutter model -o experiments/model
```
Then, edit the model code file `experiments/model/model.py` and the config file `experiments/model/model_fit_config.yml` to set the model parameters, data parameters, and training parameters.
Now you can run the model training using the following command:
```
python experiments/model/model.py fit
```

In the case of `uv` usage, add `uv run` before the commands above, e.g.:
```
uv run python -m sci_cli.cookiecutter model -o experiments/model
uv run python experiments/model/model.py fit
```
