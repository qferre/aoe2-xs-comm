# AoE2 XS Communication Debugger

This project allows communication between Age of Empires II DE's XS scripting engine and a Python GUI.

## 🔧 Files

- `my_comm.xs` – XS script that reads/writes data from a binary file.
- `xs_comm_gui.py` – Python script with a Gradio GUI and a background sync thread.
- `xs_data_file.xsdat` – Binary file used for data exchange (created automatically).

## 🚀 Usage

### Setup in Age of Empires II DE

1. Place `my_comm.xs` into:
   ```
   C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources_common\xs\
   ```

2. In the **Scenario Editor**:
   - In the **Map Tab**, set the script filename to `my_comm`
   - Create a new Trigger:
     - **Condition**: Timer = 1 second
     - **Effect**: Script Call → `main`

### Run the Python Interface

Make sure you have Python 3 and install the required dependency:

```bash
pip install gradio AoE2ScenarioParser
```

Then launch the GUI:

```bash
python xs_comm_gui.py 
```

### Use the GUI

- Set values for trigger variables and click **Send to XS**.
- Live XS values are displayed and update every second.

## 📌 Notes

- You can edit `NUM_VARS` in both the XS and Python files to change the number of variables.
- Ensure `xs_data_file.xsdat` is accessible from both Python and the AoE2 XS script.

Enjoy your programmable empire.
