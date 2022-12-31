import requests
import os

def download_data():
    if (os.path.exists("resources\Data.csv")) :
        return
        
    """Download data at each start of the dashboard to always be up to date
    """
    url = "https://www.data.gouv.fr/fr/datasets/r/8a0b8d35-fea2-4c8d-9af1-fb25edb16980"

    r = requests.get(url, allow_redirects=True)
    open("resources\Data.csv", 'wb').write(r.content)