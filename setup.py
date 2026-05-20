from pathlib import Path
from setuptools import setup


version = "1.0.0.dev0"

long_description = (
    Path("README.md").read_text()
    if Path("README.md").exists()
    else "plonetheme.bootstrap6"
)

setup(
    name="plonetheme.bootstrap6",
    version=version,
    description="A Plone 6 theme based on Bootstrap 6 and Barceloneta (Classic UI).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Theme",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="web zope plone theme bootstrap6",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plonetheme.bootstrap6",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "plone.app.theming",
        "plone.resource",
        "plone.theme",
        "Products.GenericSetup",
    ],
    extras_require={"test": []},
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
