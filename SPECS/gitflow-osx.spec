Summary: Git extensions for Vincent Driessen branching
Name: gitflow
Version: 0.4.1
Release: 0%{?_dist_release}
# git clone http://github.com/nvie/gitflow.git
# cd gitflow; git checkout 0.4.1
# git submodule init; git submodule update
# cd shFlags; git checkout 1.0.3 cd ../..; mv gitflow gitflow-0.4.1
# tar czf gitflow-0.4.1.tar.gz --exclude=.git* gitflow
Source0: gitflow-%{version}.tar.gz
License: BSD and LGPL
Group: Development/Tools
URL: https://github.com/nvie/gitflow

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Git extensions to provide high-level repository operations for Vincent Driessen's branching mode

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/git-flow*
%{_bindir}/gitflow*
%doc AUTHORS Changes.mdown LICENSE README.mdown

%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.4.1-0
- initial build for Mac OS X WorkShop

