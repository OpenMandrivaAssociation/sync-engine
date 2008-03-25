Summary:	Synce synchronization engine
Name:		sync-engine
Version:	0.11
Release:	%mkrel 16
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
# From upstream SVN: fix some more error handling issues - return
# errors correctly rather than erroring out with a Python traceback
# when partnership limit is reached, or name entered for a partnership
# is too long - AdamW 2008/03
Patch2:		sync-engine-0.11-errors.patch
# From upstream SVN: send out a d-bus signal when a partnership is
# deleted or created (useful for clients)
Patch3:		sync-engine-0.11-partnershipdbus.patch
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
Synce synchronization engine.

%package -n libopensync-plugin-synce
Summary:	synce plugin for opensync
Group:		Office
Requires:	libopensync-plugin-python >= 0.22
Requires:	%{name}

%description -n libopensync-plugin-synce
SynCE plugin for OpenSync. Allows applications using the OpenSync
framework to synchronise with devices handled by SynCE.

%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .rapierror
%patch2 -p1 -b .errors
%patch3 -p1 -b .partnership

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
# so apps like kitchensync know the plugin needs no config. Note this
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

%files -n libopensync-plugin-synce
%defattr(-,root,root,-)
%{_libdir}/opensync/python-plugins/*
%{_datadir}/opensync/defaults/synce-opensync-plugin

