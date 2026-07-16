"""ClearML utility functions for the sci-cli package."""

from pathlib import Path
import os
from dataclasses import dataclass
from collections.abc import Mapping, Iterable
import warnings


@dataclass
class Requirement:
    """Represents a ClearML requirement with a name and an optional version."""

    name: str
    version: str | None = None


@dataclass
class RequirementsConfig:
    """Configuration for ClearML requirements management.

    Packages can be specified to be removed, replaced, or added to the ClearML task requirements.
    """

    unnecessary: Iterable[Requirement] | None = None
    replacements: Mapping[str, Requirement] | None = None
    additional: Iterable[Requirement] | None = None


def fix_clearml_requirements(requirements: RequirementsConfig | None):
    """
    Fix ClearML requirements based on the provided configuration.

    This function modifies the ClearML task requirements according to the
    specified configuration, allowing for removal of unnecessary requirements,
    replacement of existing requirements, and addition of new requirements.


    Parameters
    ----------
    requirements : RequirementsConfig or None
        Configuration specifying which requirements to remove, replace, or add.
        If None, no changes are made.
    """
    if requirements is None:
        return

    from clearml.task import Task

    # remove unnecessary requirements
    if requirements.unnecessary is not None:
        for req in requirements.unnecessary:
            Task.ignore_requirements(req.name)

    # replace requirements
    if requirements.replacements is not None:
        for name, req in requirements.replacements.items():
            Task.ignore_requirements(name)
            Task.add_requirements(req.name, req.version)

    # add additional requirements
    if requirements.additional is not None:
        for req in requirements.additional:
            Task.add_requirements(req.name, req.version)


def set_conf_env(config_file: str | None = "clearml.conf"):
    """Set the ClearML config file environment variable.

    Parameters
    ----------
    config_file : str | None, optional
        Path to the ClearML config file, by default "clearml.conf"
    """
    import clearml.config

    if clearml.config.running_remotely():
        return

    if config_file is None:
        return

    if not config_file:
        return

    config_file_parh = Path(config_file).absolute()

    if not config_file_parh.exists() or not config_file_parh.is_file():
        warnings.warn(f"ClearML config file {config_file} does not exist.", stacklevel=2)

    os.environ["CLEARML_CONFIG_FILE"] = str(config_file_parh)
