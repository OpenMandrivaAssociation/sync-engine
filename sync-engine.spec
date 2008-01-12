%define name	sync-engine

Summary:	SynCE: Serial connection support
Name:		%{name}
Version:	0.11
Release:	%mkrel 2
License:	MIT
Group:		Office
Source:		%{name}-%{version}.tar.bz2
URL:		http://synce.sourceforge.net/
Buildroot:	%{_tmppath}/%name-root
BuildRequires:	python-setuptools
BuildRequires:	python-devel
Requires:	python-libxslt
Requires:	python-librtfcomp
Requires:	python-librra
Requires:	librapi-python	

%description
Sync-engine is part of the SynCE project.

%prep
%setup -q

%build
python ./setup.py build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_bindir
python ./setup.py install --root=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/synce
mv config/config.xml %{buildroot}/%{_sysconfdir}/synce/config.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/synce/*.xml
%{_bindir}/*
%{py_puresitedir}/*
