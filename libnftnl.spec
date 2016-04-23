%define major 4
%define libname %mklibname nftnl %{major}
%define libnamedevel %mklibname nftnl -d

Summary:	Userspace library for handling of netfilter netlink messages
Name:		libnftnl
Version:	1.0.5
Release:	2
Group:		System/Libraries
License:	GPLv2
URL:		http://netfilter.org/projects/libnftnl/index.html
Source0:	http://netfilter.org/projects/libnftnl/files/libnftnl-%{version}.tar.bz2
Patch0:		libnftnl-1.0.5-sprintf.patch
BuildRequires:	pkgconfig(libmnl)

%description
libnftnl is a userspace library providing a low-level netlink programming
interface (API) to the in-kernel nf_tables subsystem. The library libnftnl has
been previously known as libnftables. This library is currently used by
nftables.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libname}
libnftnl is a userspace library providing a low-level netlink programming
interface (API) to the in-kernel nf_tables subsystem. The library libnftnl has
been previously known as libnftables. This library is currently used by
nftables.

%package -n	%{libnamedevel}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	libnftnl-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libnamedevel}
This package contains the development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure --disable-static
%make

%check
%make check

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/*.la

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libnamedevel}
%{_includedir}/libnftnl
%{_libdir}/*.so
%{_libdir}/pkgconfig/libnftnl.pc
