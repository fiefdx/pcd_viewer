
# -*- coding: utf-8 -*-
'''
Created on 2019-01-25
@summary: pcd_viewer
@author: fiefdx
'''

from setuptools import setup, Extension

from Cython.Distutils import build_ext
import numpy

kwargs = {}
kwargs["name"] = "pcd_viewer"
kwargs["version"] = "0.0.1"
kwargs["author"] = "fiefdx"
kwargs["author_email"] = "fiefdx@163.com"
kwargs["packages"] = ["pcd_viewer"]
kwargs["package_dir"] = {"pcd_viewer": "src"}

carrayfilter = Extension(
    name = 'varrayfilter',
    sources = ['lib/varrayfilter.pyx', 'lib/arrayfilterlink.pxd', 'lib/arrayfilter.c'],
    include_dirs = ['lib', numpy.get_include()]
)

kwargs["cmdclass"] = {'build_ext': build_ext}
kwargs["ext_modules"] = [carrayfilter]
kwargs["entry_points"] = {'console_scripts': ['pcdv = pcd_viewer:main']}
setup(**kwargs)
