from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["plot==0.6.5"]

test_requirements = [
    "pytest==5.4.3",
]

extra_requirements = {
    "dev": test_requirements,
}

setup(
    name="computorv2",
    version="1.0.0",
    description="A calculator interpreter.",
    long_description=long_description,
    author="Malo Boucé",
    author_email="ma.sithis@gmail.com",
    url="https://github.com/Sithi5/computorv2",
    py_modules=["computorv2"],
    packages=["src", "gui", "tests"],
    install_requires=requirements,
    extras_require=extra_requirements,
)
