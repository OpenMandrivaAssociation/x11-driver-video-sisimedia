# Upstream source tarball is not versioned, so we have to account for
# the fact it can change: version it as 0.9.1 (the internal version)
# -1.downloaddata.Xmdv - AdamW 2008/08
%define date 20080808
%define rel 3

Name: x11-driver-video-sisimedia
Version: 0.9.1
Release: %mkrel 1.%{date}.%{rel}
Summary: Video driver for SiS 670 / 671 cards
Group: System/X11
URL: http://www.linuxconsulting.ro/xorg-drivers/
Source: http://www.linuxconsulting.ro/xorg-drivers/src/xf86-video-sis-imedia.tgz
# Fix build: don't include ansic.h (leads to conflicting defs)
Patch0: x11-driver-video-sis-imedia-0.9.1-ansic.patch
# Fix build: always include setjmp.h (conditional doesn't work on
# 2008.0)
Patch1:	x11-driver-video-sis-imedia-0.9.1-setjmp.patch
License: MIT
BuildRoot: %{_tmppath}/%{name}-root
 
BuildRequires: libdrm-devel >= 2.0
BuildRequires: x11-proto-devel >= 1.0.0
BuildRequires: x11-server-devel >= 1.0.1
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: GL-devel

Conflicts: xorg-x11-server < 7.0

%description
x11-driver-video-sisimedia is the video driver for SiS 670 / 671
cards. These are not supported by the X.org 'sis' driver. This code
is very different, so the two cannot be easily merged.

%prep
%setup -q -n xf86-video-sis-imedia
%patch0 -p1 -b .ansic
%patch1 -p1 -b .setjmp

%build
# rename driver sisimedia so it can co-exist with x.org sis driver
# - AdamW 2008/08
mv src/sis_drv.la src/sisimedia_drv.la
sed -i -e 's,sis_drv,sisimedia_drv,g' src/sisimedia_drv.la src/Makefile.am
sed -i -e 's,\"sis\",\"sisimedia\",g' src/sis.h
sed -i -e 's,sisModuleData,sisimediaModuleData,g' src/sis_driver.c

# these two in this order are needed to avoid odd failures: seems the
# tarball was generated in a very weird environment - AdamW 2008/08,
# thanks to pcpa
autoreconf
make distclean

%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# it's just a copy of the x.org driver manpage and so not really any
# use - AdamW 2008/08
rm -f %{buildroot}%{_mandir}/man4/sis.*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/xorg/modules/drivers/sisimedia_drv.la
%{_libdir}/xorg/modules/drivers/sisimedia_drv.so

