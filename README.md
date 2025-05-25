# Metabooster

**Metabooster** is a small Python script that automatically adds metadata to supported files within a specified directory. It is designed to facilitate consistent metadata improving cross-referencing on the internet.

---

## Features

* **Metadata Injection**

  * Adds user-defined metadata to all supported files within the selected directory.
  * Injects metadata as comments into HTML and CSS files.
  * If appropriate the same metadata is reused for all supported files to maximize semantic linkage across content.

* **Directory Metadata**

  * Creates a `.metadata.yaml` file in each directory to store metadata contextually.
* **JSON-LD Generation**

  * Generates a `metadata.json` file containing a [JSON-LD](https://json-ld.org/) schema for use in HTML.
  * Optionally embeds the JSON-LD into a specified HTML file.
  * Supports custom descriptions for each media.
* **Non-destructive Operation**

  * Creates a copy of the original directory to preserve original content.
  * All operations are performed on the copied directory.

---
## Supported Files and Tags

| File Type         | Supported Extensions | Supported Metadata Tags                                                                                                   |
|-------------------|----------------------|---------------------------------------------------------------------------------------------------------------------------|
| **Images**        | `.png`, `.jpg`, `.jpeg` | `Author`, `Artist`, `Title`, `Description`, `Copyright`, `Keywords`                                                       |
| **Images (HEIC)** | `.heic`              | `Artist`, `Title`, `ImageDescription`, `Copyright`                                                                        |
| **Videos**        | `.mp4`, `.mov`,      | `Title`, `Artist`, `Copyright`, `Description`, `Keywords`                                                                 |
| **Videos (GIF)**  | `.gif`               | `Title`, `Author`, `Comment`, `Rights` (copyright), `Subject` (keywords), `Description`, `Creator`                        |
| **HTML**          | `.html`              | (added as comment on top of the file) `Author`, `Description`, `Copyright`, `Keywords`                                    |
| **CSS**           | `.css`               | same as html                                                                                                              |
| **Directories**   |                      | Saved in `.metadata.yaml` as key-value pairs: `Title`, `Author`, `Copyright`, `Description`, `Keywords`, `Created` (date) |

---

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/A-Temur/Metabooster.git
   ```
2. Edit `main.py` and define your metadata strings accordingly:
   * change line 185 to 223 with your metadata.
2. Run the script.
3. Select the source directory via the EasyGUI file picker.
4. Provide a name for the output directory. The script will create a copy with this name and apply all changes there.

---

## Requirements

* Python 3.13 with Tcl/Tk runtime (for easygui)
* exiftool (https://exiftool.org/) and Pip package PyExifTool
* ffmpeg (https://ffmpeg.org/download.html)
* on windows add exiftool and ffmpeg to PATH
* Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

---

## Notes

* on each startup, the script saves the current timestamp. The same timestamp is used for all supported metadata in order to increase the cross-references.