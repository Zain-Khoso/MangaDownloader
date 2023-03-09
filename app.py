#! python3.11.1
# app.py - Kickstarts the program by getting the manga name in the commandline-arguments
# and downloading the approprient manga.

import os, sys
from pathlib import Path
from time import time
from Scrapers.OnePiece import download_OnePiece_Manga
from Scrapers.AceNovel import download_AceNovel_Manga


# This is the main function of the program that manages all that is going in the program.
def main():
    # Getting the root working directory of the program and the command-line-argument.
    rootDir = Path.cwd()
    mangaName = sys.argv[1]

    # Setting up the downloaders that are available.
    downloaders = ["OnePiece", "AceNovel"]

    # Checking if the program can or connot download the specified manga.
    if mangaName not in downloaders:
        print(f"Sorry, We don't currently have a downloader for {mangaName}.")
        return

    # Changing the Current-Working-Directory to the Newly-Created /
    # An-Existing downloads directory.
    os.makedirs(f"{mangaName}-Manga", exist_ok=True)
    os.chdir(rootDir / f"{mangaName}-Manga")

    # Checks the manga name once again and determinds which module to call.
    if mangaName == "OnePiece":
        # Call to download_OnePiece_Manga funtion inside Scraper.OnePiece module.
        # Which downloads the appropriate manga.
        download_OnePiece_Manga()
    
    elif mangaName == "AceNovel":
        # Call to download_AceNovel_Manga funtion inside Scraper.AceNovel module.
        # Which downloads the appropriate manga.
        download_AceNovel_Manga()


if __name__ == "__main__":
    try:
        startTime = time()
        main()
    except KeyboardInterrupt:
        endTime = time()
        print("Stopped.")
    else:
        endTime = time()
        print("Done.")
    finally:
        timeTaken = endTime - startTime
        print(f"Took {round(timeTaken, 2)}s")
        sys.exit()
