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
            (
                (.*?-)          # Group5 - "chapter-"
                ((\d|\.)+)      # Group6 - Chapter Number
            )    
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

    def total_size(self):
        # Size in bytes.
        total_size = 0

        # Walking the directory to get total_size.
        for dirpath, dirnames, filenames in os.walk(Path.cwd()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        # Size in GBs
        gbs, reminder = divmod(total_size, 1000000000)
        # Size in MBs
        mbs, bytes = divmod(reminder, 1000000)

        print(f"\nSize:\t{round(gbs):02}GBs , {round(mbs):02}MBs")

    def totalRangeSize(self, sChp, eChp):
        # List of the chapter names which were downloaded.
        downloadedDirs = []

        # Adding name to downloadedDirs.
        for num in range(int(sChp), int(eChp) + 1):
            downloadedDirs.append(f"Chapter_{num}")

        # Size in bytes.
        total_size = 0

        # Walking the directory to get total_size.
        for dirpath, dirnames, filenames in os.walk(Path.cwd()):
            for f in filenames:
                if os.path.basename(dirpath) in downloadedDirs:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)

        # Size in GBs
        gbs, reminder = divmod(total_size, 1000000000)
        # Size in MBs
        mbs, bytes = divmod(reminder, 1000000)

        print(f"\nSize:\t{round(gbs):02}GBs , {round(mbs):02}MBs")

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
            self.chpNum = self.URLRegex.search(self.cURL).group(6)

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

        # Printing the total size of the download.
        self.total_size()

    def downloadSingleChapter(self, chpNum):
        # Getting the Chapter Number.
        self.chpNum = chpNum

        # Parsing the first chapter URL.
        search = self.URLRegex.search(self.cURL)

        # Setting-up the chapter URL.
        self.cURL = (
            search.group(1)
            + search.group(2)
            + search.group(3)
            + search.group(5)
            + self.chpNum
        )

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

        # Changing working directory to download chapter directory.
        os.chdir("Chapter_%s" % self.chpNum)

        # Printing the total size of the download.
        self.total_size()

        # Changing working directory back to manga directory.
        os.chdir("../")

    def downloadRange(self, startChp, endChp):
        for chpNum in range(int(startChp), int(endChp) + 1):
            # Getting the Chapter Number.
            self.chpNum = chpNum

            # Parsing the first chapter URL.
            search = self.URLRegex.search(self.cURL)

            # Setting-up the chapter URL.
            self.cURL = (
                search.group(1)
                + search.group(2)
                + search.group(3)
                + search.group(5)
                + str(self.chpNum)
            )

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

        # Printing the total size of the download.
        self.totalRangeSize(startChp, endChp)

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
