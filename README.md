# MangaDownloader

## Installation:

### 1. Use git to download all the source code.

### 2. Use the command `python -m pip install -r requirements.txt`
#### Use this command to install all required pakages\modules.

### 3. Change the `app.py` file's name to `mangaDownloader.py`.

### 4. Add this repo folder to the environment variables so that you can use this Bot from anywhere on your machine.


## Usage:

### 1. `mangaDownloader.py downloadsDir <custom-path>`.
#### Use this command add a custom path to the folder where the mangas will be saved. 
#### If this is not set then the then the downloads will be saved in the root folder of this repo in a new directory called Downloads

### 2. `mangaDownloader.py downloadsDir`.
#### Use this command to get the location where the future downloads will be saved.

### 3. `mangaDownloader.py add <manga-name> <first-chapter-link>`.
#### Use this command to add a new manga downloader. or to change an existing one.

### 4. `mangaDownloader.py list`.
#### Use this command to get a list of all the available downloaders.

### 5. `mangaDownloader.py delete <manga-name>`.
#### Use this command to delete a particular manga-downloader.

### 6. `mangaDownloader.py <manga-name>`.
#### Use this command to download a particular manga. And that manga's downloader should be in the downloaders.

### 7. `mangaDownloader.py <manga-name> <chapter-number>`.
#### Use this command to download a particular manga's particular chapter. And that manga's downloader should be in the downloaders.

### 8. `mangaDownloader.py <manga-name> <start-chapter-number>  <end-chapter-number>`.
#### Use this command to download a particular manga's particular range of chapters. And that manga's downloader should be in the downloaders.
