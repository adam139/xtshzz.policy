from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='xtshzz.policy',
      version=version,
      description="a site policy for xtshzz web site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['xtshzz'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'Products.membrane>=2.0.2',          
          'five.grok',
#          'collective.wtf',
          'dexterity.membrane',          
          'collective.monkeypatcher',
          'z3c.jbot',
          'my315ok.socialorgnization',
          'collective.diazotheme.bootstrap',
          'z3c.caching',
          'collective.autopermission',
                                                                     
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },         
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
