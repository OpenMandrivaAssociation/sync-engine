%define name	sync-engine

Summary:	Synce synchronization engine
Name:		%{name}
Version:	0.11
Release:	%mkrel 7
License:	GPLv2+
Group:		Office
Source0:	%{name}-%{version}.tar.bz2
Source1:        synce-config.xml
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
Obsoletes:	libopensync-plugin-synce <= 0.22-4

%description -n libopensync-plugin-synce
Synce plugin for Opensync

Before using sync-engine, you must first copy the
/usr/share/doc/sync-engine/config.xml into your $HOME/.synce
directory.


%prep
%setup -q

%build
%{__python} ./setup.py build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_bindir
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/opensync-1.0/python-plugins/
mv \
 $RPM_BUILD_ROOT%{py_puresitedir}/plugins/synce-opensync-plugin-3* \
 $RPM_BUILD_ROOT%{_libdir}/opensync-1.0/python-plugins/
  
rm -fr $RPM_BUILD_ROOT%{py_puresitedir}/plugins/

# supply a default config as doc
cp %{SOURCE1} config.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING config.xml
%{_bindir}/*py
%{_bindir}/%{name}
%{py_puresitedir}/*

%files -n libopensync-plugin-synce
%defattr(-,root,root,-)
%{_libdir}/opensync-1.0/python-plugins/*
