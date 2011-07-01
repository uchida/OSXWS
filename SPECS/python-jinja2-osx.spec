Name:		python-jinja2
Version:	2.5.5
Release:	3%{?_dist_release}
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-markupsafe
%if %{with doc}
BuildRequires:	python-sphinx
%endif
Requires:	python-babel >= 0.8
Requires:	python-markupsafe

BuildRequires:	python-setuptools

%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.

%prep
%setup -q -n Jinja2-%{version}

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete

# fix EOL
sed -i.tmp 's|\r$||g' LICENSE
rm -f LICENSE.tmp

%build
python setup.py build

# for now, we build docs using Python 2.x and use that for both
# packages.
%if %{with doc}
make -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build \
	    --root %{buildroot}

# remove hidden file
rm -rf docs/_build/html/.buildinfo

%clean
rm -rf $RPM_BUILD_ROOT

%check
make test

%files
%defattr(-,root,wheel)
%doc AUTHORS CHANGES LICENSE
%if %{with doc}
%doc docs/_build/html
%endif
%doc ext
%doc examples
%{python_sitelib}/*
%exclude %{python_sitelib}/jinja2/_debugsupport.c

%changelog
* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-3
- make more compatible with Vine Linux

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-2
- requires python-setuptools

* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-1
- replace setuptools with distribute

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-0
- initial build for Mac OS X WorkShop 10.6

