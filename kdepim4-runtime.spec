%define _disable_ld_no_undefined 1
%define oname kdepim-runtime

Summary:	K Desktop Environment Information Management runtime stuff
Name:		kdepim4-runtime
Version:	4.14.10
Release:	3
Epoch:		3
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		http://community.kde.org/KDE_PIM
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Source0:	http://download.kde.org/%{ftpdir}/%{version}/src/%{oname}-%{version}.tar.xz
Source1:	kdepim4-runtime.rpmlintrc
Patch10:	kdepim-runtime-4.10.5-noakonaditray.patch
BuildRequires:	boost-devel
BuildRequires:	kdelibs-devel >= 5:%{version}
BuildRequires:	kdepimlibs4-devel
BuildRequires:	qt4-qtdbus
BuildRequires:	akonadi
BuildRequires:	pkgconfig(akonadi)
BuildRequires:	pkgconfig(LibKFbAPI)
BuildRequires:	pkgconfig(libkgapi) >= 2.2.0
BuildRequires:	pkgconfig(libstreams)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(shared-desktop-ontologies)
%description
Information Management applications for the K Desktop Environment runtime libs.

#-----------------------------------------------------------------------------

%package -n akonadi-kde4
Group:		Graphical desktop/KDE
Summary:	Akonadi control center for KDE
Conflicts:	kdepim4-runtime-devel < 2:4.7.97
Conflicts:	%{_lib}kdepim-copy4 < 3:4.9.0
Requires:	akonadi
%if %{mdvver} >= 201400
Requires:	mariadb-client
%else
Requires:	mysql-client
%endif

%description -n akonadi-kde4
Akonadi control center for KDE.

