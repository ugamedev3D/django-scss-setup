import click

class group_order(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command_order = []

    def add_command(self, cmd, name=None):
        name = name or cmd.name
        self._command_order.append(name)
        return super().add_command(cmd, name)

    def list_commands(self, ctx):
        return self._command_order