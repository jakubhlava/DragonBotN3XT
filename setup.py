from setuptools import setup

setup(
    name="dragonbot",
    packages=["dragonbot"],
    include_package_data=True,
    install_requires=[
        "nextcord",
        "sqlalchemy",
        "pymysql"
    ]
)