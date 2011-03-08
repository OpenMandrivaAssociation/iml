%define _requires_exceptions	devel(libcblas

%define name	iml
%define libname	%{mklibname %name 0}
%define devname	%{mklibname %name -d}

Name:		%{name}
Group:		Sciences/Mathematics
License:	BSD-like
Summary:	IML - Integer Matrix Library
Version:	1.0.3
Release:	%mkrel 2
Source:		http://www.cs.uwaterloo.ca/~astorjoh/iml-1.0.3.tar.gz
URL:		http://www.cs.uwaterloo.ca/~astorjoh/iml.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libgmp-devel
BuildRequires:	libatlas-devel

Patch0:		iml-1.0.3-build.patch
Patch1:		iml-1.0.3-leak.patch

%description
IML is a free library of C source code which implements algorithms for
computing exact solutions to dense systems of linear equations over the
integers. IML is designed to be used with the ATLAS/BLAS library and
GMP bignum library. 

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%dir %{_datadir}/%{name}/examples
%{_datadir}/%{name}/examples/*

#-----------------------------------------------------------------------
%package	-n %{libname}
Group:		Development/C
Summary:	IML - Integer Matrix Library library
Provides:	libname%{name}-devel = %{version}-%{release}

%description	-n %{libname}
IML - Integer Matrix Library library.

%files		-n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

#-----------------------------------------------------------------------
%package	-n %{devname}
Group:		Development/C
Summary:	IML - Integer Matrix Library development files
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description	-n %{devname}
IML- Integer Matrix Library development files.

%files		-n %{devname}
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/*.la
%{_libdir}/*.so

#-----------------------------------------------------------------------
%prep
%setup -q

%patch0 -p1
%patch1 -p1
rm -f config/*.m4

#-----------------------------------------------------------------------
%build
autoreconf -ifs
%configure						\
	--with-atlas-include=%{_includedir}/atlas	\
	--with-atlas-lib=%{_libdir}/atlas		\
	--disable-static				\
	--enable-shared

%make CFLAGS="%{optflags} -fPIC"

#-----------------------------------------------------------------------
%install
%makeinstall_std

mkdir -p %{buildroot}%{_docdir}
mv -f %{buildroot}%{_datadir}/%{name} %{buildroot}%{_docdir}
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -fa examples/*.c examples/readme %{buildroot}%{_datadir}/%{name}/examples

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}
