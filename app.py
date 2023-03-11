#! python3
# app.py - Starts the Scraper for the manga provided in the command-line-argument.

import os, sys, shelve
from time import time
from Scrapers.TCB_Scans import Scraper


# This is the main function of the program that manages all that is going in the program.
def main():
    # Making a Storage Dir
    os.makedirs("Downloaders", exist_ok=True)
    os.chdir("Downloaders")

    # Avaiable downloaders.
    downloaders = shelve.open("shelf")

    # Checking if the user wants to download a manga or wants to add downloader for another manga
    if sys.argv[1] == "save":
        downloaders[sys.argv[2]] = sys.argv[3]
        return

    # Getting the command-line-argument.
    mangaName = sys.argv[1]

    # Checking if the program can or connot download the specified manga.
    if mangaName not in downloaders.keys():
        print(f"Sorry, We don't currently have a downloader for {mangaName}.")
        return

    # Downloads the appropriate Manga.
    for name, url in downloaders.items():
        if mangaName != name:
            continue

        # Changing Directory to the downloads directory.
        os.chdir("../")
        os.makedirs("Downloads", exist_ok=True)
        os.chdir("Downloads")

        # Downloading
        manga = Scraper(url)
        manga.download()

        # Changing Directory to the downloaders directory.
        os.chdir("../Downloaders")

        break

    # Closing the downloaders Shelf.
    downloaders.close()


if __name__ == "__main__":
    # Start the timer and Calls main function.
    try:
        startTime = time()
        main()

    # Stops the timer and Handels the KeyboardInterupt Exception.
    except KeyboardInterrupt:
        endTime = time()
        print("Stopped.")

    # Stops the timer and prints Done.
    else:
        endTime = time()
        print("Done.")

    # prints the total time the scraper ran.
    finally:
        timeTaken = endTime - startTime
        print(f"Took {round(timeTaken, 2)}s")
        sys.exit()
