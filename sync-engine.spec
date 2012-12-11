%define srcname synce-sync-engine
%define svn 0

Summary:	SynCE synchronization engine
Name:		sync-engine
Version:	0.15
Release:	%mkrel 1
License:	GPLv2+
Group:		Office
Source0:	http://downloads.sourceforge.net/project/synce/SynCE/%{version}/synce-%{name}-%{version}.tar.gz
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
%setup -q -n synce-%{name}-%{version}

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

# install dbus service file
mkdir -p %{buildroot}%{_datadir}/dbus-1/services
install -m 0644 config/org.synce.SyncEngine.service %{buildroot}%{_datadir}/dbus-1/services/org.synce.SyncEngine.service

# default config for opensync plugin, specifying an empty configuration
# so apps like multisync know the plugin needs no config. Note this
# will be different for opensync 0.3 / 0.4 - AdamW 2008/03
mkdir -p %{buildroot}%{_datadir}/opensync/defaults
cat > %{buildroot}%{_datadir}/opensync/defaults/synce-opensync-plugin << EOF
<config></config>
EOF

# install a default config file
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 config/syncengine.conf.xml %{buildroot}%{_sysconfdir}/syncengine.conf.xml

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING
%{_bindir}/*py
%{_bindir}/%{name}
%{_sysconfdir}/syncengine.conf.xml
%{_datadir}/dbus-1/services/org.synce.SyncEngine.service
%{py_puresitedir}/*

%files -n synce-opensync-plugin
%defattr(-,root,root,-)
%{_libdir}/opensync/python-plugins/*
%{_datadir}/opensync/defaults/synce-opensync-plugin



%changelog
* Tue Apr 27 2010 Emmanuel Andry <eandry@mandriva.org> 0.15-1mdv2010.1
+ Revision: 539656
- New version 0.15
- drop unneeded source1
- use upstream dbus service file

* Thu Mar 04 2010 Emmanuel Andry <eandry@mandriva.org> 0.15-0.r3893.1mdv2010.1
+ Revision: 514179
- pre 0.15 svn snapshot

* Fri Jul 24 2009 Frederik Himpe <fhimpe@mandriva.org> 0.14-1mdv2010.0
+ Revision: 399138
- Update to new version 0.13
- Remove voice patch integrated upstream
- Remove description patch which is not necessary anymore

* Wed Jan 14 2009 Adam Williamson <awilliamson@mandriva.org> 0.13-1mdv2009.1
+ Revision: 329272
- drop birthdays.patch (merged upstream)
- new release 0.13

* Sat Dec 27 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-5mdv2009.1
+ Revision: 319722
- rebuild with python 2.6

* Fri Oct 31 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-4mdv2009.1
+ Revision: 298840
- drop a bogus part of voice.patch: it was breaking sync of evo -> wm for me

* Sun Oct 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-3mdv2009.1
+ Revision: 297293
- add birthdays.patch from upstream SVN: fix birthday sync

* Thu Sep 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-2mdv2009.0
+ Revision: 288037
- add voice.patch (from Pawel Kot): handle phone number types better

* Wed Jul 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-1mdv2009.0
+ Revision: 236645
- drop config.patch (no longer needed, upstream has a sane config file system
  now)
- drop hal.patch (merged upstream)
- adjust config file installation for new config file system
- new release 0.12

* Tue Jun 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-4mdv2009.0
+ Revision: 214794
- add description.patch: better description for the opensync plugin

* Tue Jun 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-3mdv2009.0
+ Revision: 214447
- rename the opensync plugin so we can ship both the SynCE-provided and opensync-provided ones
- improve description
- add hal.patch: from upstream SVN, support synce-hal

* Thu Apr 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-2mdv2009.0
+ Revision: 197169
- resurrect and rediff config.patch: still needed as we change config.xml location

* Wed Apr 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-1mdv2009.0
+ Revision: 194620
- drop all patches (merged upstream)
- new release 0.11.1

* Tue Mar 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-16mdv2008.1
+ Revision: 190174
- reintroduce partnershipdbus.patch, fixed up properly this time

* Tue Mar 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-15mdv2008.1
+ Revision: 190087
- revert last change, it seems to cause synchronization to fail for an as-yet undetermined reason

* Mon Mar 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-14mdv2008.1
+ Revision: 189770
- add partnershipdbus.patch, from upstream SVN: send out a d-bus signal when a partnership is created or deleted

* Thu Mar 20 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-13mdv2008.1
+ Revision: 189201
- add errors.patch, from upstream SVN: handles errors better, returning an error rather than failing with a python trace; will let synce-kpm behave better in this case

* Thu Mar 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-12mdv2008.1
+ Revision: 187590
- only install the .py file for the opensync plugin, not the .pyo and .pyc, otherwise GUIs list it three times

* Thu Mar 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-11mdv2008.1
+ Revision: 187307
- adapt opensync plugin package to upcoming 0.22 opensync reversion
- better description for opensync plugin
- few small cleanups

* Wed Mar 12 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-10mdv2008.1
+ Revision: 187277
- create a dbus activation file so sync-engine gets run when anything tries to access the relevant dbus service

* Wed Mar 12 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-9mdv2008.1
+ Revision: 187222
- add rapierror.patch, from upstream SVN: fixes bugs in rapi handling which was causing partnerships not to be re-detected when phone was re-plugged or sync-engine started
- add comment on config.patch
- rename config.patch with version included

* Tue Mar 11 2008 Adam Williamson <awilliamson@mandriva.org> 0.11-8mdv2008.1
+ Revision: 186937
- install config.xml to the appropriate place (see sync-engine-config.patch)
- use %%{buildroot} instead of $RPM_BUILD_ROOT
- stop libopensync-plugin-synce from obsoleting itself
- add sync-engine-config.patch from upstream SVN: fix #37874 (default config file not created on first run) - slightly modified for better location of config file

* Sun Feb 17 2008 Emmanuel Andry <eandry@mandriva.org> 0.11-7mdv2008.1
+ Revision: 170031
- fix summary
- add an advisory for firt use

* Sat Feb 02 2008 Emmanuel Andry <eandry@mandriva.org> 0.11-6mdv2008.1
+ Revision: 161488
- fix license
- use fedora config.xml file
- ship config.xml as doc
- better description

* Wed Jan 16 2008 Emmanuel Andry <eandry@mandriva.org> 0.11-5mdv2008.1
+ Revision: 153840
- opensync plugin have now its own package
- add more requires
- use python macro
- provide opensync plugin

* Sat Jan 12 2008 Emmanuel Andry <eandry@mandriva.org> 0.11-2mdv2008.1
+ Revision: 149797
- add config file
- add missing requires librapi-python
- add missing requires librra-python
- add missing requires python-librtfcomp
- requires python-libxslt

* Fri Jan 11 2008 Emmanuel Andry <eandry@mandriva.org> 0.11-1mdv2008.1
+ Revision: 147796
- import sync-engine


