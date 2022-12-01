"""Console script for picsbox_uploader."""
import sys
import click
from click_help_colors import HelpColorsCommand
from .picsbox_uploader import upload_picsbox
from . import __version__


def print_version(ctx, param, value):
    """Function called when using --version."""
    if not value or ctx.resilient_parsing:
        return
    click.echo('picsbox-up ' + __version__)
    ctx.exit()


@click.command(cls=HelpColorsCommand,
               no_args_is_help=True,
               help_headers_color='yellow',
               help_options_color='green',
               context_settings={'max_content_width': 100})
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.argument('filename', type=click.Path(exists=True))
@click.option('-s', '--size', type=click.Choice(["small", "thumbnail", "medium", "normal", "forum"]),  # noqa: E501
              default="forum",
              help=''''Value for image resizing. Optional.

              \b
              "small", "thumbnail", "medium", "normal", "forum"''')
def app(filename, size):  # pylint: disable=redefined-builtin  # noqa: D301,E501
    """Upload an image to Picsbox, and get url back.

    \b
    Resizing is optionnal ("small", "thumbnail", "medium", "normal", "forum")
    Default returned url is the forum size.

    \b
    Examples :
        picsbox-up my_image.jpg

        picsbox-up my_image --size medium
    """
    res = upload_picsbox(filename, size)
    click.echo(res)
    return 0


if __name__ == "__main__":
    sys.exit(app())  # pragma: no cover
