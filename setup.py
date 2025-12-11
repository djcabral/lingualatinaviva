from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements-refactored.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lingua-latina-viva",
    version="1.0.0",
    author="Diego J. Cabral",
    author_email="djcabral@example.com",
    description="A comprehensive Latin learning platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djcabral/lingualatinaviva",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Education :: Language",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lingua-latina-viva=app.main:main",
        ],
    },
)