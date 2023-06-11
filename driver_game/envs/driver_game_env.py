import gymnasium
import numpy as np
import gymnasium.spaces as spaces

class DriverGameEnv(gymnasium.Env):
    def __init__(self, size=10) -> None:
        self.size = size
        self.points = 0
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Discrete(2),
                "enemy": spaces.Box(0, 2, shape=(self.size, 2), dtype=int),
            }
        )
        self.action_space = spaces.Discrete(2)
        self._action_to_direction = {
            0: 0,
            1: 1
        }

    # Obserwacje
    def _get_obs(self):
        return { "agent": self._agent_location, "enemy": self._enemy_location }
    
    # Informacja o punktach
    def _get_info(self):
        return { "points": self.points }
    
    # Reset gry
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.points = 0
        self._agent_location = self.np_random.integers(0, 2)
        self._enemy_location = np.array([0, 0])
        for i in range(0, self.size, 2):
            first_array = np.array([1, 0]) if self.np_random.integers(0, 2) == 0 else np.array([0, 1])
            second_array = np.array([0, 0])
            self._enemy_location = np.vstack([self._enemy_location, first_array])
            self._enemy_location = np.vstack([self._enemy_location, second_array])

        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    # Krok gry
    def step(self, action):
        direction = self._action_to_direction[action]
        self._agent_location = direction
        crashed = self._enemy_location[0][1] if self._agent_location == 1 else self._enemy_location[0][0]
        self.points = self.points if crashed == 1 else self.points + 1
        reward = -1 if crashed else 1 if self.points >= self.size else 0

        # Aktualizacja mapy
        self._enemy_location = np.delete(self._enemy_location, (0), axis=0)
        self._enemy_location = np.vstack([self._enemy_location, np.array([0, 0])])

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, reward != 0, False, info