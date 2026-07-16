"""Model template for sci-cli."""

import torch
import torch.nn as nn
import lightning as L
from sci_cli import run_cli


class DataModule(L.LightningDataModule):
    r"""Generates data using a simple power function.

    The data is generated with the following formula:
        $y = 2 - 2 \cdot x^2$
    """

    def __init__(self, dim: int, batch_size: int = 32, num_workers: int = 0):
        super().__init__()
        self.dim = dim
        self.batch_size = batch_size
        self.num_workers = num_workers

    def setup(self, stage: str):
        if stage == "fit":
            # Generate synthetic data for demonstration purposes
            x = torch.rand((64 * 1000, self.dim))
            a = 2
            b = -2
            y = a + b * x**2  # Example target: square of the input

            dataset = torch.utils.data.TensorDataset(x, y)

            # Split into training and validation datasets
            train_size = int(0.8 * len(dataset))
            val_size = len(dataset) - train_size
            self.train_dataset, self.val_dataset = torch.utils.data.random_split(
                dataset, [train_size, val_size]
            )

        elif stage == "test":  # noqa: SIM114
            raise NotImplementedError
        elif stage == "predict":
            raise NotImplementedError
        else:
            raise NotImplementedError

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            persistent_workers=True,
            shuffle=True,
            pin_memory=True,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            persistent_workers=True,
            pin_memory=True,
        )


class PowerBlock(nn.Module):
    """Calculates the power of the input tensor."""

    def __init__(
        self,
        power: int,
    ):
        super().__init__()
        self.a = torch.nn.Parameter(torch.rand(1)[0])
        self.b = torch.nn.Parameter(torch.rand(1)[0])
        self.power = power

    def forward(self, x: torch.Tensor):
        # x shape: (B, dim)
        x = self.a + self.b * x**self.power
        return x


class Module(L.LightningModule):
    r"""
    Power model.

    This model takes an input tensor and raises it to a specified power:
        $y = a  + b \cdot x^p$

    """

    def __init__(self, power: int):
        """Initialize the Module.

        Parameters
        ----------
        power : int
            The power to which to raise the input tensor

        """
        super().__init__()

        self.power_block = PowerBlock(power=power)

        # Loss function for reconstruction
        self.loss_fn = nn.MSELoss()

        # Save hyperparameters for logging and checkpointing
        self.save_hyperparameters()

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        y = self.power_block(x)

        return y

    def training_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x, y = batch

        y_pred = self(x)
        loss = self.loss_fn(y, y_pred)

        self.log(
            "train_loss",
            loss,
            on_step=True,
            on_epoch=True,
            prog_bar=True,
            logger=True,
        )

        return loss

    def validation_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x, y = batch

        y_pred = self(x)
        loss = self.loss_fn(y, y_pred)

        self.log(
            "val_loss",
            loss,
            on_epoch=True,
            prog_bar=True,
            logger=True,
        )

        return loss


if __name__ == "__main__":
    run_cli(__file__, run=True)
