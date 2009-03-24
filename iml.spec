%define name	iml

Name:		%{name}
Group:		Sciences/Mathematics
License:	BSDish
Summary:	IML - Integer Matrix Library
Version:	1.0.2
Release:	%mkrel 1
Source:		http://www.cs.uwaterloo.ca/~z4chen/iml-1.0.2.tar.gz
URL:		http://www.cs.uwaterloo.ca/~z4chen/iml.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libgmp-devel
BuildRequires:	libatlas-devel

Provides:	lib%{name}-devel = %{version}-%{release}

%description
IML is a free library of C source code which implements algorithms for
computing exact solutions to dense systems of linear equations over the
integers. IML is designed to be used with the ATLAS/BLAS library and
GMP bignum library. 

%prep
%setup -q

%build
%configure2_5x						\
	--with-atlas-include=%{_includedir}/atlas	\
	--with-atlas-lib=%{_libdir}/atlas

%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_docdir}
mv -f %{buildroot}%{_datadir}/%{name} %{buildroot}%{_docdir}
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -fa examples/*.c examples/readme %{buildroot}%{_datadir}/%{name}/examples

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%dir %{_datadir}/%{name}/examples
%{_datadir}/%{name}/examples/*
