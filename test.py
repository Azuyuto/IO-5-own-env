import gymnasium
import driver_game
import random

size = 10
env = gymnasium.make("DriverGame-v0", size=size, render_mode = "human")
env.reset()

# Rozwiązanie gry - przykład 1
observation, reward, done, _, info = env.step(0)
while not done:
    step = random.randint(0, 1)
    if observation["obstacle"][0][0]:
        step = 1
    if observation["obstacle"][0][1]:
        step = 0

    observation, reward, done, _, info = env.step(step)
    print(observation, reward, done, info)

