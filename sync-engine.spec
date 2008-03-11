%define name	sync-engine

Summary:	Synce synchronization engine
Name:		%{name}
Version:	0.11
Release:	%mkrel 8
License:	GPLv2+
Group:		Office
Source0:	%{name}-%{version}.tar.bz2
Source1:        synce-config.xml
Patch0:		sync-engine-config.patch
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
Synce synchronization engine.

%package -n libopensync-plugin-synce
Summary:	synce plugin for opensync
Group:		Office
Requires:	libopensync-plugin-python >= 0.35
Requires:	libopensync-plugin-vformat >= 0.35
Requires:	sync-engine

%description -n libopensync-plugin-synce
Synce plugin for Opensync

Before using sync-engine, you must first copy the
/usr/share/doc/sync-engine/config.xml into your $HOME/.synce
directory.


%prep
%setup -q
%patch0 -p1 -b .config

%build
%{__python} ./setup.py build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_bindir
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_libdir}/opensync-1.0/python-plugins/
mv \
 %{buildroot}%{py_puresitedir}/plugins/synce-opensync-plugin-3* \
 %{buildroot}%{_libdir}/opensync-1.0/python-plugins/
  
rm -fr %{buildroot}%{py_puresitedir}/plugins/

mkdir -p %{buildroot}%{py_puresitedir}/SyncEngine/config
install -m 0644 config/config.xml %{buildroot}%{py_puresitedir}/SyncEngine/config/config.xml

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING
%{_bindir}/*py
%{_bindir}/%{name}
%{py_puresitedir}/*

%files -n libopensync-plugin-synce
%defattr(-,root,root,-)
%{_libdir}/opensync-1.0/python-plugins/*
