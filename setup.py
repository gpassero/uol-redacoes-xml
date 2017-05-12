from distutils.core import setup
setup(name='uol_redacoes_xml',
      version='0.2',
	  description='UOL essays bank in XML format',
	  author='Guilherme Passero',
	  author_email='guilherme.passero0@gmail.com',
	  url='https://github.com/gpassero/uol-redacoes-xml',
      packages=['uol_redacoes_xml', 'uol_redacoes_xml.reader', 'uol_redacoes_xml.crawler'],
	  package_data={'uol_redacoes_xml': ['essays.xml.bz2']}
)
