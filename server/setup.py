import setuptools

setuptools.setup(
    name="lemon_pie",
    version="0.0.2",
    author="Henrique Rodrigues",
    description="Judge your friends using emojis",
    url="https://github.com/Henrod/lemon_pie",
    packages=setuptools.find_packages(include=["lemon_pie.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.7.*',
    install_requires=[],
)
