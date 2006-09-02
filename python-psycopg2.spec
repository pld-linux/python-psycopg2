#
# todo:
# - zope adapter
# - lib64 patch
#

%define 	module	psycopg2

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	2.0.5.1
Release:	1
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/psycopg/%{module}-%{version}.tar.gz
# Source0-md5:	052e4b97dab47708fdcdc36ffb25af66
#Patch0:		%{name}-lib64.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	autoconf
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
Requires:	postgresql-libs
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define zope_subname ZPsycopgDA

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

%package -n Zope-%{zope_subname}
Summary:	Zope PostgreSQL database adapter
Summary(pl):	Interfejs bazy danych PostgreSQL do Zope
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	Zope

%description -n Zope-%{zope_subname}
Zope PostgreSQL database adapter.

%description -n Zope-%{zope_subname} -l pl
Interfejs bazy danych PostgreSQL do Zope.

%prep
%setup -q -n %{module}-%{version}
#%if "%{_lib}" == "lib64"
#%patch0 -p1
#%endif

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{py_libdir} -type f -name "*.py" | xargs rm

#install -d $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}

#cp -ar %{zope_subname}/* $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
#%py_comp $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
#%py_ocomp $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
#rm -f $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

#%post -n Zope-%{zope_subname}
#/usr/sbin/installzopeproduct %{_datadir}/Zope-%{zope_subname} %{zope_subname}
#if [ -f /var/lock/subsys/zope ]; then
#	/etc/rc.d/init.d/zope restart >&2
#fi

#%postun -n Zope-%{zope_subname}
#if [ "$1" = "0" ]; then
#	/usr/sbin/installzopeproduct -d %{zope_subname} 
#	if [ -f /var/lock/subsys/zope ]; then
#		/etc/rc.d/init.d/zope restart >&2
#	fi
#fi

%files
%defattr(644,root,root,755)
%doc ChangeLog AUTHORS README doc/HACKING doc/SUCCESS doc/TODO
%dir %{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[co]

#%files -n Zope-%{zope_subname}
#%defattr(644,root,root,755)
#%{_datadir}/Zope-%{zope_subname}
