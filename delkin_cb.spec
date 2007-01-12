#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define	rel	0.1
Summary:	Delkin CardBus IDE CompactFlash Adapter driver
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
Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter

%package -n kernel%{_alt_kernel}-block-delkin_cb
Summary:	Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	kernel%{_alt_kernel}-pcmcia

%description -n kernel%{_alt_kernel}-block-delkin_cb
Delkin CardBus IDE CompactFlash Adapter driver

%package -n kernel%{_alt_kernel}-smp-block-delkin_cb
Summary:	Linux kernel driver for Delkin CardBus IDE CompactFlash Adapter (SMP)
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	kernel%{_alt_kernel}-smp-pcmcia

%description -n kernel%{_alt_kernel}-smp-block-delkin_cb
Delkin CardBus IDE CompactFlash Adapter driver (SMP)

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
/lib/modules/%{_kernel_ver}/kernel/drivers/ide/pci/delkin_cb.ko.gz
%endif

%if %{with smp}
%files -n kernel%{_alt_kernel}-smp-block-delkin_cb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/ide/pci/delkin_cb.ko.gz
%endif
