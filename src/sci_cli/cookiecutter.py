"""Cookiecutter for model template."""

import argparse
from pathlib import Path
from shutil import copy
from importlib import import_module


def copy_template(output_name: str, output_dir: Path | None = None, force: bool = False):
    """
    Create `{output_name}_fit_config.yml` and `{output_name}.py` in the output directory.

    Parameters
    ----------
    output_name : str
        Name of the output files (e.g., 'AENet')
    output_dir : Path, optional
        Directory to copy the config to. If None, uses current working directory.
    force : bool, optional
        If True, overwrite existing files. If False (default), raise error if file exists.

    Raises
    ------
    FileExistsError
        If any output file already exists and force is False
    """
    output_dir = Path.cwd() if output_dir is None else Path(output_dir)

    # Get source directory
    module = import_module("sci_cli.templates.power.model")
    if hasattr(module, "__file__") and module.__file__:
        source_dir = Path(module.__file__).parent
    else:
        raise ValueError("Could not determine source directory `sci_cli.templates.power.model`")

    # Find config file
    config_file = source_dir / "model_fit_config.yml"
    source_file = source_dir / "model.py"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_file}\n"
            f"Expected to find model_fit_config.yml in {source_dir}"
        )

    if not source_file.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_file}\nExpected to find model.py in {source_dir}"
        )

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy file
    files = {
        f"{output_name}_fit_config.yml": config_file,
        f"{output_name}.py": source_file,
    }

    if not force:
        for file_name in files:
            output_file = output_dir / file_name
            if output_file.exists():
                raise FileExistsError(
                    f"Output file already exists: {output_file}\nUse --force to overwrite"
                )

    for file_name, source_file in files.items():
        output_file = output_dir / file_name
        copy(source_file, output_file)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Copy model template files.")

    parser.add_argument(
        "name",
        help="Name of the output files (e.g., AENet)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory (default: current working directory)",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )

    args = parser.parse_args()

    copy_template(args.name, args.output, force=args.force)


if __name__ == "__main__":
    main()
