from setuptools import setup

setup(
    name="pyprettyplot",
    version="1.0",
    packages=["pyprettyplot"],
    package_data={"pyprettyplot": ["matplotlibrc"]},
    description="Pretty Plotter For Plotly and Matplotlib",
    url="https://github.com/JQInanophotonics/pyprettyplot",
    author="Greg Moille",
    author_email="gmoille@umd.edu",
    license="Open",
    install_requires=[
        "pandas",
        "scipy",
        "numpy",
        "matplotlib",
        "plotly",
        "cmcrameri",
        "SecretColors",
        "nbformat",
        "kaleido",
        "lxml",
    ],
    include_package_data=True,
    zip_safe=False,
)
