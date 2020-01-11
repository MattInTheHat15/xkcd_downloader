# xkcd_downloader
Downloads comics and metadata from xkcd

Reqires `bs4` and  `requests`

Usage: `python xkcd_downloader.py`

Features:
* Downloads XKCD comics and metadata
* Creates a "history" file to avoid downloading the same comic twice
* Pauses 5 seconds between downloads to avoid putting a strain on the XKCD server
