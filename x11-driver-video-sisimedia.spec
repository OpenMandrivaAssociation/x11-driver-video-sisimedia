# Update to the sis driver provided by clevo. It's based on release 0.9.1 fd.o
# release, but it does not have a version of itself. The tarball is the fd.o
# 0.9.1 release itself. The following date macro is the date when the patch
# from the provided driver and the release was generated.
%define date 20090622
%define rel 2

Name: x11-driver-video-sisimedia
Version: 0.9.1
Release: %mkrel 1.%{date}.%{rel}
Summary: Video driver for SiS 670 / 671 cards
Group: System/X11
URL: http://www.linuxconsulting.ro/xorg-drivers/
Source: http://xorg.freedesktop.org/releases/individual/driver/xf86-video-sis-%{version}.tar.bz2
# Fix build: don't include ansic.h (leads to conflicting defs)
Patch0: x11-driver-video-sis-imedia-0.9.1-ansic.patch
# Fix build: always include setjmp.h (conditional doesn't work on
# 2008.0)
Patch1:	x11-driver-video-sis-imedia-0.9.1-setjmp.patch

# Changes provided by Clevo and build fixes
Patch101: 0001-Driver-changes-sent-by-clevo.patch
Patch102: 0002-Remove-XFree86-Misc-PassMessage-support.patch
Patch103: 0003-Fix-build-with-Werror-format-security.patch
Patch104: 0004-Do-not-force-detected-CRT1-to-off.patch
Patch105: 0005-Fix-backlight-off-on-SiS30x.-video-bridges.patch
Patch106: 0006-Add-IgnoreHotkeyFlag-driver-option.patch


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
#patch0 -p1 -b .ansic
#patch1 -p1 -b .setjmp

%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1

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

