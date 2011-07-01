Name:           python-configobj
Version:        4.7.2
Release:        1%{?_dist_release}
Summary:        Config file reading, writing, and validation
Summary(ja):	設定ファイルの読み込み、書き込み、及び評価用のPython ツール

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.voidspace.org.uk/python/configobj.html
Source0:        http://www.voidspace.org.uk/downloads/configobj-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildArch:      noarch

BuildRequires: python-devel

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file
round tripper. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files. 
It has lots of other features though:

    * Nested sections (subsections), to any level
    * List values
    * Multiple line values
    * String interpolation (substitution)
    * Integrated with a powerful validation system
          - including automatic type checking/conversion
          - repeated sections
          - and allowing default values
    * All comments in the file are preserved
    * The order of keys/sections is preserved
    * No external dependencies
    * Full Unicode support
    * A powerful unrepr mode for storing basic datatypes


%prep
%setup -q -n configobj-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%check
export PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}"
python tests/test_configobj.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc docs/*
%{python_sitelib}/*

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-1
- add summary in Japanese

* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-0
- initial build for Mac OS X WorkShop

