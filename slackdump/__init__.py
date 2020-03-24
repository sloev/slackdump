import click

from slackdump.scraper import run_scraper
from slackdump.chrome import osx_chrome


@click.command()
@click.option(
    "--ROOTURL",
    "-e",
    type=str,
    help="The url to your channel, eg: https://somewhere.slack.com/messages/66666666",
)
def cli(rooturl):
    with osx_chrome() as debug_url:
        run_scraper(rooturl, debug_url)


if __name__ == "__main__":
    cli()