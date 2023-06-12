import gymnasium
import numpy as np
import gymnasium.spaces as spaces
import pygame

class DriverGameEnv(gymnasium.Env):
    metadata = {"render_modes": ["human"], "render_fps": 2}

    def __init__(self, size=10, render_mode=None) -> None:
        self.size = size
        self.points = 0
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Discrete(2),
                "obstacle": spaces.Box(0, 2, shape=(self.size, 2), dtype=int),
            }
        )
        self.action_space = spaces.Discrete(2)
        self._action_to_direction = {
            0: 0,
            1: 1
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        self.window = None
        self.clock = None


    # Obserwacje
    def _get_obs(self):
        return { "agent": self._agent_location, "obstacle": self._obstacle_location }
    
    # Informacja o punktach
    def _get_info(self):
        return { "points": self.points }
    
    # Reset gry
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.points = 0
        self._agent_location = self.np_random.integers(0, 2)
        self._obstacle_location = np.array([0, 0])
        for i in range(0, self.size, 2):
            first_array = np.array([1, 0]) if self.np_random.integers(0, 2) == 0 else np.array([0, 1])
            second_array = np.array([0, 0])
            self._obstacle_location = np.vstack([self._obstacle_location, first_array])
            self._obstacle_location = np.vstack([self._obstacle_location, second_array])

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    # Krok gry
    def step(self, action):
        direction = self._action_to_direction[action]
        self._agent_location = direction
        crashed = self._obstacle_location[0][1] if self._agent_location == 1 else self._obstacle_location[0][0]
        self.points = self.points if crashed == 1 else self.points + 1
        reward = -1 if crashed else 1 if self.points >= self.size else 0

        if self.render_mode == "human":
            self._render_frame()

        # Aktualizacja mapy
        if not crashed:
            self._obstacle_location = np.delete(self._obstacle_location, (0), axis=0)
            self._obstacle_location = np.vstack([self._obstacle_location, np.array([0, 0])])

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, reward != 0, False, info
    

    # Graficzny panel
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        self.x = 200
        self.y = 1000
        self.pix_square_size = 100

        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.x, self.y))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.x, self.y))
        canvas.fill((255, 255, 255))

        carImg = pygame.image.load('car.png')
        obstancleImg = pygame.image.load('obstancle.png')

        # Rysowanie pojazdu
        if self._agent_location == 0:
            canvas.blit(carImg, (15, 0))
        else:
            canvas.blit(carImg, (self.pix_square_size + 15, 0))

        # Rysowanie przeszkód
        i = 0
        for x in self._obstacle_location[0:10]:
            if not np.array_equal(x, [0, 0]):
                if(x[0] == 0):
                    canvas.blit(obstancleImg, (self.pix_square_size, i * self.pix_square_size))
                else:
                    canvas.blit(obstancleImg, (0, i * self.pix_square_size))
            i = i + 1

        # Linie na mapce
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, self.pix_square_size * x),
                (self.x, self.pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (self.pix_square_size * x, 0),
                (self.pix_square_size * x, self.y),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])