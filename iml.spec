%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(libsatlas(.*)|libsatlas\\.so\\..*'
%else
%define _requires_exceptions devel(libsatlas\\|libsatlas\.so\..*
%endif
%define old_libname	%mklibname %{name} 0
%define old_devname	%mklibname %{name} -d

Name:           iml
Version:        1.0.3
Release:        8%{?dist}
Summary:        Finds solutions to systems of linear equations over integers

License:        BSD
URL:            https://cs.uwaterloo.ca/~astorjoh/iml.html
Source0:        https://cs.uwaterloo.ca/~astorjoh/%{name}-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
# This patch will not be sent upstream, as it is Fedora specific.  Configure
# checks whether the system realloc() has either of two bugs and, if so,
# uses a wrapper around realloc() to work around the bugs.  Glibc does not
# have those bugs, so the wrapper is unnecessary.  However, it gets linked
# into the final library anyway.  The wrapper code is GPLv2+ and iml is BSD.
# Since the workaround is not used on Fedora systems anyway, this patch
# prevents it from being linked in, allowing iml to remain straight BSD.
Patch0:         %{name}-no-repl.patch
# Support building on aarch64
Patch1:         %{name}-aarch64.patch

BuildRequires:  libatlas-devel
BuildRequires:  gmp-devel
%rename %{old_libname}


%description
IML provides efficient routines to compute exact solutions to dense
systems of linear equations over the integers.  The following
functionality is provided:
- Nonsingular rational system solving.
- Compute the right nullspace of an integer matrix.
- Certified linear system solving.


%package	devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libatlas-devel%{?_isa}, gmp-devel%{?_isa}
%rename libname%{name}-devel
%rename %{old_devname}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0
%patch1

# Fix a typo in iml 1.0.3
sed 's/mpz_init_ui/mpz_init_set_ui/' src/nullspace.c > src/nullspace.c.fix
touch -r src/nullspace.c src/nullspace.c.fix
mv -f src/nullspace.c.fix src/nullspace.c

# Adapt to recent ATLAS library structure
sed -i 's/-lcblas -latlas/-lsatlas/' configure

%build
%configure2_5x --enable-shared --disable-static \
  --with-atlas-include=%{_includedir}/atlas \
  --with-atlas-lib=%{_libdir}/atlas \
  LDFLAGS="-L%{_libdir}/atlas"

# Remove an unnecessary direct shared library dependency
sed -i 's/ -latlas//' src/Makefile

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}


%check
make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS README
%{_libdir}/lib%{name}.so.*


%files devel
%doc doc/liblink doc/libroutines examples
%{_includedir}/*
%{_libdir}/lib%{name}.so