%files -n akonadi-kde4
%{_kde_bindir}/*
%{_kde_appsdir}/akonadi
%{_kde_appsdir}/akonadi_facebook_resource/akonadi_facebook_resource.notifyrc
%{_kde_appsdir}/akonadi_maildispatcher_agent
%{_kde_appsdir}/akonadi_newmailnotifier_agent/akonadi_newmailnotifier_agent.notifyrc
%{_kde_appsdir}/kconf_update/newmailnotifier.upd
%{_kde_applicationsdir}/*
%{_kde_datadir}/akonadi/
%{_kde_datadir}/mime/packages/*
%{_kde_libdir}/kde4/*
%{_kde_iconsdir}/*/*/*/*
%{_kde_configdir}/*
%{_kde_autostart}/kaddressbookmigrator.desktop
%{_kde_services}/*
%{_kde_servicetypes}/*.desktop
%{_kde_datadir}/dbus-1/interfaces/*

#-----------------------------------------------------------------------------

%define akonadi_filestore_major 4
%define libakonadi_filestore %mklibname akonadi_filestore %{akonadi_filestore_major}

%package -n %{libakonadi_filestore}
Summary:	KDE 4 library
Group:		System/Libraries

%description -n %{libakonadi_filestore}
KDE 4 library.

%files -n %{libakonadi_filestore}
%{_kde_libdir}/libakonadi-filestore.so.%{akonadi_filestore_major}*

#-----------------------------------------------------------------------------

%define folderarchivesettings_major 4
%define libfolderarchivesettings %mklibname folderarchivesettings %{folderarchivesettings_major}

%package -n %{libfolderarchivesettings}
Summary:	KDE 4 library
Group:		System/Libraries

%description -n %{libfolderarchivesettings}
KDE 4 library.

%files -n %{libfolderarchivesettings}
%{_kde_libdir}/libfolderarchivesettings.so.%{folderarchivesettings_major}*

#-----------------------------------------------------------------------------

%define kdepim_copy_major 4
%define libkdepim_copy %mklibname kdepim-copy %{kdepim_copy_major}

%package -n %{libkdepim_copy}
Summary:	KDE 4 library
Group:		System/Libraries

%description -n %{libkdepim_copy}
KDE 4 library.

%files -n %{libkdepim_copy}
%{_kde_libdir}/libkdepim-copy.so.%{kdepim_copy_major}*

#-----------------------------------------------------------------------------

%define kmindexreader_major 4
%define libkmindexreader %mklibname kmindexreader %{kmindexreader_major}

%package -n %{libkmindexreader}
Summary:	KDE 4 library
Group:		System/Libraries

%description -n %{libkmindexreader}
KDE 4 library.

%files -n %{libkmindexreader}
%{_kde_libdir}/libkmindexreader.so.%{kmindexreader_major}*

#-----------------------------------------------------------------------------

%define maildir_major 4
%define libmaildir %mklibname maildir %{maildir_major}

%package -n %{libmaildir}
Summary:	KDE 4 library
Group:		System/Libraries

%description -n %{libmaildir}
KDE 4 library.

%files -n %{libmaildir}
%{_kde_libdir}/libmaildir.so.%{maildir_major}*

#----------------------------------------------------------------------

%package devel
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	kdepimlibs4-devel
Requires:	%{libakonadi_filestore} = %{EVRD}
Requires:	%{libfolderarchivesettings} = %{EVRD}
Requires:	%{libkdepim_copy} = %{EVRD}
Requires:	%{libkmindexreader} = %{EVRD}
Requires:	%{libmaildir} = %{EVRD}

%description devel
This package contains header files needed if you wish to build applications
based on kdepim-runtime.

%files devel
%{_kde_libdir}/libakonadi-filestore.so
%{_kde_libdir}/libfolderarchivesettings.so
%{_kde_libdir}/libkdepim-copy.so
%{_kde_libdir}/libkmindexreader.so
%{_kde_libdir}/libmaildir.so

#----------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}
%patch10 -p1
# required for cmake now
sed -i '1s/^/cmake_minimum_required(VERSION 2.4)\n/' CMakeLists.txt

%build
rm -fr po
%cmake_kde4
%make

%install
%makeinstall_std -C build

# Remove non packaged files
rm -rf %{buildroot}%{_kde_libdir}/libnepomukfeederpluginlib.a

%changelog
* Tue Nov 11 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.14.3-1
- New version 4.14.3

* Wed Oct 15 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.14.2-1
- New version 4.14.2

* Tue Sep 30 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.14.1-2
- Requires libkgapi at least 2.2.0

* Mon Sep 29 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.14.1-1
- New version 4.14.1

* Tue Jul 15 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.13.3-1
- New version 4.13.3

* Wed Jun 11 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.13.2-1
- New version 4.13.2
- Drop some nepumuk-related files
- New library libfolderarchivesettings

* Wed Apr 02 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.12.4-1
- New version 4.12.4

* Tue Mar 04 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.12.3-1
- New version 4.12.3

* Tue Feb 04 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.12.2-1
- New version 4.12.2

* Tue Jan 14 2014 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.12.1-1
- New version 4.12.1
- Move some files from akonadi-kde to kdepimlibs4-core
- Move libakonadi-xml subpackage to kdepimlibs4-core

* Wed Dec 04 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.11.4-1
- New version 4.11.4

* Wed Nov 06 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.11.3-1
- New version 4.11.3

* Wed Oct 02 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.11.2-1
- New version 4.11.2

* Tue Sep 03 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.11.1-1
- New version 4.11.1

* Wed Aug 14 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.11.0-1
- New version 4.11.0
- Add pkgconfig(LibKFbAPI) to BuildRequires
- Update files list

* Wed Jul 03 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.5-1
- New version 4.10.5
- Re-diff noakonaditray patch
- Cleanup really old Conflicts

* Wed Jun 05 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.4-1
- New version 4.10.4

* Tue May 07 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.3-1
- New version 4.10.3

* Wed Apr 03 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.2-1
- New version 4.10.2

* Sat Mar 09 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.1-1
- New version 4.10.1

* Thu Feb 07 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.10.0-1
- New version 4.10.0
- Update files

* Wed Dec 05 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.9.4-1
- New version 4.9.4

* Wed Nov 07 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.9.3-1
- New version 4.9.3

* Thu Oct 04 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.9.2-2
- New version 4.9.2
- Add rpmlint filters

* Sat Sep 08 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.9.1-1
- New version 4.9.1

- Add Conflicts on older libkdepim-copy4 for akonadi-kde package

* Tue Aug 07 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.9.0-1
- New version 4.9.0
- Re-diff l10n patch

* Sun Jul 22 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.8.97-2
- Add pkgconfig(libkgapi) to BuildRequires

* Mon Jul 16 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.8.97-1
- New version 4.8.97
- Convert BuildRequires to pkgconfig style
- Re-diff and enable l10n-ru patch

* Thu Jun 28 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.8.95-1
- Update to 4.8.95

* Wed Jun 27 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 3:4.8.90-1
- Update to 4.8.90

* Fri Jun 08 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 3:4.8.4-1
- update to 4.8.4

* Thu May 10 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 3:4.8.3-1
- update to 4.8.3

* Mon Apr 16 2012 Mikhail Kompaniets <mkompan@mezon.ru> 5:4.8.2-2
- Russian localization for .desktop files

* Thu Apr  5 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 5:4.8.2-1
- update to 4.8.2

* Sun Mar 11 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 5:4.8.1-1
- update to 4.8.1

* Thu Jan 19 2012 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.8.0-1
+ Revision: 762412
- New upstream tarball

* Fri Jan 06 2012 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.7.97-1
+ Revision: 758112
- New upstream tarball
- Move .so + dbus files file in the akonadi subpackage

* Tue Jan 03 2012 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.7.95-1
+ Revision: 748912
- Fix file list
- Fix file list
- Remove useless %%find_lang
- New version
- Try to fix build ( step 1)
- New upstream tarball
- New upstream tarball

* Fri Sep 09 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.7.41-1
+ Revision: 699154
- Fix file list
- New version 4.7.41

* Tue Jun 28 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.6.0-5
+ Revision: 687627
- Remove all translations

* Fri Jun 17 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.6.0-4
+ Revision: 685738
- Remove duplicate files

* Fri Jun 10 2011 Funda Wang <fwang@mandriva.org> 3:4.6.0-3
+ Revision: 684135
- final conflicts correction

* Fri Jun 10 2011 Funda Wang <fwang@mandriva.org> 3:4.6.0-2
+ Revision: 684103
- add more conflicts
- use actural package conflicts
- now ships included translations

* Thu Jun 09 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.6.0-1
+ Revision: 683342
- Fix epoch
- Say hello to brand new kdepim 4.6

* Tue Apr 26 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 3:4.4.11.1-0.1
+ Revision: 659243
- Revert kdepim to 4.4 branch

* Tue Apr 12 2011 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.5.95-1
+ Revision: 652802
- Update to beta5
- Remove mkrel

* Fri Jan 14 2011 Funda Wang <fwang@mandriva.org> 2:4.5.94.1-1
+ Revision: 631027
- New version 4.5.94.1
- update URL

* Sat Jan 08 2011 Funda Wang <fwang@mandriva.org> 2:4.5.94-1mdv2011.0
+ Revision: 630347
- new version 4.5.94

* Fri Dec 24 2010 Funda Wang <fwang@mandriva.org> 2:4.5.93-1mdv2011.0
+ Revision: 624415
- 4.6 beta3

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - New upstream tarball

* Wed Dec 08 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.5.85-1mdv2011.0
+ Revision: 616359
- New upstream tarball

* Fri Nov 26 2010 Funda Wang <fwang@mandriva.org> 2:4.5.80-1mdv2011.0
+ Revision: 601497
- new version 4.5.80 (aka 4.6 beta1)

* Sun Nov 21 2010 Funda Wang <fwang@mandriva.org> 2:4.5.77-0.svn1198704.2mdv2011.0
+ Revision: 599460
- bump req

* Sat Nov 20 2010 Funda Wang <fwang@mandriva.org> 2:4.5.77-0.svn1198704.1mdv2011.0
+ Revision: 599112
- new snapshot 4.5.77

* Sat Nov 13 2010 Funda Wang <fwang@mandriva.org> 2:4.5.76-0.svn1196608.1mdv2011.0
+ Revision: 597186
- new snapshot 4.5.76

* Thu Oct 28 2010 Funda Wang <fwang@mandriva.org> 2:4.5.74-0.svn1190490.1mdv2011.0
+ Revision: 589701
- new snapshot 4.5.74

* Fri Oct 08 2010 Funda Wang <fwang@mandriva.org> 2:4.5.71-0.svn1183613.1mdv2011.0
+ Revision: 584129
- New snapshot 4.5.71

* Wed Sep 15 2010 Funda Wang <fwang@mandriva.org> 2:4.5.68-1mdv2011.0
+ Revision: 578668
- new snapshot 4.5.68

* Tue Sep 07 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.5.67-1mdv2011.0
+ Revision: 576471
- Fix file list
- New version 4.5.67

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 2:4.4.5-1mdv2011.0
+ Revision: 563986
- New version 4.4.5
- sync with branch latest code

* Wed Jun 02 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.3-3mdv2010.1
+ Revision: 546960
- Add missing patch
- Akonaditray requires mysqldump
  CCBUG: 59570
- Rebuild in release mode

* Thu May 06 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.3-1mdv2010.1
+ Revision: 542790
- Remove P301 : Merged upstream
- Update to version 4.4.3

* Wed Apr 28 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.2-3mdv2010.1
+ Revision: 540303
- Add a patch fixing disribution list

* Fri Apr 02 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.2-2mdv2010.1
+ Revision: 530762
- Enable back those patches

* Tue Mar 30 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.2-1mdv2010.1
+ Revision: 530076
- Disabled akonadi patches, will be fixed after beta1
- Silent akonadi start ( P200 P201 )
- Update to version 4.4.2

* Tue Mar 02 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.1-1mdv2010.1
+ Revision: 513423
- Update to version 4.4.1

* Tue Feb 09 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.0-1mdv2010.1
+ Revision: 502633
- Update to version 4.4.0

* Mon Feb 01 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.98-1mdv2010.1
+ Revision: 498959
- Update to version 4.3.98 aka "kde 4.4 RC3"

* Mon Jan 25 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.95-1mdv2010.1
+ Revision: 496119
- Update to kde 4.4 Rc2

* Mon Jan 11 2010 Funda Wang <fwang@mandriva.org> 2:4.3.90-2mdv2010.1
+ Revision: 489627
- rebuild for missing packages

* Sun Jan 10 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.90-1mdv2010.1
+ Revision: 488234
- Update to kde 4.4 rc1
- Fix use of majors

* Mon Dec 21 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.85-2mdv2010.1
+ Revision: 480965
- Add patch to fix build
  Fix file list
- Update release because new bs failure
- Update to kde 4.4 beta2

* Fri Dec 04 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.80-1mdv2010.1
+ Revision: 473251
- Add shared-desktop-ontologies-devel as BuildRequire
- Update to kde 4.4 Beta1

* Sat Nov 28 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.77-1mdv2010.1
+ Revision: 470730
- Update to kde 4.3.77

* Tue Nov 17 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.75-1mdv2010.1
+ Revision: 466835
- Update to kde 4.3.75

* Thu Nov 12 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.73-2mdv2010.1
+ Revision: 465102
- Rebuild against new qt

* Sun Nov 08 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.73-1mdv2010.1
+ Revision: 462756
- Update to kde 4.3.73

* Tue Oct 06 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.2-1mdv2010.0
+ Revision: 454404
- New upstream release 4.3.2.

* Thu Sep 03 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.1-2mdv2010.0
+ Revision: 428850
- Move kdepim4-runtime naming to a proper akonadi-kde name
- Fix KDE bug 205742 ( Fail to read spaces in filename of addressbooks ) Thanks to mikala

* Tue Sep 01 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.1-1mdv2010.0
+ Revision: 423183
- New upstream release 4.3.1.

* Mon Aug 10 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.0-4mdv2010.0
+ Revision: 414271
- Fix BuildRequires
- Fix BuildRequires
- Add conflicts

* Tue Aug 04 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.0-3mdv2010.0
+ Revision: 409306
- New upstream release 4.3.0.

* Tue Jul 28 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.2.98-2mdv2010.0
+ Revision: 402519
- Add obsoletes to old library

* Fri Jul 24 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.2.98-1mdv2010.0
+ Revision: 399491
- Update for KDE 4.3 RC3
- imported package kdepim4-runtime

* Sat Jul 11 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.2.96-1mdv2010.0
+ Revision: 394819
- Fix file list
- Update to Rc2

* Sat Jun 27 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.2.95-3mdv2010.0
+ Revision: 389597
- Fix Requires

* Fri Jun 26 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.2.95-2mdv2010.0
+ Revision: 389418
- Add conflict

* Fri Jun 26 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.2.95-1mdv2010.0
+ Revision: 389367
- import kdepim4-runtime


