"""
This module provides the command line interface (CLI) for the environment commands.
"""

import click

from src.env_cmd import commands


@click.group(name="env")
def env_cmd():
    """env_cmd - CLI is a command line interface for the environment commands.
    """
    pass


env_cmd.add_command(commands.list_env_files)
env_cmd.add_command(commands.remove_env_files)
env_cmd.add_command(commands.init_env_files)
