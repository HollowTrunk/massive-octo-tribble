
import urllib

from PIL import Image
from io import BytesIO
from massive.models import *
from bs4 import BeautifulSoup


def get_page_favicon(url, iconUri=None):
    page = None
    if iconUri:
        try:
            page = urllib.request.urlopen(iconUri, timeout=5)
        except:
            page = None

    if not page:
        try:
            page = urlopen("http://getfavicon.appspot.com/%s" % url, timeout=5)
        except:
            page = None

    if page:
        i = BytesIO(page.read())

        if i:
            image = BytesIO()
            try:
                Image.open(i).save(image, "PNG")
                image.seek(0)
                fav = Favicon()
                fav.image.put(image)
                fav.save()
                return fav
            except Exception as e:
                print("error with image")
        else:
            return None


def get_page_title(url):
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        text = urllib.request.urlopen(req).read()
    except:
        return None
        
    soup = BeautifulSoup(text)

    for x in soup.findAll('title'):
        if x.string:
            return x.string

    return None
