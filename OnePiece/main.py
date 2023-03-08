# main.py - Manages all the work needed to download OnePiece manga.

from bs4 import BeautifulSoup
from threading import Thread
import os, re, requests


# This function makes sure all on the chapter are downloaded and stored correctly.
def download_OnePiece_Manga():
    # Setting up the rootURL and cwURL for the downloader.
    rootURL = "https://onepiecechapters.com"
    cChpURL = "https://onepiecechapters.com/chapters/433/one-piece-chapter-1"
    threads = []

    # Loops until there are no chapters to be downloaded.
    while cChpURL != None:
        # Determinds which chapter is being downloaded and creates a folder for that
        # chapter in some steps.

        # 1 - Creating a regex to get chapter number.
        chNumRegex = re.compile(r"chapter-(\d+)")

        # 2 - Using the regex to get the chapter num.
        chpSearch = chNumRegex.search(cChpURL)
        chpNum = chpSearch.group(1)

        # 3 - Makes the new Directory for the current chapter's downloading.
        os.makedirs(f"Chapter_{chpNum}", exist_ok=True)
        os.chdir(f"Chapter_{chpNum}")

        # Downloading the HTML Document of the current chapter and Checkink for any issues.
        res = requests.get(cChpURL)
        res.raise_for_status()

        # Creating a DOM Object fot the downloaded document.
        doc = BeautifulSoup(res.text, "html.parser")

        # Downloading the current chapter using threads in some steps.
        print(f"Started downloading Chapter-{chpNum}")

        # 1 - Creating a new thread.
        newThread = Thread(target=downloadChapter, args=(doc, threads))

        # 2 - Appending this thread in chpDownloadingThreads.
        threads.append(newThread)

        # Starts the new thread.
        newThread.start()

        # Getting the URL of the next Chapter in some steps.

        # 1 - Regex to get a piece from the current Chapter URL.
        cChpNameInURLRegex = re.compile(
            r"(.*?)(/chapters)(/\d+)(/one-piece-chapter-(\d+))"
        )

        # 2 - Searches the Current-Chapter-URL using Regex and gets the next-Chapter-Name.
        cChpNameSearch = cChpNameInURLRegex.search(cChpURL)
        nChpName = f"one-piece-chapter-{str(int(cChpNameSearch.group(5)) + 1)}"

        # 3 - Selects the next chapter <a> tag using the Next Chapter Name.
        # And gets the next Chapter URL
        nextBtn = doc.select_one(f'a[href$="{nChpName}"]')
        if nextBtn == None:
            cChpURL = None
        else:
            cChpURL = f'{rootURL}{nextBtn["href"]}'

        # Goes back to the root downloads Directory.
        os.chdir("../")

    return threads


# This function downloads a Chapter from the DOC given to it in it's arguments.
def downloadChapter(doc, threads):

    # Selecting all the img elements
    imgElems = doc.select('img[alt~="Piece"]')

    # Creates a new thread to download each img together.
    for i in imgElems:
        # Creates a new thread.
        newThread = Thread(target=downloadPage, args=(i,))

        # Appends this thread in threads.
        threads.append(newThread)

        # Starts the new thread.
        newThread.start()


# This function loops through the img elements specified in the arguments one-by-one and
# downloads them. Then writes them in an image file
def downloadPage(elem):
    # Getting the Sourcr URL of the img.
    imgURL = elem["src"]

    # Downloading the img from the Source URL and checking for issues.
    img = requests.get(imgURL)
    img.raise_for_status()

    # Creates a new img file for the current page being processed. And Opens it.
    imgfile = open(os.path.basename(imgURL)[-6:], "wb")

    # Writing the downloaded image in the new img file 100000-per-iteration
    for chunk in img.iter_content(100000):
        imgfile.write(chunk)

    # Closes the current img file.
    imgfile.close()
