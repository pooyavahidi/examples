import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybackpack",
    version="0.1.0",
    author="Pooya Vahidi",
    description="A collection of utilities and tools in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pooyavahidi/examples/libs/pybackpack",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["redis"],
    python_requires=">=3.7",
)
