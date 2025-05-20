
# AoE2 XS Communication System - README


This guide explains how to use the Age of Empires II communication system
based on XS scripting and a Python daemon.


## Prerequisites


- Age of Empires II: Definitive Edition installed.
- Python 3.7 or higher installed.
- Gradio installed via pip:

    pip install gradio

----------------------------
## Files Overview
----------------------------

- my_comm.xs              : XS script for in-game variable polling and actions.
- xs_comm_gui.py          : Python script with Gradio GUI for interacting with variables.
- xs_data_file.xsdat      : Shared binary data file for communication (auto-created).
- scenario_MODIFIED.aoe2scenario : Scenario file modified to include XS script and triggers.

----------------------------
## Step-by-Step Instructions
----------------------------

1. Place the XS Script:
-----------------------
Copy 'my_comm.xs' to:

    C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources_common\xs\

(Adjust the path based on your actual installation.)

2. Modify the Scenario:
-----------------------
Use the provided Python script/function to patch your scenario:

    from your_module import add_xs_and_triggers_to_scenario

    add_xs_and_triggers_to_scenario(
        scenario_path="path/to/original_scenario.aoe2scenario",
        xs_script_path="path/to/my_comm.xs",
        output_path="path/to/scenario_MODIFIED.aoe2scenario",
        num_vars=4
    )

This injects the XS script and adds automatic triggers to use variables.

3. Launch the Python Daemon:
----------------------------
Run the Gradio interface to manipulate the variables:

    python xs_comm_gui.py

This opens a browser window where you can view/edit variables in real-time.

4. Run the Modified Scenario:
-----------------------------
- Open AoE2:DE.
- Load 'scenario_MODIFIED.aoe2scenario' in the Scenario Editor or start a game.
- The XS script polls every second, performs actions based on variables, and prints debug info to chat.

----------------------------
## Tips
----------------------------

- Ensure the variable count matches in Python and XS code.
- Use Trigger Variable indices in AoE2 to drive scenario logic.
- Add more logic to XS and Python for complex demos (e.g., strategic number setting, AI control).

Enjoy experimenting!
