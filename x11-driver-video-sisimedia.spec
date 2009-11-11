# Update to the sis driver provided by clevo. It's based on release 0.9.1 fd.o
# release, but it does not have a version of itself. The tarball is the fd.o
# 0.9.1 release itself. The following date macro is the date when the patch
# from the provided driver and the release was generated.
#
# The last driver provided by SiS is from 14/05/09
# This tarball was generated with the commands:
# % unrar x sis_drv_src_140509_viaSIS.rar
# % cd sis_drv_src_140509/2d-driver
# % make distclean
# % rm -f src/*.bak
# % rm -fr src/xvmc/.deps
# % rm -fr src/xvmc/Makefile
# % cd ..
# % mkdir xf86-video-sis-0.9.1
# % mv sis_drv_src_140509/2d-driver/* xf86-video-sis-0.9.1
# % chmod +x configure
# % tar jcvf xf86-video-sis-0.9.1.tar.bz2 xf86-video-sis-0.9.1
%define date 20090911
%define rel 1

Name: x11-driver-video-sisimedia
Version: 0.9.1
Release: %mkrel 1.%{date}.%{rel}
Summary: Video driver for SiS 670 / 671 cards
Group: System/X11
URL: http://www.linuxconsulting.ro/xorg-drivers/
Source: http://xorg.freedesktop.org/releases/individual/driver/xf86-video-sis-%{version}.tar.bz2

Patch1: 0002-Remove-XFree86-Misc-PassMessage-support.patch
Patch2: 0003-Fix-build-with-Werror-format-security.patch
Patch3: 0004-Do-not-force-detected-CRT1-to-off.patch
Patch4: 0005-Fix-backlight-off-on-SiS30x.-video-bridges.patch
Patch5: 0006-Add-IgnoreHotkeyFlag-driver-option.patch

# This corrects issues ("black stripes" in video output) in 2 Mandriva OEMs:
# oem 1 Requires:
#	Option "QuirkEDID60Hz"
# in the Device section /etc/X11/xorg.conf
# oem 2 Requires:
#	Option "QuirkEDID60Hz"
#	Option "UseOEMData" "false"
#	Option "UseROMData" "false"
# in the Device section /etc/X11/xorg.conf
# Both OEMs require a "cold boot" to take effect, that is, if fiddling
# with xorg.conf options, it may require a cold boot because the driver
# will keep some register set between X Server restarts.
# Both OEMs are based on 2009.1 (using SiS 671).
Patch6: x11-driver-video-sisimedia-0.9.1-QuirkEDID60Hz.patch

License: MIT
BuildRoot: %{_tmppath}/%{name}-root
 
BuildRequires: libdrm-devel >= 2.0
BuildRequires: x11-proto-devel >= 1.0.0
BuildRequires: x11-server-devel >= 1.0.1
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: GL-devel

Conflicts: xorg-x11-server < 7.0

Obsoletes: x11-driver-video-sis-imedia < %{version}-%{release}

%description
x11-driver-video-sisimedia is the video driver for SiS 670 / 671
cards. These are not supported by the X.org 'sis' driver. This code
is very different, so the two cannot be easily merged.

%prep
%setup -q -n xf86-video-sis-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
# rename driver sisimedia so it can co-exist with x.org sis driver
# - AdamW 2008/08
sed -i -e 's,sis_drv,sisimedia_drv,g' src/Makefile.am
sed -i -e 's,\"sis\",\"sisimedia\",g' src/sis.h
sed -i -e 's,sisModuleData,sisimediaModuleData,g' src/sis_driver.c

autoreconf -ifs

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

