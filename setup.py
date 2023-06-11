import setuptools

REQUIRED_PACKAGES = [
    "gymnasium",
    "numpy",
    "pygame",
]

setuptools.setup(
    name="driver_game",
    version="1.0.1",
    install_requires=REQUIRED_PACKAGES,
    python_requires=">=3.9"
)
