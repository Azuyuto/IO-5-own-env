import os
from gymnasium.envs.registration import register
from driver_game.envs.driver_game_env import DriverGameEnv

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

register(
    id="DriverGame-v0",
    entry_point="driver_game.envs:DriverGameEnv",
)

__all__ = [
    DriverGameEnv.__name__,
]
