Summary:	GaduGadu transport module for Jabber
Summary(pl.UTF-8):	Moduł transportowy GaduGadu dla systemu Jabber
Name:		jggtrans-xiaoka
Version:	20100310
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	0db904a25fb79a711f436fb79fbe8549
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-pidfile.patch
Patch1:		%{name}-spooldir.patch
URL:		http://svn.xiaoka.com/transports/jggtrans/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	expat-devel >= 1.95.1
BuildRequires:	gettext-autopoint
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libidn-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	jabber-common
Requires:	jabber-common
Obsoletes:	jabber-gg-transport
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with GaduGadu server. Xiaoka
fork.

%description -l pl.UTF-8
Moduł ten umożliwia użytkownikom Jabbera komunikowanie się z
użytkownikami GaduGadu. Wersja rozwijana przez Xiaoka.

%prep
%setup -q -n jggtrans
%patch0 -p1
%patch1 -p1

%build
./autogen.sh
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?debug:--with-efence} \
	--without-bind \
	--sysconfdir=%{_sysconfdir}/jabber
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d,/etc/sysconfig,/var/lib/jggtrans}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT"

install jggtrans.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jggtrans
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jggtrans

%find_lang jggtrans

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in jggtrans.xml..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/jggtrans.xml
	fi
fi
/sbin/chkconfig --add jggtrans
if [ -r /var/lock/subsys/jggtrans ]; then
	/etc/rc.d/init.d/jggtrans restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jggtrans start\" to start Jabber GaduGadu transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jggtrans ]; then
		/etc/rc.d/init.d/jggtrans stop >&2
	fi
	/sbin/chkconfig --del jggtrans
fi

%files -f jggtrans.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README README.Pl jggtrans.xml.Pl
%attr(755,root,root) %{_bindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/jggtrans.xml
%attr(754,root,root) /etc/rc.d/init.d/jggtrans
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jggtrans
%attr(770,root,jabber) /var/lib/jggtrans
