%define major 11
%define libname %mklibname nftnl %{major}
%define libnamedevel %mklibname nftnl -d

Summary:	Userspace library for handling of netfilter netlink messages
Name:		libnftnl
Version:	1.1.4
Release:	1
Group:		System/Libraries
License:	GPLv2
URL:		http://netfilter.org/projects/libnftnl/index.html
Source0:	http://netfilter.org/projects/libnftnl/files/libnftnl-%{version}.tar.bz2
#Patch0:		libnftnl-1.0.7-clang.patch
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
# (tpg) 2019-05-29 
# BUILDSTDERR: object.c:372:19: error: no member named '__builtin___snprintf_chk' in 'struct obj_ops'
export CC=gcc
%configure --disable-static
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libnamedevel}
%{_includedir}/libnftnl
%{_libdir}/*.so
%{_libdir}/pkgconfig/libnftnl.pc
