
%include	/usr/lib/rpm/macros.python
%define 	module psycopg

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	1.1.9
Release:	3
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	3a8ab26a7b9d83c179675866e7d6d414
Patch0:		%{name}-dumb-ac-fix.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	postgresql-backend-devel
BuildRequires:	python-devel
BuildRequires:	python-mx-DateTime-devel
Requires:	postgresql-libs
%pyrequires_eq	python-modules
Requires:	python-mx-DateTime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define prod_name ZPsycopgDA
%define zope_dir	   %{_libdir}/zope
%define zope_productsdir   %{zope_dir}/Products
%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile     python -c "import compileall; compileall.compile_dir('.')"


%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -l pl
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
PostgreSQL (tak jak pygresql i popy). Zosta³ zakodowany od pocz±tku
z za³o¿eniem ¿e ma byæ bardzo ma³y, szybki i stabilny. G³ówna zalet±
psycopg jest, ¿e w jest pe³ni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.

%package -n Zope-%{prod_name}
Summary:	Zope PostgreSQL database adapter
Summary(pl):	Interfejs bazy danych PostgreSQL do Zope
Group:		Development/Languages/Python
Requires:	Zope
Requires:	%{name} = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description -n Zope-%{prod_name}
Zope PostgreSQL database adapter.

%description -n Zope-%{prod_name} -l pl
Interfejs bazy danych PostgreSQL do Zope.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__autoconf}

%configure \
	--with-python=%{_bindir}/python \
	--with-mxdatetime-includes=%{py_incdir}/mx \
	--with-postgres-includes=%{_includedir}/postgresql/server
%{__make}

cd %{prod_name}
%{python_compile}
%{python_compile_opt}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{py_sitedir},%{zope_productsdir}/%{prod_name}}

install psycopgmodule.so $RPM_BUILD_ROOT%{py_sitedir}

cp -ar %{prod_name}/* $RPM_BUILD_ROOT%{zope_productsdir}/%{prod_name}
rm -f $RPM_BUILD_ROOT%{zope_productsdir}/%{prod_name}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS FAQ NEWS README RELEASE-1.0 SUCCESS TODO doc
%attr(755,root,root) %{py_sitedir}/*.so

%files -n Zope-%{prod_name}
%defattr(644,root,root,755)
%{zope_productsdir}/%{prod_name}
