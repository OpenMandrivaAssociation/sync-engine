%define name	sync-engine

Summary:	SynCE: Serial connection support
Name:		%{name}
Version:	0.11
Release:	%mkrel 5
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
Requires:	libxml2-python
Requires:	pywbxml
Requires:	python-gobject
Requires:	python-pyxml
Requires:	python-dbus
Requires:	python-sqlite2


%description
Sync-engine is part of the SynCE project.


%package -n libopensync-plugin-synce
Summary:	synce plugin for opensync
Group:		Office
Requires:	libopensync-plugin-python >= 0.35
Requires:	libopensync-plugin-vformat >= 0.35
Requires:	sync-engine
Obsoletes:	libopensync-plugin-synce <= 0.22-4

%description -n libopensync-plugin-synce
Synce plugin for Opensync

%prep
%setup -q

%build
%{__python} ./setup.py build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_bindir
%{__python} ./setup.py install --skip-build --root=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/synce
mv config/config.xml %{buildroot}/%{_sysconfdir}/synce/config.xml

mkdir -p $RPM_BUILD_ROOT%{_libdir}/opensync-1.0/python-plugins/
mv \
 $RPM_BUILD_ROOT%{py_puresitedir}/plugins/synce-opensync-plugin-3* \
 $RPM_BUILD_ROOT%{_libdir}/opensync-1.0/python-plugins/
  
rm -fr $RPM_BUILD_ROOT%{py_puresitedir}/plugins/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sysconfdir}/synce/*.xml
%{_bindir}/*py
%{_bindir}/%{name}
%{py_puresitedir}/*

%files -n libopensync-plugin-synce
%{_libdir}/opensync-1.0/python-plugins/*
