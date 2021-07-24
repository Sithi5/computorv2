from setuptools import setup

requirements = ["plot"]

test_requirements = [
    "pytest==5.4.3",
]

extra_requirements = {
    "dev": test_requirements,
}

setup(
    name="computorv2",
    version="0.0.1",
    description="A calculator interpreter than can operate on real, complex numbers, and 2D matrix data types, store variables, define and evaluate functions, and solve quadratic equation.",
    author="Malo Boucé",
    author_email="ma.sithis@gmail.com",
    url="https://github.com/Sithi5/computorv2",
    packages=["computorv2", "tests"],
    install_requires=requirements,
    extras_require=extra_requirements,
)
