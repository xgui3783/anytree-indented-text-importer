from setuptools import setup, find_packages

setup(
    name="indtext",
    version="0.0.1",
    packages=find_packages(include=["indented_text_importer"]),
    python_requires=">=3.7",
    install_requires=[
        "anytree",
    ],
)
