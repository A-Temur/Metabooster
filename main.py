"""
Copyright 2025 github.com/A-Temur, Abdullah Temur. All rights reserved.
"""
import datetime

from PIL import Image
from bs4 import BeautifulSoup
from easygui import diropenbox, enterbox
from mutagen.mp4 import MP4
from shutil import copytree
from os.path import basename, splitext
import os
import subprocess
import yaml
import json
import re
import exiftool
from conf import *


def check_and_write_comment(search_str_, file_writer_, original_content_, new_content_, css=True):
    if css:
        finder = re.findall(r"(?s)/\*.*?\*/", original_content)
    else:
        finder = re.findall(r"(?s)<!--.*?-->", original_content)
    if len(finder) > 0:
        if search_str_ in finder[0]:
            new_content_ = original_content_.replace(finder[0], new_content_)
        else:
            new_content_ = new_content_ + "\n" + original_content
    else:
        new_content_ = new_content_ + "\n" + original_content
    file_writer_.write(new_content_)

def add_img_to_jsonld(metadata_jsonld_, file_name_, file_path_):
    # update name and id
    metadata_jsonld_["name"] += file_name_
    metadata_jsonld_["@id"] += file_name_
    # paste path
    relative_path = os.path.relpath(file_path_, working_directory)
    relative_path = relative_path.replace(os.sep, "/")
    # noinspection PyTypeChecker
    metadata_jsonld_["contentUrl"] = website + relative_path
    # append to json-ld
    json_ld["@graph"].append(metadata_jsonld_)

def get_video_duration(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", video_path],
        capture_output=True, text=True
    )
    metadata = json.loads(result.stdout)
    duration = float(metadata["format"]["duration"])
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    iso_duration = f"PT{minutes}M{seconds}S"
    return iso_duration

def add_metadata_to_heic_image(file_path_, metadata_, file_name_, metadata_jsonld_):
    try:
        file_name_extended = basename(file_path_)

        # append filename into metadata title
        metadata_["Title"] += file_name_
        # add custom description if available
        if file_name_extended in custom_descriptions.keys():
            metadata_["ImageDescription"] = custom_descriptions[file_name_extended]

        with exiftool.ExifToolHelper() as et:
            et.set_tags(file_path_, tags=metadata_,
                        params=["-P", "-overwrite_original"])
            # -P parameter preservers original modification date

        add_img_to_jsonld(metadata_jsonld_, file_name_, file_path_)
        print(f"Created modified image: {file_path_}")
    except Exception as e:
        print(f"Error processing image {file_path_}: {e}")

def add_metadata_to_image(file_path_, metadata_, file_name_, metadata_jsonld_):
    try:
        img = Image.open(file_path_)
        exif_data = img.getexif()

        file_name_extended = basename(file_path_)

        # append filename into metadata title
        metadata_["40091"] += file_name_.encode("utf-16le")
        # add custom description if available
        if file_name_extended in custom_descriptions.keys():
            metadata_["270"] = custom_descriptions[file_name_extended]

        for tag, value in metadata_.items():
            exif_data[int(tag)] = value

        img.save(file_path_, exif=exif_data)

        add_img_to_jsonld(metadata_jsonld_, file_name_, file_path_)
        print(f"Created modified image: {file_path_}")
    except Exception as e:
        print(f"Error processing image {file_path_}: {e}")


def add_metadata_to_video(file_path_, metadata_, file_name_, metadata_jsonld_):
    try:
        if file_path_.lower().endswith(".mp4"):

            video = MP4(file_path_)
            custom_description_available = False
            file_name_extended = file_name_ + ".mp4"

            # append filename into metadata title
            metadata_["\xa9nam"] += file_name_
            # add custom description if available
            if file_name_extended in custom_descriptions.keys():
                custom_description_available = True
                metadata_["\xa9des"] = custom_descriptions[file_name_extended]

            for tag, value in metadata_.items():
                video[tag] = value

            video.save()

            # update name and id
            metadata_jsonld_["name"] += file_name_
            metadata_jsonld_["@id"] += file_name_
            # paste path
            relative_path  = os.path.relpath(file_path_, working_directory)
            relative_path = relative_path.replace(os.sep, "/")
            # noinspection PyTypeChecker
            metadata_jsonld_["contentUrl"] = website + relative_path
            # calc and paste duration
            metadata_jsonld_["duration"] = get_video_duration(file_path_)
            # generate and paste thumbnailUrl
            thumbnail_name = file_name_ + "_thumbnail.jpg"
            thumbnail_url = relative_path.replace(file_name_ + ".mp4", thumbnail_name)
            # noinspection PyTypeChecker
            metadata_jsonld_["thumbnailUrl"] = website + thumbnail_url
            # add custom description if any
            if custom_description_available:
                metadata_jsonld_["description"] = custom_descriptions[file_name_extended]
            # append to json-ld
            json_ld["@graph"].append(metadata_jsonld_)
            print(f"Created modified video: {file_path_}")
        else:
            print(f"Skipping non-MP4 video file: {file_path_}")
    except Exception as e:
        print(f"Error processing video {file_path_}: {e}")


