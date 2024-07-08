import os
import uuid
from datetime import datetime
from pathlib import Path

import typer
from palworld_save_tools.commands.convert import (convert_json_to_sav,
                                                  convert_sav_to_json)
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated

HOST_DEFAULT_UUID = "00000000-0000-0000-0000-000000000001"
DATETIME_FORMAT = "%Y_%m_%d-%p%I_%M_%S"

app = typer.Typer()


def _replace_lines_to_file(
    from_char, to_char, original_path: str, save_path: str
) -> None:
    with open(original_path, "r") as fr, open(save_path, "w") as fw:
        for line in fr:
            new_line = line.replace(from_char, to_char)
            fw.writelines(new_line)


def update_palworld_file(file_path: str, from_uuid: str, to_uuid: str) -> None:
    curr_time = f"{datetime.now().strftime(DATETIME_FORMAT)}"

    output_dir = os.path.join(os.path.dirname(file_path), "output")
    temp_json_path = os.path.join(output_dir, f"temp_original_{curr_time}.json")
    temp_replace_path = os.path.join(output_dir, f"temp_replaced_{curr_time}.json")
    file_name = Path(file_path).stem
    output_path = os.path.join(output_dir, f"{file_name}_replaced.sav")

    os.makedirs(output_dir, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        progress.add_task("[green]Processing original file...", total=None)
        convert_sav_to_json(file_path, temp_json_path, force=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        progress.add_task(description="[red]Converting...", total=None)
        _replace_lines_to_file(from_uuid, to_uuid, temp_json_path, temp_replace_path)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        progress.add_task(description="[cyan]Saving...", total=100)
        convert_json_to_sav(temp_replace_path, output_path, force=True)

    os.remove(temp_json_path)
    os.remove(temp_replace_path)


@app.command()
def update_uuid(
    file_path: Annotated[
        str, typer.Option(help="Filepath to either {PLAYER_UUID}.sav or Level.sav")
    ],
    to_uuid: Annotated[str, typer.Option(help="New player UUID, with/without hypen")],
    from_uuid: Annotated[
        str,
        typer.Option(
            help="Old player UUID to move from, if not specified the program will use the host default UUID"
        ),
    ] = HOST_DEFAULT_UUID,
) -> None:

    try:
        from_uuid = str(uuid.UUID(from_uuid))
    except ValueError:
        typer.echo(f"Please double check from_uuid value")
        return

    try:
        to_uuid = str(uuid.UUID(to_uuid))
    except ValueError:
        typer.echo(f"Please double check to_uuid value")
        return

    update_palworld_file(file_path=file_path, from_uuid=from_uuid, to_uuid=to_uuid)
    typer.echo(f"Done. Please check the output folder.")


if __name__ == "__main__":
    app()
