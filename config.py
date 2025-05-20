USERNAME = "Quentin"  # Windows username
PROFILE_ID = 76561198007343704  # Profile ID
SCENARIO_NAME = "Testing"  # Scenario name without extension

# You should not need to change anything below this line
# ---------------------------------------------------------------------------- #

from pathlib import Path


class GeneralConfig:
    """
    General configuration for the application.
    """

    def __init__(self):

        # PATH ARGUMENTS

        self.username = USERNAME
        self.profile_id = PROFILE_ID
        self.scenario_name = SCENARIO_NAME

        # Deduce the scenario path from the profile ID and scenario name
        self.scenario_path_input = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/resources/_common/scenario/{self.scenario_name}.aoe2scenario"
        )
        self.scenario_path_output = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/resources/_common/scenario/{self.scenario_name}_MODIFIED.aoe2scenario"
        )

        # Deduce the xsdat path from the profile ID and scenario name
        self.xsdat_path = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/profile/{self.scenario_name}_MODIFIED.xsdat"
        )

        # Python parameters
        self.poll_interval = 1  # Polling interval in seconds
