"""Main module."""

import json
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import filetype
import mechanicalsoup

# config_file credentials
config_file = Path("~").expanduser() / ".config" / "forumtrad1.json"
try:
    with open(config_file, encoding='utf-8') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Le fichier dans votre répertoire utilisateur / .config / forumtrad1.json"  # noqa: E501
          "n'existe pas. Créez le, au format json"
          "avec les clés user et password")
    input("Appuyer sur une touche pour quitter.")
    sys.exit()

host = data["host"]
user = data["user"]
password = data["password"]
picsbox = urljoin(host, "app.php/picsbox/image")

headers = {
    "Accept": "*/*",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",  # noqa: E501
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "X-Requested-With": "XMLHttpRequest"
    }


def upload_picsbox(path, size: str = "forum"):
    """Upload image to picsbox, with a size

    Args:
        path (_type_): path to the image
        size (str, optional): Size to the uploaded image. Defaults to "forum".

    Returns:
        str: url of image
    """
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(host)

    # LOGIN
    browser.follow_link("mode=login")
    browser.select_form("form#login")
    browser["username"] = user
    browser["password"] = password
    browser["autologin"] = "on"
    # browser.form.print_summary()
    time.sleep(0.6)
    browser.submit_selected()

    # Get tokens for picsbox
    r = browser.open_relative("posting.php?mode=reply&t=16622#preview")
    time.sleep(0.6)
    picsboxupload = r.soup.select_one("#picsbox-upload")['data-picsbox-tokens']
    picsbox_dict = json.loads(picsboxupload)
    post_token = picsbox_dict.pop("post_token")
    # delete_token = picsbox_dict.pop("delete_token")
    picsbox_dict["form_token"] = post_token
    picsbox_dict["resize-mode"] = size
    # resize-mode = small / thumbnail / medium / normal / forum /

    # Input
    input_ = path
    kind = filetype.guess(input_)
    if kind is None:
        print('Cannot guess file type!')
        sys.exit(1)

    # Post image
    with open(input_, 'rb') as f:
        file_ = {'file': (input_, f, kind.mime)}
        r = browser.post(picsbox,
                         files=file_,
                         data=picsbox_dict,
                         headers=headers)
    # Result
    return r.json()["url"]


if __name__ == "__main__":
    res = upload_picsbox(sys.argv[1])
    print(res)
