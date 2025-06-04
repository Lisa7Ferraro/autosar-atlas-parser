from setuptools import setup, find_packages

setup(
    name="autosar-atlas-parser",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    py_modules=[],
    install_requires=[
        # PDF処理に必要なライブラリをここに
        "pdfminer.six>=20221105"
    ],
    entry_points={
        "console_scripts": [
            "autosar-parser=autosar_atlas_parser.main:main",
        ]
    }
)
