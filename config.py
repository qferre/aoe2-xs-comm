USERNAME = "Quentin"  # Windows username
PROFILE_ID = 76561198007343704  # Profile ID
SCENARIO_NAME = "Testing"  # Scenario name without extension

# You should not need to change anything below this line
# ---------------------------------------------------------------------------- #

from pathlib import Path


class GeneralConfig:

    def __init__(
        self,
        username: str = USERNAME,
        profile_id: int = PROFILE_ID,
        scenario_name: str = SCENARIO_NAME,
        poll_interval: float = 1,
        num_vars: int = 4,
    ):
        """
        General configuration. If you leave default arguments, remember to change the username, ID, and scenario name in the config.py file!

        Automatically deduces file paths. They are currently hardcoded for Windows, but they should be
        relative to the profile ID and scenario name.

        :param username: Windows username
        :param profile_id: Profile ID
        :param scenario_name: Scenario name without extension
        :param poll_interval: Polling interval in seconds for the GUI
        :param num_vars: Number of XS variables to handle
        """

        ## ---------------- PATH PARAMETERS ---------------- ##

        self.username = username
        self.profile_id = profile_id
        self.scenario_name = scenario_name

        # Deduce the scenario path from the profile, ID and scenario name
        self.scenario_path_input = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/resources/_common/scenario/{self.scenario_name}.aoe2scenario"
        )
        self.scenario_path_output = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/resources/_common/scenario/{self.scenario_name}_MODIFIED.aoe2scenario"
        )

        # Deduce the xsdat path as well
        self.xsdat_path = Path(
            f"C:/Users/{self.username}/Games/Age of Empires 2 DE/{self.profile_id}/profile/{self.scenario_name}_MODIFIED.xsdat"
        )

        ## ---------------- PYTHON PARAMETERS ---------------- ##
        self.poll_interval = poll_interval

        ## ---------------- XS PARAMETERS ---------------- ##
        self.NUM_VARS = num_vars

        self.LOCK_PYTHON_DONE = 0   # Value of the lock when Python is done
        self.LOCK_XS_DONE = 1       # Value of the lock when XS is done
