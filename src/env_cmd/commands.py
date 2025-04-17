import click
import os
from src.common.files import get_file_or_dir_infos, get_files, permissions_to_string


# ---------------------------------------------------------------------------------------------------- #

@click.command(name="list")
@click.option("-p", "--path", default=".", help="Path to the directory to list files from.")
def list_env_files(path: str):
    """
    List all 'dot env' files in the specified directory and its subdirectories.
    """
    files = get_files(path, pattern=r'.*\.env.*', include_subdirs=True)

    count = len(files)

    if count == 0:
        click.secho(f"No 'dot env' files found in '{path}'", fg="yellow")
        click.echo()  # Add an empty line for better readability
        return

    click.echo(
        f"Found {click.style(count, fg='green')} 'dot env' files in '{path}'")
    click.echo("\nListing files:")

    for file in files:
        f_stats = get_file_or_dir_infos(file)
        file_permissions = "d" if f_stats["is_dir"] else "-"
        file_permissions += permissions_to_string(f_stats["permissions"])

        if not f_stats["is_dir"] and 'x' in file_permissions:
            f_stats['path'] = click.style(
                f_stats['path'], fg="green", bold=True)
        elif f_stats["is_dir"]:
            f_stats['path'] = click.style(
                f_stats['path'], fg="blue", bold=True)

        click.echo(
            f"{file_permissions} {f_stats['links']}\t{f_stats['owner']}\t{f_stats['group']}\t{f_stats['size']}\t{f_stats['last_modified']} {f_stats['path']}")
    click.echo()  # Add an empty line for better readability
    return

# ---------------------------------------------------------------------------------------------------- #


@click.command(name="remove")
@click.option("-p", "--path", default=".", help="Path to the directory to remove files from.")
@click.confirmation_option(prompt="Are you sure you want to remove all 'dot env' files? This action cannot be undone.")
def remove_env_files(path: str):
    """
    Remove all 'dot env' files in the specified directory and its subdirectories.
    """
    files = get_files(path, pattern=r'.*\.env$', include_subdirs=True)

    count = len(files)

    if count == 0:
        click.secho(f"No 'dot env' files found in '{path}'", fg="yellow")
        click.echo()
        return

    click.echo(
        f"Found {click.style(count, fg='green')} 'dot env' files to remove in '{path}'")
    click.echo("\nRemoving files:")

    for file in files:
        if os.path.isfile(file):
            os.remove(file)
            click.echo(
                f"Removed file: {click.style(file, fg='red', bold=True)}")
        else:
            click.echo(f"Skipped non-file: {file}")

    click.echo()
    return

# ---------------------------------------------------------------------------------------------------- #


@click.command(name="init")
@click.option("-p", "--path", default=".", help="Path to the directory to initialize.")
@click.option("-f", "--force", is_flag=True, help="Force overwrite existing files.")
def init_env_files(path: str, force: bool):
    """
    Initialize the environment files in the specified directory by copying the `.env.example` file.
    """
    files = get_files(path, pattern=r'.*\.env.example$', include_subdirs=True)
    count = len(files)
    if count == 0:
        click.secho(f"No '.env.example' files found in '{path}'", fg="yellow")
        click.echo()
        return

    click.echo(
        f"Found {click.style(count, fg='green')} '.env.example' files to initialize in '{path}'")
    click.echo("\nInitializing files:")
    for file in files:
        env_file = file.replace('.env.example', '.env')
        if os.path.isfile(env_file) and not force:
            click.echo(
                f"Skipped existing file: {click.style(env_file, fg='yellow', bold=True)}")
            continue
        elif os.path.isfile(env_file):
            os.remove(env_file)
            click.echo(
                f"Removed existing file: {click.style(env_file, fg='red', bold=True)}")

        with open(file, 'r') as src_file:
            content = src_file.read()

        with open(env_file, 'w') as dest_file:
            dest_file.write(content)

        click.echo(
            f"Initialized file: {click.style(env_file, fg='green', bold=True)}")
    click.echo()
    return

# ---------------------------------------------------------------------------------------------------- #
