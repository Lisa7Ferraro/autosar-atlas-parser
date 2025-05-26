from setuptools import setup, find_packages

setup(
    name="autosar-atlas-parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # PDF処理に必要なライブラリをここに
        "pdfminer.six>=20221105"
    ],
    entry_points={
        "console_scripts": [
            "autosar-parser=parse_pdf:main",  # parse_pdf.py に main() を実装していれば
        ]
    }
)
