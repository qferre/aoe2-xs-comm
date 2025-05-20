import os
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.units import UnitInfo
from pathlib import Path

def add_xs_and_triggers_to_scenario(
    scenario_path: str, xs_script_path: str, output_path: str,
):
    """
    Modifies an AoE2 scenario by adding an XS script and triggers that use XS variables.

    :param scenario_path: Path to the original .aoe2scenario file.
    :param xs_script_path: Path to the XS script file.
    :xs_func_name: Name of the XS function (in the XS script mentioned above) to call.
    :param output_path: Path to save the modified scenario.
    :param num_vars: Number of XS variables to handle.
    """
    # Load the scenario
    scenario = AoE2DEScenario.from_file(scenario_path)


    # Add a trigger to call the XS 'main' function every second
    trigger_manager = scenario.trigger_manager
    xs_trigger = trigger_manager.add_trigger("XS Main Loop",
                                             looping =True,)
    xs_trigger.new_condition.timer(timer=5) # TODO put this back to 1


    with open(xs_script_path, 'r', encoding='utf-8') as f:
        script_as_message = f.read()
    xs_trigger.new_effect.script_call(message = script_as_message)


    ##### EXAMPLE TRIGGERS #####

    # # Add triggers that use XS variables to perform actions
    # for i in range(num_vars):
    #     trigger = trigger_manager.add_trigger(f"Use XS Var {i}")
    #     trigger.new_condition.timer(timer=2)  # Start after 2 seconds
    #     trigger.new_condition.trigger_variable...# If variable i == 1
    #     trigger.new_effect.create_object(
    #         object_list_unit_id=UnitInfo.PALADIN.ID,
    #         source_player=PlayerId.ONE,
    #         location_x=10 + i * 2,
    #         location_y=10,
    #     )

    # Save the modified scenario

    # Ensure we check the XS upon writing
    scenario.xs_manager.xs_check.enabled = True
    scenario.xs_manager.xs_check.raise_on_error = False

    scenario.write_to_file(output_path)
    print(f"Modified scenario saved to: {output_path}")


if __name__ == "__main__":

    this_file_dir = os.path.dirname(os.path.abspath(__file__))

    PATH_ROOT = Path(
        "C:/Users/Quentin/Games/Age of Empires 2 DE/76561198007343704/resources/_common/scenario/"
    )

    add_xs_and_triggers_to_scenario(
        scenario_path=f"{PATH_ROOT}/Testing.aoe2scenario",
        xs_script_path=f"{this_file_dir}/my_comm.xs",
        output_path=f"{PATH_ROOT}/Testing_MODIFIED.aoe2scenario",
    )
    # Example usage
