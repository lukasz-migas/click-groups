"""Core functionality."""
import typing as ty
import click

class GroupedGroup(click.Group):
    """Override click group to enable ordering and grouping.

    See: https://stackoverflow.com/questions/47972638/how-can-i-define-the-order-of-click-sub-commands-in-help
    See: https://stackoverflow.com/questions/57066951/divide-click-commands-into-sections-in-cli-documentation
    """

    def __init__(self, *args, **kwargs):
        # dictionary containing priority of each command
        self.priorities = {}
        # dictionary containing list of commands for each help group
        self.help_groups = {}
        # dictionary containing priority of each help group
        self.help_groups_priority = {}
        super().__init__(*args, **kwargs)

    # noinspection PyAttributeOutsideInit
    def get_help(self, ctx) -> str:
        """Get help."""
        return super().get_help(ctx)

    def list_commands(self, ctx: click.Context) -> ty.Iterable[str]:
        """Reorder the list of commands when listing the help."""
        commands = super().list_commands(ctx)
        return (c[1] for c in sorted((self.priorities.get(command, 1), command) for command in commands))

    def sort_commands_with_help(self, commands_with_help: ty.List[ty.Tuple[str, str]]) -> ty.List[ty.Tuple[str, str]]:
        """Sort commands with help."""
        return sorted(commands_with_help, key=lambda x: self.priorities[x[0]])

    def add_command(
        self, cmd, name=None, priority=1, help_group: str = "Commands", help_group_priority: ty.Optional[int] = None
    ) -> None:
        """Add command."""
        super().add_command(cmd, name)
        self.priorities[cmd.name] = priority
        self.help_groups.setdefault(help_group, []).append(cmd.name)
        if help_group not in self.help_groups_priority:
            self.help_groups_priority[help_group] = help_group_priority or 1
        if help_group_priority is not None:
            self.help_groups_priority[help_group] = help_group_priority

    def command(
        self, *args, priority=1, help_group: str = "Commands", help_group_priority: ty.Optional[int] = None, **kwargs
    ) -> ty.Callable:
        """Behaves the same as `click.Group.command()` except capture a priority for listing command names in help.
        """
        priorities = self.priorities
        help_groups = self.help_groups
        help_groups_priority = self.help_groups_priority
        if help_group not in help_groups_priority:
            help_groups_priority[help_group] = help_group_priority or 1
        if help_group_priority is not None:
            self.help_groups_priority[help_group] = help_group_priority

        def decorator(f):
            cmd = super().command(*args, **kwargs)(f)
            priorities[cmd.name] = priority
            help_groups.setdefault(help_group, []).append(cmd.name)
            return cmd

        return decorator

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Format commands."""
        for help_group in sorted(self.help_groups, key=lambda x: self.help_groups_priority[x]):
            commands = self.help_groups[help_group]
            # for group, commands in self.help_groups.items():
            rows = []
            for subcommand in commands:
                cmd = self.get_command(ctx, subcommand)
                if cmd is None:
                    continue
                rows.append((subcommand, cmd.get_short_help_str()))

            if rows:
                rows = self.sort_commands_with_help(rows)
                with formatter.section(help_group):
                    formatter.write_dl(rows)
