"""
"@Author  :   Siddharth Mittal",
"@Contact :   siddharth.mittal@meduniwien.ac.at",
"@License :   (C)Copyright 2025, Medical University of Vienna",
"@Desc    :   Utility to auto-set paths in a GEMpRF configuration XML file.",
"""

import os
from lxml import etree
from utils.xml_utils import update_xml_value 

def auto_path_setting(config_filepath):

    config_filepath = os.path.abspath(config_filepath)
    if not os.path.isfile(config_filepath):
        print("\033[91mConfiguration file not found at:", config_filepath, "\033[0m")
        return False

    # derive repo root
    repo_root = os.path.dirname(os.path.dirname(config_filepath)).replace("\\", "/")
    stimuli_dir = os.path.join(repo_root, "example_data", "stimuli").replace("\\", "/")
    study_basepath = os.path.join(repo_root, "example_data").replace("\\", "/")

    # ---- parse ONCE ----
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(config_filepath, parser)
    root = tree.getroot()

    # --- 1) stimulus/directory ---
    nodes = root.xpath("//stimulus/directory")
    if nodes:
        nodes[0].text = stimuli_dir

    # --- 2) BIDS basepath ---
    nodes = root.xpath("//input_datasrc/BIDS/basepath")
    if nodes:
        nodes[0].text = study_basepath

    # --- 3) fixed_paths / stimulus_filepath ---
    nodes = root.xpath("//fixed_paths/stimulus_filepath")
    if nodes:
        nodes[0].text = os.path.join(
            stimuli_dir, "task-bar_apertures.nii.gz"
        ).replace("\\", "/")

    # --- 4) fixed_paths / measured_data_filepath / filepath ---
    filepath_nodes = root.xpath("//fixed_paths/measured_data_filepath/filepath")
    for fp in filepath_nodes:
        filename = os.path.basename(fp.text)
        fp.text = os.path.join(
            study_basepath,
            "derivatives", "prfprepare", "analysis-01",
            "sub-001", "ses-001", "func",
            filename
        ).replace("\\", "/")

    # --- 5) fixed_paths results/basepath ---
    nodes = root.xpath("//fixed_paths/results/basepath")
    if nodes:
        nodes[0].text = os.path.join(
            study_basepath, "derivatives", "prfanalyze-gem",
            "analysis-ex001-results"
        ).replace("\\", "/")

    # ---- WRITE ONCE ----
    tree.write(config_filepath, pretty_print=True, encoding="UTF-8", xml_declaration=True)

    return True