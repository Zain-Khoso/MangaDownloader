# TCB_Scans.py - Holds Scraper Class for tcbscans.org.

import os, re, requests as req
from requests.exceptions import ConnectionError, HTTPError
from bs4 import BeautifulSoup
from threading import Thread
from pathlib import Path


class Scraper:
    def __init__(self, firstChapterURL):
        # The starting URL for the Scraper.
        self.cURL = firstChapterURL

        # Regex to parse the URL.
        self.URLRegex = self.getURLRegex()

        # Apropriat Manga Name.
        self.mangaName = self.getMangaName()

        # Creating Downloads directory for the manga.
        os.makedirs(self.mangaName, exist_ok=True)
        os.chdir(self.mangaName)

        # Downloading Status.
        self.downloading = True

    def getURLRegex(self):
        # Returns a Regex object to parse the URL.
        return re.compile(
            r"""
            (.*?/)              # Group1 - Root URL of the site.
            (manga/)            # Group2 - "manga"
            (.*?/)              # Group3 - Manga name.
            (.*?-((\d|\.)+))    # Group5 - Chapter Number
            """,
            re.VERBOSE,
        )

    def getMangaName(self):
        # Parsing the URL to get manga name.
        mangaNameWords = self.URLRegex.search(self.cURL).group(3)[:-1].split("-")

        # Apropriat MangaName.
        mangaName = ""

        for word in mangaNameWords:
            mangaName += " %s" % word.capitalize()

        return mangaName.strip()

    def getNextURL(self):
        # Selecting the next btn
        nextBtn = self.DOM.select_one("a.next_page")

        # Getting the next chapter URL.
        if nextBtn == None:
            self.downloading = False
        else:
            self.cURL = nextBtn.get("href")

    def download(self):
        # Loops through all the chapters.
        while self.downloading:
            # Getting the Chapter Number.
            self.chpNum = self.URLRegex.search(self.cURL).group(5)

            # Creating a directory for chapter downloads.
            os.makedirs("Chapter_%s" % self.chpNum, exist_ok=True)

            # Downloading the chapter DOM.
            try:
                res = req.get(self.cURL)
                res.raise_for_status()

            # Handeling Connection or HTTPError.
            except ConnectionError or HTTPError as err:
                print(
                    "Was not able to download Chapter_%s\nAt: %s\nBecause of: %s"
                    % (self.chpNum, self.cURL, err)
                )

            # If there was no Exception.
            else:
                print("Chapter_%s " % self.chpNum, end="")

                # Creating DOM.
                self.DOM = BeautifulSoup(res.text, "lxml")

                # Call to downloadChapter method, which downloads the manga pages using threading
                self.downloadChapter()

            # Weither an error occurs or not.
            finally:
                self.getNextURL()

    def downloadChapter(self):
        # Selects all the manga-pages.
        pageElems = self.DOM.select("img.wp-manga-chapter-img")

        # Thread List
        threads = []

        # Createing threads to download each page.
        for elem in pageElems:
            # Creating new thread.
            newThread = Thread(target=self.downloadPage, args=(elem,))

            # Add newThread to Thread List
            threads.append(newThread)

            # Starts the newThread
            newThread.start()

        for thread in threads:
            thread.join()

        print("Downloaded.")

    def downloadPage(self, imgElem):
        # Getting img URL.
        imgURL = imgElem.get("src")

        # Downloading the img.
        try:
            res = req.get(imgURL)
            res.raise_for_status()

        # Handeling ConnectionError and HTTPError.
        except ConnectionError or HTTPError as err:
            # Creating a text file.
            file = open(
                Path.cwd()
                / f"Chapter_{self.chpNum}"
                / f"{os.path.basename(imgURL)[:-4]}.txt",
                "w",
            )
            # Writing the address of the file that was not downloaded successfully.
            # And the Error that occured, in this text file.
            file.writelines(["URL: %s\n" % imgURL, "ERROR: %s\n" % err])

        # If no exception occured.
        else:
            # Creating an image file.
            file = open(
                Path.cwd() / f"Chapter_{self.chpNum}" / os.path.basename(imgURL),
                "wb",
            )
            # Writing the img file, 100000 bytes per iteration.
            for chunk in res.iter_content(100000):
                file.write(chunk)

        finally:
            # Closing a file depending if an error occured or not.
            file.close()
