from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'process_monitor',
        ['process_monitor.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name='process_monitor',
    version='0.1',
    ext_modules=ext_modules,
)
