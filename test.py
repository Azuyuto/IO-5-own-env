import gymnasium
import driver_game

size = 10
env = gymnasium.make("DriverGame-v0", size=size)
env.reset()

# Rozwiązanie gry - przykład 1
observation, reward, done, _, info = env.step(0)
while not done:
    step = 0
    if observation["enemy"][0][0]:
        step = 1

    observation, reward, done, _, info = env.step(step)
    print(observation, reward, done, info)

