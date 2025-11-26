"""
"@Author  :   Siddharth Mittal",
"@Contact :   siddharth.mittal@meduniwien.ac.at",
"@License :   (C)Copyright 2025, Medical University of Vienna",
"@Desc    :   Utility functions for XML manipulation in GEMpRF.",
"""

from lxml import etree
import shutil

def update_xml_value(filepath, xpath, new_value):
    """
    Update the text content of a single XML node without disturbing
    formatting, comments, or attributes.
    """
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(filepath, parser)
    root = tree.getroot()

    nodes = root.xpath(xpath)
    if not nodes:
        raise ValueError(f"XPath not found: {xpath}")

    # Only update text, leave attributes and structure unchanged
    nodes[0].text = str(new_value)

    tree.write(filepath, pretty_print=True, encoding="UTF-8")

def create_coarse_grid_config(original_xml, coarse_xml_path):
    """
    Create a copy of the config file and modify:
        num_horizontal_prfs = 11
        num_vertical_prfs   = 11
        num_sigmas          = 5
    Without altering formatting or comments.
    """

    shutil.copy2(original_xml, coarse_xml_path)

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(coarse_xml_path, parser)
    root = tree.getroot()

    # Update spatial grid
    grid = root.xpath("//default_spatial_grid")
    if grid:
        grid[0].set("num_horizontal_prfs", "11")
        grid[0].set("num_vertical_prfs", "11")

    # Update sigma count
    sigmas = root.xpath("//default_sigmas")
    if sigmas:
        sigmas[0].set("num_sigmas", "5")

    tree.write(coarse_xml_path, pretty_print=True, encoding="UTF-8")

    return coarse_xml_path

