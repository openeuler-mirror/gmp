Name: gmp
Version: 6.3.0
Release: 1
Epoch: 1
URL: https://gmplib.org
Source0: https://gmplib.org/download/gmp/gmp-%{version}.tar.xz
License: LGPLv3 and GPLv2
BuildRequires: gcc gcc-c++ make m4
Summary: A GNU multiple precision arithmetic library

%description
GMP is a portable library written in C for arbitrary precision arithmetic
on integers, rational numbers, and floating-point numbers. It aims to provide
the fastest possible arithmetic for all applications that need higher
precision than is directly supported by the basic C types.

%package devel
Summary: Development library package for GMP.
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-c++%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description devel
Devel package include header files, documentation and libraries for GMP

%package c++
Summary: C++ development library package for GMP.
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description c++
GMP dependent library for C++ applications.

%prep
%autosetup -p1

%build
if as --help | grep -q execstack; then
  export CCAS="gcc -c -Wa,--noexecstack"
fi

%ifarch %{ix86}
  export CFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
  export CXXFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
%endif

%configure --enable-cxx

sed -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -i libtool
export LD_LIBRARY_PATH=`pwd`/.libs
%make_build

%install
export LD_LIBRARY_PATH=`pwd`/.libs
%make_install
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libgmpxx.so.4 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so

basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

%check
export LD_LIBRARY_PATH=`pwd`/.libs
%make_build check

%files
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{_libdir}/libgmp.so.*
%{_libdir}/pkgconfig/gmp.pc

%files devel
%{_libdir}/libgmpxx.so
%{_libdir}/libgmp.so
%{_includedir}/*.h
%{_infodir}/gmp.info*
%{_libdir}/libgmpxx.a
%{_libdir}/libgmp.a

%files c++
%{_libdir}/libgmpxx.so.*
%{_libdir}/pkgconfig/gmpxx.pc

%changelog
* Mon Jul 31 2023 Funda Wang <fundawang@yeah.net> - 1:6.3.0-1
- New version 6.3.0

* Tue Dec 7 2021 zhouwenpei <zhouwenpei1@huawei.com> - 1:6.2.1-3
- fix CVE-2021-43618

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 1:6.2.1-2
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Sat Jan 30 2021 xinghe <xinghe1@huawei.com> - 1:6.2.1-1
- Upgrade to 6.2.1

* Thu Jul 23 2020 jinzhimin <jinzhimin2@huawei.com> - 1:6.2.0-1
- Upgrade to 6.2.0

* Fri Jan 10 2020 yuxiangyang <yuxiangyang4@huawei.com> - 1:6.1.2-10
- Delete unuseful files

* Mon Aug 12 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:6.1.2-9
- Package init
