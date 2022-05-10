import click

try:
    import lvtn1_utils as utils

    config = utils.load_config()
    logger = utils.setup_logging("{{cookiecutter.package_name}}.cli")
except ImportError:
    import logging

    config = {}
    logger = logging.getLogger("{{cookiecutter.package_name}}.cli")


@click.group()
def cli():
    pass


@cli.command()
def hello():
    """Will greet"""
    print("Hello World!")


if __name__ == "__main__":
    cli()
