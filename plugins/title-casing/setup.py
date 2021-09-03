from setuptools import setup, find_packages

setup(
    name="mkdocs-title-casing-plugin",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.2",
        "titlecase>=2.3"
    ],
    entry_points={
        "mkdocs.plugins": [
            "title-casing = mkdocs_title_casing_plugin.plugin:TitleCasingPlugin"
        ]
    },
)
