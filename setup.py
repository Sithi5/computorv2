from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["plot==0.6.5"]

test_requirements = ["pytest==5.4.3"]

dev_requirements = ["black==21.9b0"] + test_requirements

extra_requirements = {
    "dev": dev_requirements,
}

setup(
    name="computorv2",
    version="0.0.2",
    description="A calculator interpreter.",
    long_description=long_description,
    author="Malo Boucé",
    author_email="ma.sithis@gmail.com",
    url="https://github.com/Sithi5/computorv2",
    py_modules=["computorv2"],
    packages=["src", "gui", "tests"],
    install_requires=requirements,
    extras_require=extra_requirements,
    entry_points={
        "console_scripts": ["computorv2 = computorv2:main"],
    },
    classifiers=[
        "Development Status :: 2 - Released",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
