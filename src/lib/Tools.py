import requests
import urllib


def build_google_drive_url(doc_id):
    DRIVE1 = "https://docs.google.com/uc"
    DRIVE2 = "https://drive.google.com/uc"

    baseurl = DRIVE1  # DRIVE2 works as well
    params = {"export": "download",
              "id": doc_id}
    url = baseurl + "?" + urllib.parse.urlencode(params)
    return url


def read_remote(url):
    # some python versions throw an exception
    # with the use of 'with'
    with requests.get(url) as response:
        response.encoding = 'utf-8'
        if response.status_code == requests.codes.ok: # that is 200
            return response.text
    return None


def read_remote1(url):
    # assumes the url is already encoded (see urllib.parse.urlencode)
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == requests.codes.ok:  # that is 200
        return response.text
    return None

