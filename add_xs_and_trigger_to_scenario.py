import os
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from pathlib import Path
from config import GeneralConfig


def add_xs_and_triggers_to_scenario(
    scenario_path: str,
    xs_script_path: str,
    output_path: str,
    xs_timer_loop: int = 1,
):
    """
    Modifies an AoE2 scenario by adding an XS script which will regularly read
    the XS variables into trigger variables and write them back.

    :param scenario_path: Path to the original .aoe2scenario file.
    :param xs_script_path: Path to the XS script file.
    :xs_func_name: Name of the XS function (in the XS script mentioned above) to call.
    :param output_path: Path to save the modified scenario.
    :param num_vars: Number of XS variables to handle.
    :param xs_timer_loop: How often will the XS script fire, in AoE2 in-game seconds? (default is 1).
    """
    # Load the scenario
    scenario = AoE2DEScenario.from_file(scenario_path)

    # Add a trigger to call the XS 'main' function every second
    trigger_manager = scenario.trigger_manager
    xs_trigger = trigger_manager.add_trigger(
        "XS Main Loop",
        looping=True,
    )
    xs_trigger.new_condition.timer(timer=xs_timer_loop)

    with open(xs_script_path, "r", encoding="utf-8") as f:
        script_as_message = f.read()
    xs_trigger.new_effect.script_call(message=script_as_message)

    # NOTE You can now add triggers that use XS variables to perform actions.

    # Save the modified scenario

    # Ensure we check the XS upon writing
    scenario.xs_manager.xs_check.enabled = True
    scenario.xs_manager.xs_check.raise_on_error = False

    scenario.write_to_file(output_path)
    print(f"Modified scenario saved to: {output_path}")


if __name__ == "__main__":

    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    config = GeneralConfig()

    add_xs_and_triggers_to_scenario(
        scenario_path=config.scenario_path_input,
        xs_script_path=f"{this_file_dir}/my_comm.xs",
        output_path=config.scenario_path_output,
    )
