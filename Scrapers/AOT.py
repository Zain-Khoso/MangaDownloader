# main.py - Manages all the work needed to download AOT manga.

import os, re, requests
from threading import Thread
from pathlib import Path
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError


# This function makes sure all on the chapter are downloaded and stored correctly.
def download_AOT_Manga():
    # Setting up the rootURL and cwURL for the downloader.
    cwURL = "https://onepiecechapters.com/chapters/3721/attack-on-titan-chapter-1"

    # Loops until there are no chapters to be downloaded.
    while cwURL != None:
        # Determinds which chapter is being downloaded and creates a folder for that chapter.
        chNumSearch = re.compile(r"chapter-(\d+)").search(cwURL)
        chNum = chNumSearch.group(1)
        os.makedirs(f"Chapter_{chNum}", exist_ok=True)

        # Downloading the HTML Document of the current chapter and Checking for any issues.
        try:
            res = requests.get(cwURL)
            res.raise_for_status()
        except ConnectionError:
            print("Unable to download Chapter_%s at %s" % (chNum, cwURL))
        else:
            # Creating a DOM Object for the downloaded document.
            DOM = BeautifulSoup(res.text, "html.parser")
            print(f"Chapter-{chNum} ", end="")

            # Call to downloadChapter function, which downloads the current chapter.
            downloadChapter(DOM, chNum)
        finally:
            # Call to getNextURL function, which return the URL address of the next Chapter.
            cwURL = getNextURL(DOM, cwURL)


# This function gets the URL of the next Chapter.
def getNextURL(DOM, cwURL):
    # 1 - Regex to get info for next Chapter URL in the Current Chapter URL.
    cwURLRegex = re.compile(
        r"(.*?)(/chapters)(/\d+)(/attack-on-titan-chapter-(\d+))"
    )

    # 2 - Searches the Current-Chapter-URL using Regex and gets the next-Chapter-Name.
    cChpURLSearch = cwURLRegex.search(cwURL)
    nChpName = (
        f"attack-on-titan-chapter{str(int(cChpURLSearch.group(5)) + 1)}"
    )

    # 3 - Selects the next chapter <a> tag using the Next Chapter Name.
    # If none exists then returns None.
    nextBtn = DOM.select_one(f'a[href$="{nChpName}"]')

    # Gets the next Chapter URL
    if nextBtn == None:
        nChpURL = None
    else:
        nChpURL = f'{cChpURLSearch.group(1)}{nextBtn["href"]}'

    return nChpURL


# This function downloads a Chapter from the DOC given to it in it's arguments.
def downloadChapter(DOM, chNum):
    # Selecting all Manga Pages.
    pageElems = DOM.select('img[alt~="Titan"]')
    threads = []

    # Creating new threads to download all the pages in packs of 10s.
    for i in range(0, len(pageElems), 10):
        # Getting some required values
        sIndex, eIndex = i, i + 9

        # Making sure the eIndex is correct.
        if eIndex >= len(pageElems):
            eIndex = len(pageElems) - 1

        # Creating a new thread.
        newThread = Thread(target=downloadPage, args=(chNum, pageElems, sIndex, eIndex))

        # Appends this thread in the list of the all threads.
        threads.append(newThread)

        # Starts the new thread.
        newThread.start()

    # Appending all the threads that were created in the main thread.
    for thread in threads:
        thread.join()

    print("Downloaded.")


# This function loops through the range of img elements specified in the arguments
# one-by-one and downloads them. Then writes them in an image file.
def downloadPage(chNum, pages, sIndex, eIndex):
    # Looping through the img range.
    for i in range(sIndex, eIndex + 1):
        # Getting the Source URL of the img.
        imgURL = pages[i]["src"]

        # Downloading the img from the Source URL and checking for issues.
        try:
            # Downloading the Page Image.
            img = requests.get(imgURL)
            img.raise_for_status()
        except ConnectionError or HTTPError as err:
            print(f"Was not able to download Page_{imgURL}")

            # Creates a new txt file for the error that occured when downloading the
            # current page. And Opens it.
            file = open(
                Path.cwd() / f"Chapter_{chNum}" / os.path.basename(imgURL)[-6:]
                + ".txt",
                "w",
            )
            # Writes the newly created file.
            file.writelines([f"IMG_URL: {imgURL}\n", f"ERROR: {err}"])
        else:
            # Creates a new file for the current page being processed. And Opens it.
            file = open(
                Path.cwd() / f"Chapter_{chNum}" / os.path.basename(imgURL)[-6:], "wb"
            )

            # Writing the downloaded image in the new file 100000-per-iteration
            for chunk in img.iter_content(100000):
                file.write(chunk)
        finally:
            # Closes the current img file.
            file.close()
