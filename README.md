# aoe2-xs-comm
A framework to communicate between Age of Empires II's XS script and external Python code.


This project allows communication between Age of Empires II DE's XS scripting engine and a Python GUI. The GUI is accessible in a local web browser. Communication is achieved by setting trigger variables, which can be used by triggers in a scenario.


## Usage guide


### Installation

- Age of Empires II: Definitive Edition installed.
- Python 3.7 or higher installed.

Install prerequisites

```bash
pip install gradio AoE2ScenarioParser
```

Create a scenario in the Scenario Editor according to your tastes and save it


### Launching

- Change the parameters in config.py, notably your ID and the name of the scenario
- Run the add_xs_and_trigger_to_scenario.py file. This will modify the scenario with the specified name.
- Launch AoE II and launch the scenario with the "_MODIFIED" suffix (either testing in editor or in skirmish). This will create a xsdat file and wait for sync
- Now, launch the xs_comm_gui.py Python script, which will launch the gradio GUI


### Usage

- You can now connect to the GUI at 127.0.0.1:7860 (by default)
- Set values for trigger variables and click **Send to XS**.
- Live XS values are displayed and update every second.

## Development

In add_xs_and_trigger_to_scenario.py, there is space for trigger logic. Also in the XS script. Also in the xs_comm_gui.py file. You can add your own logic there. Currently, nothing is done with the variables.

For now, the variables passed are trigger variables, but further trigger or xs modifications could be used to pass AI script variables, goals, etc.

The goal of this repository is just to be a proof of concept that this is possible and straightforward.






- Ensure the variable count matches in Python and XS code.
- Use Trigger Variable indices in AoE2 to drive scenario logic.
- Add more logic to XS and Python for complex demos (e.g., strategic number setting, AI control).


- By default, this will use the trigger variables 0 to NUM_VARS, so be careful if you are using those. There is a position in the code to add potentially another lock so the game can signal it's done using them, but for now it's not implemented



## Contact and Informations

MIT License

Original link: https://github.com/qferre/aoe2-xs-comm

quentin.q.ferre@gmail.com


Thanks to https://ksneijders.github.io/AoE2ScenarioParser/getting_started/ and https://ugc.aoe2.rocks/general/xs/programmer/