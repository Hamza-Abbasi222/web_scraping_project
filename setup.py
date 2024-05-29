from setuptools import setup, find_packages

setup(
    name='web_scraping_project',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'scrape-books=scraping_script:main',
        ],
    },
)
