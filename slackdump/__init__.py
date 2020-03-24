import click

from slackdump.scraper import run_scraper


@click.command()
@click.option(
    "--ROOTURL",
    "-e",
    type=str,
    help="The url to your channel, eg: https://somewhere.slack.com/messages/66666666",
)
def cli(rooturl):
    run_scraper(rooturl)
