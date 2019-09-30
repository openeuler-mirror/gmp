Name: gmp
Version: 6.1.2
Release: 9
Epoch: 1
URL: https://gmplib.org
Source0: https://gmplib.org/download/gmp/gmp-%{version}.tar.bz2
Source1: gmp.h
Source2: gmp-mparam.h
Patch0: gmp-6.0.0-debuginfo.patch
License: LGPLv3 and GPLv2
BuildRequires: autoconf automake libtool gcc gcc-c++ git perl-Carp
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
%autosetup -S git

%build
autoreconf -ifv
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
make %{?_smp_mflags}

%install
export LD_LIBRARY_PATH=`pwd`/.libs
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libgmpxx.so.4 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so

basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

mv %{buildroot}/%{_includedir}/gmp.h %{buildroot}/%{_includedir}/gmp-${basearch}.h
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/gmp.h
mv %{buildroot}/%{_includedir}/gmp-mparam.h %{buildroot}/%{_includedir}/gmp-mparam-${basearch}.h
install -m644 %{SOURCE2} %{buildroot}/%{_includedir}/gmp-mparam.h

%check
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{_libdir}/libgmp.so.*

%files devel
%{_libdir}/libgmpxx.so
%{_libdir}/libgmp.so
%{_includedir}/*.h
%{_infodir}/gmp.info*
%{_libdir}/libgmpxx.a
%{_libdir}/libgmp.a

%files c++
%{_libdir}/libgmpxx.so.*

%changelog
* Mon Aug 12 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:6.1.2-9
- Package init