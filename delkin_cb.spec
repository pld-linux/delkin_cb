#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define	rel	0.1
Summary:	Delkin CardBus IDE CompactFlash Adapter driver
Summary(pl.UTF-8):	Sterownik do adaptera CardBus IDE CompactFlash firmy Delkin
Name:		delkin_cb
Version:	0.1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	%{name}.c
URL:		http://rtr.ca/dell_i9300/kernel/latest/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build}
%endif
BuildRequires:	rpmbuild(macros) >= 1.330
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter.

%description -l pl.UTF-8
Sterownik jądra Linuksa do adaptera CardBus IDE CompactFlash firmy Delkin.

%package -n kernel%{_alt_kernel}-block-delkin_cb
Summary:	Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter
Summary(pl.UTF-8):	Sterownik jądra Linuksa do adaptera CardBus IDE CompactFlash firmy Delkin
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	kernel%{_alt_kernel}-pcmcia

%description -n kernel%{_alt_kernel}-block-delkin_cb
Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter.

%description -n kernel%{_alt_kernel}-block-delkin_cb -l pl.UTF-8
Sterownik jądra Linuksa do adaptera CardBus IDE CompactFlash firmy
Delkin.

%package -n kernel%{_alt_kernel}-smp-block-delkin_cb
Summary:	Linux SMP kernel driver for Delkin CardBus IDE CompactFlash Adapter
Summary(pl.UTF-8):	Sterownik jądra Linuksa SMP do adaptera CardBus IDE CompactFlash firmy Delkin
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	kernel%{_alt_kernel}-smp-pcmcia

%description -n kernel%{_alt_kernel}-smp-block-delkin_cb
Linux SMP kernel driver for Delkin CardBus IDE CompactFlash Adapter.

%description -n kernel%{_alt_kernel}-smp-block-delkin_cb -l pl.UTF-8
Sterownik jądra Linuksa SMP do adaptera CardBus IDE CompactFlash firmy
Delkin.

%prep
%setup -q -c -T
echo 'obj-m += delkin_cb.o' > Makefile
install %{SOURCE0} delkin_cb.c

%build
%build_kernel_modules -m delkin_cb

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m delkin_cb -d kernel/drivers/ide/pci

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-block-delkin_cb
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-block-delkin_cb
%depmod %{_kernel_ver}

%post -n kernel%{_alt_kernel}-smp-block-delkin_cb
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-block-delkin_cb
%depmod %{_kernel_ver}smp

%if %{with up}
%files -n kernel%{_alt_kernel}-block-delkin_cb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/ide/pci/delkin_cb.ko*
%endif

%if %{with smp}
%files -n kernel%{_alt_kernel}-smp-block-delkin_cb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/ide/pci/delkin_cb.ko*
%endif
