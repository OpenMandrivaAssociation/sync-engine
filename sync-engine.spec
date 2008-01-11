%define name	sync-engine

Summary:	SynCE: Serial connection support
Name:		%{name}
Version:	0.11
Release:	%mkrel 1
License:	MIT
Group:		Office
Source:		%{name}-%{version}.tar.bz2
URL:		http://synce.sourceforge.net/
Buildroot:	%{_tmppath}/%name-root
BuildRequires:	python-setuptools
BuildRequires:	python-devel
Requires:	python-libxslt
Requires:	python-librtfcomp
Requires:	librra-python	

%description
Sync-engine is part of the SynCE project.

%prep
%setup -q

%build
python ./setup.py build

%install
mkdir -p %buildroot%_bindir
python ./setup.py install --root=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{py_puresitedir}/*
