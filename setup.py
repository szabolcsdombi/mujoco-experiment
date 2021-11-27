from setuptools import Extension, setup

ext = Extension(
    name='mymodule',
    sources=['./mymodule.cpp'],
    define_macros=[('PY_SSIZE_T_CLEAN', None)],
    include_dirs=['./include'],
    library_dirs=['.'],
    libraries=['mujoco210nogl'],
)

setup(
    name='mymodule',
    version='0.1.0',
    ext_modules=[ext],
)
