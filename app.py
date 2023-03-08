#! python3.11.1
# app.py - Kickstarts the program by getting the manga name in the commandline-arguments
# and downloading the approprient manga.

from pathlib import Path
from OnePiece.main import download_OnePiece_Manga
import os, sys


# This is the main function of the program that manages all that is going in the program.
def main():
    # Getting the root working directory of the program and the command-line-argument.
    rootDir = Path.cwd()
    mangaName = sys.argv[1]

    # Setting up the downloaders that are available.
    downloaders = ["OnePiece"]

    # Checking if the program con or connot download the specified manga.
    if mangaName in downloaders:
        # Changing the Current-Working-Directory to the Newly-Created /
        # An-Existing downloads directory.
        os.makedirs(f"{mangaName}-Downloads", exist_ok=True)
        os.chdir(rootDir / f"{mangaName}-Downloads")

        # Checks the manga name once again and determinds which module to call.
        if mangaName == "OnePiece":
            # Downloads all the imgs one-by-one each with a new thread and
            # returns all the threads.
            threads = download_OnePiece_Manga()

            # Appending all the threads to the main thread
            for thread in threads:
                thread.join()
            return
        else:
            return

    else:
        print(f"Sorry, We don't currently have a downloader for {mangaName}.")
        return


if __name__ == "__main__":
    main()

    print("Done. ")

    sys.exit()
