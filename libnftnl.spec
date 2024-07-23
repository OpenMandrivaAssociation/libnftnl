%define major 11
%define libname %mklibname nftnl %{major}
%define libnamedevel %mklibname nftnl -d

# (tpg) optimize it a bit
%global optflags %{optflags} -Oz
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

Summary:	Userspace library for handling of netfilter netlink messages
Name:		libnftnl
Version:	1.2.7
Release:	1
Group:		System/Libraries
License:	GPLv2
URL:		http://netfilter.org/projects/libnftnl/index.html
Source0:	http://netfilter.org/projects/libnftnl/files/libnftnl-%{version}.tar.xz
# (tpg) rediff below patch with these
# sed -i -e "s,(\*snprintf),(\*snprintf_),g" $(grep -rl "(*snprintf)" *)
# sed -i -e "s,^\t.snprintf\t\=,\t.snprintf_\t\=,g" $(grep -rl "\.snprintf" *)
# sed -i -e "s,\->snprintf,\->snprintf_,g" $(grep -rl "\->snprintf" *)
# Patch0:		https://github.com/openembedded/meta-openembedded/raw/master/meta-networking/recipes-filter/libnftnl/libnftnl/0001-avoid-naming-local-function-as-one-of-printf-family.patch
BuildRequires:	pkgconfig(libmnl)
Obsoletes:	libnftnl11 < 1.2.5-1
Obsoletes:	libnftnl-devel < 1.2.5-1

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

%prep
%autosetup -p1

rm -rf examples
sed -i 's!examples!!g' Makefile.am
sed -i 's!tests!!g' Makefile.am
sed -i 's!examples/Makefile!!g' configure.ac
sed -i 's!tests/Makefile!!g' configure.ac

aclocal
autoheader
automake -a
autoconf

%build
%configure
%make_build

%install
%make_install

%check
make %{?_smp_mflags} check

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libnamedevel}
%{_includedir}/libnftnl
%{_libdir}/*.so
%{_libdir}/pkgconfig/libnftnl.pc