def add_metadata_to_gif(file_path_, metadata_, file_name_, metadata_jsonld_):
    try:
        # append filename to title
        metadata_["Title"] += file_name_

        file_name_extended = file_name_ + ".gif"

        # add custom description if available
        if file_name_extended in custom_descriptions.keys():
            metadata_["Description"] = custom_descriptions[file_name_extended]

        for key, value in metadata_.items():
            cmd = ["exiftool", f"-{key}={value}", file_path_]
            subprocess.run(cmd, check=True)

        add_img_to_jsonld(metadata_jsonld_, file_name_, file_path_)
        print(f"Created modified image: {file_path_}")
        # exiftool automatically keeps the original file, delete it
        os.remove(file_path_ + "_original")
    except Exception as e:
        print(f"Error adding metadata to {file_path_}: {e}")


def get_html_css_comment(file_name_, html=True):
    metadata_ = metadata_html_css.copy()
    metadata_["Description"] = f"{file_name_} for {media_title_prefix}"
    metadata_ = "\n".join(f"{k}: {v}" for k, v in metadata_.items())
    if html:
        comment = html_brackets[0] + "\n" + metadata_ + "\n" + html_brackets[1]
    else:
        comment = css_brackets[0] + "\n" + metadata_ + "\n" + css_brackets[1]
    return comment


