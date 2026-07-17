# sci-cli

## Installation

```bash linenums="0"
pip install sci-cli
```

## Quick Start

```bash linenums="0"
python -m sci_cli.cookiecutter model -o model
```

Then, edit the model code file `model/model.py` and the config file `model/model_fit_config.yml` to set the model parameters, data parameters, and training parameters.
```bash linenums="0"
python model/model.py fit
```

- **[API Reference](reference.md)**: Detailed documentation of the `sci-cli` api.

The project is developed by [ITMO AcoustoLab](https://acoustolab.itmo.ru/en) members.
