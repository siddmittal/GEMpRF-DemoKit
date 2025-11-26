"""
"@Author  :   Siddharth Mittal",
"@Contact :   siddharth.mittal@meduniwien.ac.at",
"@License :   (C)Copyright 2025, Medical University of Vienna",
"@Desc    :   Demo script to run GEMpRF with optional interactive config selection,
               auto path setting, and GPU memory check.",     
"""

import gemprf as gp

CONFIG_FILEPATH = r"D:/GEMpRF_Demo/sample_configs/example-001_runtype-individual_input-bids_desc-analyse-prfprepare-data.xml"

if __name__ == "__main__":
    interactively_choose_config_file = True
    run_auto_path_setting = True
    run_auto_gpu_check = True
    
    # (OPTIONAL) choose config file interactively
    if interactively_choose_config_file:
        from utils.config_library import choose_config
        CONFIG_FILEPATH = choose_config()

    # (OPTIONAL) path settings - only to assist you    
    if run_auto_path_setting:
        print("\033[38;5;208m" + "\n\nAUTO path setting is running...\nYour config file will be updated with the correct paths relative for this demo program.\n"
            "If you prefer to set paths manually, edit the XML configuration file and comment out this step.\n" + "\033[0m")
        from utils.auto_path import auto_path_setting
        auto_path_setting(CONFIG_FILEPATH)    

    # (OPTIONAL) GPU memory check — only to assist you
    final_config = CONFIG_FILEPATH    
    if run_auto_gpu_check:
        from utils.gpu_info import analyze_gpus, handle_gpu_decision
        print("\nChecking GPU availability...\n")

        final_config = handle_gpu_decision(analyze_gpus(), CONFIG_FILEPATH)
        if final_config is None:
            print("\033[91mExiting due to insufficient GPU memory.\033[0m")
            exit(1)

    # (THE REAL DEAL)
    # Run GEMpRF analysis based on configuration file
    gp.run(final_config)
    print("GEMpRF analysis complete.")