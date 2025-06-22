import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PyQt6-Fluent-Widgets",
    version="1.8.2",
    keywords="pyqt6 fluent widgets",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A fluent design widgets library based on PyQt6",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPLv3",
    url="https://qfluentwidgets.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "PyQt6>=6.3.1",
        "PyQt6-Frameless-Window>=0.4.0",
        "darkdetect",
    ],
    extras_require = {
        'full': ['scipy', 'pillow', 'colorthief']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    project_urls={
        'Documentation': 'https://qfluentwidgets.com/',
        'Source Code': 'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PyQt6',
        'Bug Tracker': 'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues',
    }
)
