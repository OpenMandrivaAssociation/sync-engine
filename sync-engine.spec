Summary:	SynCE synchronization engine
Name:		sync-engine
Version:	0.11.1
Release:	%mkrel 4
License:	GPLv2+
Group:		Office
Source0:	http://prdownloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
Source1:        synce-config.xml
Patch0:		sync-engine-0.11.1-config.patch
# From upstream SVN: support synce-hal - AdamW 2008/06
Patch1:		sync-engine-0.11.1-hal.patch
# Better plugin description to differentiate from the other plugin
# that handles older devices - AdamW 2008/06
Patch2:		sync-engine-0.11.1-description.patch
URL:		http://synce.sourceforge.net/
Buildroot:	%{_tmppath}/%{name}-%{version}-root
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
SynCE synchronization engine. This component handles actual data
exchange between a Windows Mobile 5+ device and a synchronization
application.

%package -n synce-opensync-plugin
Summary:	synce plugin for opensync
Group:		Office
Requires:	libopensync-plugin-python >= 0.22
Requires:	%{name}
Obsoletes:	libopensync-plugin-synce < 0.22

%description -n synce-opensync-plugin
SynCE plugin for OpenSync. Allows applications using the OpenSync
framework to synchronise with devices handled by SynCE. This is the
plugin provided by the SynCE team, rather than that provided by the
OpenSync team. This plugin works with Windows Mobile 5 and later
devices.

%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p0 -b .hal
%patch2 -p1 -b .description

%build
%{__python} ./setup.py build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%{_bindir}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_libdir}/opensync/python-plugins/
mv \
 %{buildroot}%{py_puresitedir}/plugins/synce-opensync-plugin-2x.py \
 %{buildroot}%{_libdir}/opensync/python-plugins/

rm -fr %{buildroot}%{py_puresitedir}/plugins/

mkdir -p %{buildroot}%{py_puresitedir}/SyncEngine/config
install -m 0644 config/config.xml %{buildroot}%{py_puresitedir}/SyncEngine/config/config.xml

# dbus activation file (causes sync-engine to be run when something
# tries to access the dbus service) - AdamW 2008/03, with thanks to
# John Carr
mkdir -p %{buildroot}%{_datadir}/dbus-1/services
cat > %{buildroot}%{_datadir}/dbus-1/services/org.synce.service << EOF
[D-BUS Service]
Name=org.synce.SyncEngine
Exec=/usr/bin/sync-engine
EOF

# default config for opensync plugin, specifying an empty configuration
# so apps like multisync know the plugin needs no config. Note this
# will be different for opensync 0.3 / 0.4 - AdamW 2008/03
mkdir -p %{buildroot}%{_datadir}/opensync/defaults
cat > %{buildroot}%{_datadir}/opensync/defaults/synce-opensync-plugin << EOF
<config></config>
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING
%{_bindir}/*py
%{_bindir}/%{name}
%{_datadir}/dbus-1/services/org.synce.service
%{py_puresitedir}/*

%files -n synce-opensync-plugin
%defattr(-,root,root,-)
%{_libdir}/opensync/python-plugins/*
%{_datadir}/opensync/defaults/synce-opensync-plugin

