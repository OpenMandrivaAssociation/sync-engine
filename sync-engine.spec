%define name	sync-engine

Summary:	Synce synchronization engine
Name:		%{name}
Version:	0.11
Release:	%mkrel 9
License:	GPLv2+
Group:		Office
Source0:	%{name}-%{version}.tar.bz2
Source1:        synce-config.xml
# From upstream SVN: correct typo in code for finding default config
# file and copying it to home dir if it does not exist. Note that this
# version of the patch also changes it to look for the config file in
# SyncEngine/config rather than just /config, which is a Mandriva
# change that may not appear upstream, so when updating this package
# past 0.11 please don't just drop this patch as "merged" - AdamW
# 2008/03
Patch0:		sync-engine-0.11-config.patch
# From upstream SVN: fixes some problems with librapi error handling
# - AdamW 2008/03
Patch1:		sync-engine-0.11-rapierror.patch
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
%patch1 -p1 -b .rapierror

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
