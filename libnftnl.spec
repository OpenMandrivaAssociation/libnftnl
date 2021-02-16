# libnftnl is used by iptables, iptables is used by systemd,
# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 11
%define libname %mklibname nftnl %{major}
%define libnamedevel %mklibname nftnl -d
%define lib32name libnftnl%{major}
%define lib32namedevel libnftnl-devel

Summary:	Userspace library for handling of netfilter netlink messages
Name:		libnftnl
Version:	1.1.9
Release:	1
Group:		System/Libraries
License:	GPLv2
URL:		http://netfilter.org/projects/libnftnl/index.html
Source0:	http://netfilter.org/projects/libnftnl/files/libnftnl-%{version}.tar.bz2
Patch0:		https://github.com/openembedded/meta-openembedded/raw/master/meta-networking/recipes-filter/libnftnl/libnftnl/0001-avoid-naming-local-function-as-one-of-printf-family.patch

BuildRequires:	pkgconfig(libmnl)
BuildRequires:	pkgconfig(jansson)
%if %{with compat32}
BuildRequires:	devel(libmnl)
%endif

%description
libnftnl is a userspace library providing a low-level netlink programming
interface (API) to the in-kernel nf_tables subsystem. The library libnftnl has
been previously known as libnftables. This library is currently used by
nftables.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
libnftnl is a userspace library providing a low-level netlink programming
interface (API) to the in-kernel nf_tables subsystem. The library libnftnl has
been previously known as libnftables. This library is currently used by
nftables.

%package -n %{libnamedevel}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	nftnl-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libnamedevel}
This package contains the development files for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for %{name} (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
libnftnl is a userspace library providing a low-level netlink programming
interface (API) to the in-kernel nf_tables subsystem. The library libnftnl has
been previously known as libnftables. This library is currently used by
nftables.

%package -n %{lib32namedevel}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
Requires:	%{libnamedevel} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{lib32namedevel}
This package contains the development files for %{name}.
%endif

%prep
%autosetup -p1

rm -rf examples
sed -i 's!examples!!g' Makefile.am
sed -i 's!tests!!g' Makefile.am
sed -i 's!examples/Makefile!!g' configure.ac
sed -i 's!tests/Makefile!!g' configure.ac

export CONFIGURE_TOP="$(pwd)"
aclocal
autoheader
automake -a
autoconf

%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif
mkdir build
cd build
%configure --with-json-parsing

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%check
%if %{with compat32}
make -C build32 check
%endif
make -C build %{?_smp_mflags} check
# JSON parsing is broken on big endian, causing tests to fail. Fixes awaiting
# upstream acceptance: https://marc.info/?l=netfilter-devel&m=152968610931720&w=2
#cd tests
#sh ./test-script.sh

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libnamedevel}
%{_includedir}/libnftnl
%{_libdir}/*.so
%{_libdir}/pkgconfig/libnftnl.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/*.so.%{major}*

%files -n %{lib32namedevel}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/libnftnl.pc
%endif
