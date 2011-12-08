# Update to the sis driver provided by clevo. It's based on release 0.9.1 fd.o
# release, but it does not have a version of itself. The tarball is the fd.o
# 0.9.1 release itself. The following date macro is the date when the patch
# from the provided driver and the release was generated.
#
# The last driver provided by SiS is from 14/05/09
# This tarball was generated with the commands:

# (old: % unrar x sis_drv_src_140509_viaSIS.rar)
# (old: % cd sis_drv_src_140509/2d-driver)

# (source from 20091203)
# % unrar x Linux-driver.rar
# % cd 2d-driver
# % make distclean
# % rm -f src/*.bak
# % rm -fr src/xvmc/.deps
# % rm -fr src/xvmc/Makefile
# % for f in `find . -name \*.c -o -name \*.h`; do dos2unix $f; done
# % cd ..
# % mkdir xf86-video-sis-0.9.1
# % mv 2d-driver/* xf86-video-sis-0.9.1
# % chmod +x configure
# % tar jcvf xf86-video-sis-0.9.1.tar.bz2 xf86-video-sis-0.9.1
%define date 20091203
%define rel 10

Name: x11-driver-video-sisimedia
Version: 0.9.1
Release: %mkrel 2.%{date}.%{rel}
Summary: Video driver for SiS 670 / 671 cards
Group: System/X11
URL: http://www.linuxconsulting.ro/xorg-drivers/
Source: http://xorg.freedesktop.org/releases/individual/driver/xf86-video-sis-%{version}.tar.bz2

# How to write/apply a new patch for sisimedia:
# $ cd SOURCES
# $ tar xvjf xf86-video-sis-0.9.1.tar.bz2
# $ cd xf86-video-sis-0.9.1
# $ git init
# $ git add .
# $ git commit -a -m "Initial commit"
# $ for i in ../*.patch; do git am $i; done
# Then make your changes and commit them. After that, use "git log" to find out
# the commit-id of the first version. Then:
# $ git-format-patch ${initial-commit-id}
# Finally, copy your patch to "..", edit this spec, test and commit.

# SiS patch from 20102701
# $(B[ILwhL(B (chris_ke) <chris_ke@sis.com>
# ... I just upgrade SiS source based on ver. 090109 ...
Patch1: 0001-xf86-video-sis-0.9.1-20102701.patch
Patch2: 0002-Remove-XFree86-Misc-PassMessage-support.patch
Patch3: 0003-Fix-build-with-Werror-format-security.patch
Patch4: 0004-Fix-backlight-off-on-SiS30x.-video-bridges.patch
Patch5: 0005-Add-IgnoreHotkeyFlag-driver-option.patch
Patch6: 0006-xf86-video-sis-0.9.1-dump-regs-after-video-init.patch
Patch7: 0007-Remove-useless-loader-symbol-lists.patch
Patch8: 0008-Update-to-xextproto-7.1-support.patch
Patch9: 0009-sis-update-for-resources-RAC-API-removal.patch
Patch10: 0010-sis-change-to-using-ABI-version-check.patch
Patch11: 0011-More-RAC-removal.patch
Patch12: 0012-Remove-mibank.h-reference.patch
Patch13: 0013-Update-to-new-CreateNewResourceType-API.patch

License: MIT
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: libdrm-devel >= 2.0
BuildRequires: x11-proto-devel >= 1.0.0
BuildRequires: x11-server-devel >= 1.0.1
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: GL-devel

Requires: x11-server-common %(xserver-sdk-abi-requires videodrv)

Conflicts: xorg-x11-server < 7.0

Obsoletes: x11-driver-video-sis-imedia < %{version}-%{release}

%description
x11-driver-video-sisimedia is the video driver for SiS 670 / 671
cards. These are not supported by the X.org 'sis' driver. This code
is very different, so the two cannot be easily merged.

%prep
%setup -q -n xf86-video-sis-%{version}
%apply_patches

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

