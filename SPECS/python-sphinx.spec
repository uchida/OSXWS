%define __python /usr/osxws/bin/python
%define modulename sphinx

Summary: Python documentation generator
Name: python-%{modulename}
Version: 1.0.7
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%{version}.tar.gz
# hg clone http://bitbucket.org/shibu/sphinx-domains-docjp
# tar -czvf sphinx-docjp-20101201.tar.gz -C sphinx-domains-docjp docjp
Source1: sphinx-docjp-20101201.tar.gz
Source2: sphinx.dic
# http://bitbucket.org/birkenfeld/sphinx/issue/613
Patch1: sphinx-1.0.7-ptex.patch
# to build sphinx-docjp
Patch2: sphinx-docjp.patch
# http://bitbucket.org/birkenfeld/sphinx/issue/613
Patch3: sphinx-1.0.7-idescape.patch
License: BSD
Group: Development/Languages
Group: Applications/Publishing
URL: http://sphinx.pocoo.org/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: python-docutils
Requires: python-jinja2
Requires: python-pygments
Requires: graphviz
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-docutils
BuildRequires: python-jinja2
BuildRequires: python-pygments
Requires: tetex, dvipng
BuildRequires: tetex, dvipng
Requires: texmacro-unicode, texmacro-expdlist
BuildRequires: texmacro-unicode, texmacro-expdlist
BuildRequires: python-nose
BuildRequires: python-distribute
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Sphinx is a tool that makes it easy to create intelligent and beautiful documentation for Python projects. It was originally created to translate the new Python documentation, but has now been cleaned up in the hope that it will be useful to many other projects.
Sphinx uses reStructuredText as its markup language, and many of its strengths come from the power and straightforwardness of reStructuredText and its parsing and translating suite, the Docutils.
Although it is still under constant development, the following features are already present, work fine and can be seen "in action" in the Python docs:
- Output formats: HTML (including Windows HTML Help), plain text and LaTeX, for printable PDF versions
- Extensive cross-references: semantic markup and automatic links for functions, classes, glossary terms and similar pieces of information
- Hierarchical structure: easy definition of a document tree, with automatic links to siblings, parents and children
- Automatic indices: general index as well as a module index
- Code handling: automatic highlighting using the Pygments highlighter
- Various extensions are available, e.g. for automatic testing of snippets and inclusion of appropriately formatted docstrings.

%prep
%setup -q -a 1 -n %{modulename}-%{version}
%patch1 -p1 
%patch2 -p0
%patch3 -p1

%build
python setup.py build
pushd doc
make man
make html
make singlehtml
make latexpdf
popd

pushd docjp
make html
make singlehtml
make latex
pushd _build/latex
cp %{SOURCE2} .
make all-pdf-ja
popd
popd

%check
make test

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install doc/_build/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

mkdir -p ja
cp -r docjp/_build/html ja
cp -r docjp/_build/singlehtml ja
cp -r docjp/_build/latex/sphinx.pdf ja

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%doc AUTHORS CHANGES EXAMPLES LICENSE README TODO
%doc doc/_build/html
%doc doc/_build/singlehtml
%doc doc/_build/latex/sphinx.pdf
%doc ja
%{_mandir}/man1/*

%changelog
* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-0
- update to 1.0.7
- replace setuptools with distribute

* Fri Jan  7 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.6-0
- update to 1.0.6

* Tue Dec 21 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.5-0
- update to 1.0.5
- added Japanese LaTeX support
- added Japanese documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.4-0
- initial build for Mac OS X WorkShop 10.6

