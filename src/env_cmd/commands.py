import click

from src.common.files import get_file_or_dir_infos, get_files, permissions_to_string


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
