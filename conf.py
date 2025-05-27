autor = "Abdullah Temur - OG-Brain.com"
copyright_ = "Copyright 2025 OG-Brain.com, Abdullah Temur. All rights reserved."
default_media_description = "Media for OG-Brain.com"
keywords = ["OG-Brain", "Abdullah Temur", "Bio-inspired AI"]
media_title_prefix = "OG-Brain.com "
directory_title_prefix = "OG-Brain.com directory "
default_directory_description = "Directory metadata file"

# leave string empty, if there is no need to insert jsonld into html
add_metadata_json_to_html_file = ""

default_name_jsonld_file = "media_jsonld.json"

website = "https://www.og-brain.com/"

# in case you want custom description for your media in the jsonld
custom_descriptions = {
    "emitting.gif": "Neurons Emitting electricity",
    "electricity.jpg": "General overview of some features, including electricity, branching/growing...",
    "component_arrangement.gif": "Showcase Example of Arranging Neuron Components 1",
    "component_arrangement_alt.jpg": "Showcase Example of Arranging Neuron Components 2",
    "path_finding_2.jpg": "a neuron calculating the shortest path",
    "detection.mp4": "objects can sense other objects and electromagnetic waves",
    "branch_creation.mp4": "Customizable branching options based on specific conditions and thresholds",
    "clustering.mp4": "OG-Brain can mimic microevolution and cluster objects based on several conditions",
    "final_form.mp4": "Final video showcasing OG-Brain's major features"
}

# default json ld head
json_ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "CreativeWork",
            "license": f"{website}license.txt",
            "description": default_media_description,
            "author": {
                "@type": "Person",
                "name": autor
            }
        },
    ]
}