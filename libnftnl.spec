%define major 11
%define libname %mklibname nftnl %{major}
%define libnamedevel %mklibname nftnl -d

Summary:	Userspace library for handling of netfilter netlink messages
Name:		libnftnl
Version:	1.1.5
Release:	1
Group:		System/Libraries
License:	GPLv2
URL:		http://netfilter.org/projects/libnftnl/index.html
Source0:	http://netfilter.org/projects/libnftnl/files/libnftnl-%{version}.tar.bz2
Patch1: 0001-tests-flowtable-Don-t-check-NFTNL_FLOWTABLE_SIZE.patch
Patch2: 0002-flowtable-Fix-memleak-in-error-path-of-nftnl_flowtab.patch
Patch3: 0003-chain-Fix-memleak-in-error-path-of-nftnl_chain_parse.patch
Patch4: 0004-flowtable-Correctly-check-realloc-call.patch
Patch5: 0005-chain-Correctly-check-realloc-call.patch
Patch6: 0002-avoid-naming-local-function-as-one-of-printf-family.patch

BuildRequires:	pkgconfig(libmnl)
BuildRequires:	pkgconfig(jansson)

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
Provides:	libnftnl-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libnamedevel}
This package contains the development files for %{name}.

%prep
%autosetup -p1

rm -rf examples
sed -i 's!examples!!g' Makefile.am
sed -i 's!tests!!g' Makefile.am
sed -i 's!examples/Makefile!!g' configure.ac
sed -i 's!tests/Makefile!!g' configure.ac

%build
%configure --disable-static --disable-silent-rules --with-json-parsing
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check
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
