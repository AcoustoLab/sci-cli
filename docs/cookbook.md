# Cookbook

## uv

## Lightning

### TensorBoard

The model template allow to log metrics to TensorBoard if `TensorBoardLogger` is enabled in the .yaml config. 

Install the optional TensorBoard dashboard with either:

```bash
uv sync --extra tensorboard
# or
pip install "sci-cli[tensorboard]"
```

Train normally:

```bash
uv run python experiments/model/model.py fit
```

Loggers use the directory defined in the .yaml config as `log_name`, containing the main model parameters, for tensorboard:

```text
experiments/model/tb-<log_name>/version_#/
```


Start TensorBoard at the parent directory to compare all runs:

```bash
uv run tensorboard \
    --logdir experiments/model \
    --host 127.0.0.1 \
    --port 6006
```
Open <http://127.0.0.1:6006>.


### TensorBoard over SSH

Run TensorBoard on the remote machine using the commands above. On the local machine, forward its loopback port:

```bash
ssh -N -L 6007:127.0.0.1:6006 user@remote-host
```
Then open <http://127.0.0.1:6007> locally.

## ssh

