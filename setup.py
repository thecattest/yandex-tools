import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yandex-lyceum-api",
    version="1.0.0",
    author="Jag_k",
    author_email="me@jagk.ru",
    description="API Яндекс.Лицея",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jag-k/yandex-lyceum-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: Russian",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",

    ],
    python_requires='>=3.8',
)