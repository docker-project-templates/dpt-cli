import click


@click.group()
def dpt():
    """DPT - CLI is a command line interface for the Docker Project Templates.
    """
    pass


@dpt.command("greet")
@click.option("--count", default=1, help="number of greetings")
@click.argument("name")
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    dpt()
