"""Simple app."""
import click
from click_groups import GroupedGroup

@click.group(cls=GroupedGroup)
def cli():
    pass

@cli.command(help_group="Group 1")
def command_1():
    """Run a command."""

@cli.command(help_group="Group 1")
def command_2():
    """Run a command."""

@cli.command(help_group="Group 2")
def command_3():
    """Run a command."""

@cli.command(help_group="Group 3")
def command_4():
    """Run a command."""


if __name__ == "__main__":
    cli()