if __name__ == "__main__":
    # Convert string keys to EXIF tag IDs if possible
    # from PIL.ExifTags import TAGS
    # exif_tag_map = {TAGS[key]: key for key in TAGS if isinstance(key, int)}
    default_date = datetime.datetime.now().isoformat()


    # for images
    metadata_img = {
        "40091": media_title_prefix.encode("utf-16le"),  # title, must be encoded also
        "315": autor,  # artist
        "40093": autor.encode("utf-16le"),  # autor
        "33432": copyright_,  # copyright
        "270": default_media_description,  # description
        "40094": ", ".join(keywords).encode("utf-16le")  # keywords comma separated string
    }
    metadata_json_ld_img = {
        "@type": "ImageObject",
        "@id": "#",
        "contentUrl": "",
        "name": media_title_prefix
    }

    # for videos
    metadata_vid = {
        "\xa9nam": media_title_prefix,  # title
        "\xa9ART": autor,  # artist
        "cprt": copyright_,  # copyright
        "\xa9des": default_media_description,  # description
        "\xa9key": keywords  # keywords as list
    }

    metadata_json_ld_vid = {
        "@type": "VideoObject",
        "@id": "#",
        "name": media_title_prefix,
        "thumbnailUrl": "",
        "contentUrl": "",
        "duration": "",
        "description": default_media_description
    }

    # for gifs
    metadata_gif = {
        "Title": media_title_prefix,
        "Author": autor,
        "Comment": default_media_description,
        "Rights": copyright_,
        "Subject": "; ".join(keywords),  # keywords semicolon separated string
        "Description": default_media_description,
        "Creator": autor
    }

    # for directories
    metadata_yaml = {
        "title": directory_title_prefix,
        "author": autor,
        "description": default_directory_description,
        "keywords": ", ".join(keywords),
        "copyright": copyright_,
        "created": default_date,
    }

    # for css and html files
    metadata_html_css = {
        "Author": autor,
        "Description": default_directory_description,
        "Copyright": copyright_,
        "Keywords": ", ".join(keywords),
    }

    # for heic images
    metadata_heic = {
        "Title": media_title_prefix,
        "Artist": autor,
        "Copyright": copyright_,
        "ImageDescription": default_media_description,
    }

    html_brackets = ("<!--", "-->")
    css_brackets = ("/*", "*/")

    directory = diropenbox("Enter the parent directory: ")

    if directory:
        final_dir_name = enterbox("Enter destination directory name")

        if final_dir_name:
            original_dir_name = basename(directory)

            final_dir = directory.replace(original_dir_name, final_dir_name)

            copytree(directory, final_dir)

            working_directory = final_dir

            for root, dirs, files in os.walk(final_dir):

                # create metadata file for each directory
                for dir_name in dirs:
                    metadata_file = os.path.join(root, dir_name, ".metadata.yaml")

                    metadata_content = metadata_yaml.copy()
                    metadata_content["title"] += dir_name

                    with open(metadata_file, "w", encoding="utf-8") as f:
                        yaml.dump(metadata_content, f, default_flow_style=False, allow_unicode=True)
                # edit metadata of media (videos, images)
                for file in files:
                    file_path = os.path.join(root, file)

                    # get filename without extension
                    file_name = splitext(basename(file_path))[0]

                    if file.lower().endswith(".heic"):
                        metadata_heic_cpy = metadata_heic.copy()

                        # copy default json-ld for images
                        json_ld_img_cpy = metadata_json_ld_img.copy()

                        add_metadata_to_heic_image(file_path, metadata_heic_cpy, file_name, json_ld_img_cpy)

                    elif file.lower().endswith((".jpg", ".jpeg", ".png")):
                        metadata_img_cpy = metadata_img.copy()

                        # copy default json-ld for images
                        json_ld_img_cpy = metadata_json_ld_img.copy()

                        add_metadata_to_image(file_path, metadata_img_cpy, file_name, json_ld_img_cpy)
                    elif file.lower().endswith((".mp4", ".mov")):
                        metadata_vid_cpy = metadata_vid.copy()

                        # copy default json-ld for videos
                        json_ld_vid_cpy = metadata_json_ld_vid.copy()

                        add_metadata_to_video(file_path, metadata_vid_cpy, file_name, json_ld_vid_cpy)
                    elif file.lower().endswith(".gif"):
                        metadata_gif_cpy = metadata_gif.copy()

                        # copy default json-ld for images
                        json_ld_img_cpy = metadata_json_ld_img.copy()

                        add_metadata_to_gif(file_path, metadata_gif_cpy, file_name, json_ld_img_cpy)

                    elif file.lower().endswith(".html"):
                        # metadata_html = metadata_html_css.copy()
                        # metadata_html["Description"] = f"{file_name} for {media_title_prefix}"
                        # metadata_html = "\n".join(f"{k}: {v}" for k, v in metadata_html.items())
                        # html_comment = html_brackets[0] + "\n" + metadata_html + "\n" + html_brackets[1]
                        html_comment = get_html_css_comment(file_name)
                        with open(file_path, "r", encoding="utf-8") as html_file:
                            original_content = html_file.read()

                        if html_comment not in original_content:
                            with open(file_path, "w", encoding="utf-8") as html_file:
                                check_and_write_comment("Copyright:", html_file, original_content, html_comment, False)

                    elif file.lower().endswith(".css"):
                        # metadata_css = metadata_html_css.copy()
                        # metadata_css["Description"] = f"{file_name} for {media_title_prefix}"
                        # metadata_css = "\n".join(f"{k}: {v}" for k, v in metadata_css.items())
                        # css_comment = css_brackets[0] + "\n" + metadata_css + "\n" + css_brackets[1]
                        css_comment = get_html_css_comment(file_name, False)
                        with open(file_path, "r", encoding="utf-8") as css_file:
                            original_content = css_file.read()

                        if css_comment not in original_content:
                            with open(file_path, "w", encoding="utf-8") as css_file:
                                check_and_write_comment("Copyright:", css_file, original_content, css_comment, True)

                    else:
                        print(f"Skipping unsupported file: {file_path}")

            # Save JSON content to a file
            with open(os.path.join(final_dir, default_name_jsonld_file), "w", encoding="utf-8") as json_file:
                # json.dump(... ensure_ascii=False, if you want to allow non-Ascii chars)
                # noinspection PyTypeChecker
                json.dump(json_ld, json_file, indent=4)

            if bool(add_metadata_json_to_html_file):

                # add metadata json to html
                html_file_path = os.path.join(final_dir, add_metadata_json_to_html_file)

                with open(html_file_path, "r", encoding="utf-8") as html_reader:
                    original_html = html_reader.read()

                prettified_html = BeautifulSoup(original_html, "html.parser")

                script_element = prettified_html.find("script", attrs={"type": "application/ld+json"})
                script_element_exists_in_original = True
                if not script_element:
                    script_element_exists_in_original = False
                    new_script_element = prettified_html.new_tag("script", type="application/ld+json")
                    new_script_element.string = json.dumps(json_ld, indent=4)
                    prettified_html.find("head").append(new_script_element)
                else:
                    script_element.string = json.dumps(json_ld, indent=4)

                prettified_html = prettified_html.prettify()
                pretty_script_part = re.search(r'<script type="application/ld\+json">(.*?)</script>', prettified_html,
                                               re.DOTALL | re.IGNORECASE).group()
                if not script_element_exists_in_original:
                    final_html = re.sub(r'</head>', f"{pretty_script_part + "\n" + "</head>"}",
                                        original_html,
                                        flags=re.DOTALL | re.IGNORECASE)
                else:
                    final_html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', pretty_script_part,
                                        original_html,
                                        flags=re.DOTALL | re.IGNORECASE)

                with open(html_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write(final_html)

