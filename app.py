#! python3
# app.py - Starts the Scraper for the manga provided in the command-line-argument.

import os, sys, shelve
from time import time
from pathlib import Path
from Scrapers.TCB_Scans import Scraper


# This is the main function of the program that manages all that is going in the program.
def main():
    # Setting-up the rootDir of the program.
    rootDir = Path.cwd()

    # Making a Storage Dir
    os.makedirs("Storage", exist_ok=True)
    os.chdir("Storage")

    # Getting the downloaders shelf.
    downloaders = shelve.open("downloaders")

    # Getting the settings shelf.
    settings = shelve.open("settings")

    # Setting-up the downloadsDir.
    settings.setdefault("downloadsDir", rootDir / "Downloads")

    # Checking if the user wants add downloader for another manga.
    if sys.argv[1] == "add" and len(sys.argv) == 4:
        downloaders[sys.argv[2]] = sys.argv[3]

    # Checking if the user wants delete downloader for another manga.
    elif sys.argv[1] == "delete" and len(sys.argv) == 3:
        del downloaders[sys.argv[2]]

    # Checking if the user wants a list of the availiable downloaders.
    elif sys.argv[1] == "list":
        # If the user has no downloaders
        if len(downloaders.keys()) == 0:
            print("You have no downloaders.")
            return

        # Printing all the downloaders
        for ind, key in enumerate(downloaders.keys()):
            print("%s. %s" % (ind + 1, key))

    # Checking if the user wants to see the custom path for downloads.
    elif sys.argv[1] == "downloadsDir" and len(sys.argv) == 2:
        # If the user has no settings.
        if len(settings.keys()) == 0:
            print("You have no Custom path setup.")
            print(
                "If you want to et one type: python app.py downloadsDir <custom-path>"
            )
            return

        # Printing Path
        print(settings["downloadsDir"])

    # Checking if the user wants to give a custom path for downloads.
    elif sys.argv[1] == "downloadsDir" and len(sys.argv) == 3:
        settings["downloadsDir"] = sys.argv[2]

    # Downloads the manga.
    else:
        # Getting the command-line-argument.
        mangaName = sys.argv[1]

        # Checking if the program can or connot download the specified manga.
        if mangaName not in downloaders.keys():
            print(f"You don't have a downloader for {mangaName}.")
            return

        # Downloads the appropriate Manga.
        for name, url in downloaders.items():
            if mangaName != name:
                continue

            # Changing Directory to the downloads directory.
            os.makedirs(Path(settings["downloadsDir"]), exist_ok=True)
            os.chdir(Path(settings["downloadsDir"]))

            # Creating the Scraper Object and downloading the whole manga.
            manga = Scraper(url)

            # Checking if the user wants to download whole manga or parts of it.
            if len(sys.argv) == 2:
                manga.download()

            elif len(sys.argv) == 3:
                # Downloads just the specified chapter.
                manga.downloadSingleChapter(sys.argv[2])

            elif len(sys.argv) == 4:
                manga.downloadRange(sys.argv[2], sys.argv[3])

            else:
                print("Insufficiant Arguments.")

            # Changing Directory to the downloaders directory.
            os.chdir(rootDir / "Storage")

            break

        # Closing the downloaders and settings Shelf.
        downloaders.close()
        settings.close()


if __name__ == "__main__":
    # Start the timer and Calls main function.
    try:
        startTime = time()
        main()

    # Stops the timer and Handels the KeyboardInterupt Exception.
    except KeyboardInterrupt:
        endTime = time()

    # Stops the timer and prints Done.
    else:
        endTime = time()

    # prints the total time the scraper ran.
    finally:
        total_seconds = endTime - startTime

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"Time:\t{round(hours):02} : {round(minutes):02} : {round(seconds):02}")
        print("\nDone.")
        sys.exit()
