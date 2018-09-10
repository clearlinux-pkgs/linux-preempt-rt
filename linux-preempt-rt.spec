#
# note to self: Linus releases need to be named 4.x.0 not 4.x or various
# things break
#

Name:           linux-preempt-rt
Version:        4.18.5
Release:        1
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.18.5.tar.xz
Source1:        https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/4.18/patch-4.18.5-rt3.patch.xz
Source2:        config
Source3:        cmdline

%define ktarget  preempt_rt
%define kversion %{version}-%{release}.%{ktarget}

BuildRequires:  buildreq-kernel

Requires: systemd-bin
Requires: init-rdahead-extras

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# preempt_rt patch
Patch0000: patch-4.18.5-rt3.patch.xz

#    000X: cve, bugfixes patches

#    00XY: Mainline patches, upstream backports

# Serie    01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-Increase-the-ext4-default-commit-age.patch
Patch0103: 0103-silence-rapl.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0105: 0105-ksm-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
#Patch0107: 0107-overload-on-wakeup.patch
Patch0108: 0108-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0109: 0109-smpboot-reuse-timer-calibration.patch
Patch0110: 0110-raid6-add-Kconfig-option-to-skip-raid6-benchmarking.patch
Patch0111: 0111-Initialize-ata-before-graphics.patch
Patch0112: 0112-reduce-e1000e-boot-time-by-tightening-sleep-ranges.patch
Patch0113: 0113-give-rdrand-some-credit.patch
Patch0114: 0114-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0115: 0115-tweak-perfbias.patch
Patch0116: 0116-e1000e-increase-pause-and-refresh-time.patch
Patch0117: 0117-kernel-time-reduce-ntp-wakeups.patch
Patch0118: 0118-init-wait-for-partition-and-retry-scan.patch
Patch0119: 0119-print-fsync-count-for-bootchart.patch
Patch0120: 0120-Add-boot-option-to-allow-unsigned-modules.patch
Patch0121: 0121-Enable-stateless-firmware-loading.patch
Patch0122: 0122-Migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0123: 0123-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch

# Clear Linux KVM Memory Optimization
#Patch0151: 0151-mm-Export-do_madvise.patch
#Patch0152: 0152-x86-kvm-Notify-host-to-release-pages.patch
#Patch0153: 0153-x86-Return-memory-from-guest-to-host-kernel.patch
#Patch0154: 0154-sysctl-vm-Fine-grained-cache-shrinking.patch

#
# Small tweaks
#
Patch0500: 0500-zero-extra-registers.patch
Patch0501: 0501-locking-rwsem-spin-faster.patch

#    200X: Open Programmable Acceleration Engine (OPAE)
#Patch2001: 2001-opae-add-intel-fpga-drivers.patch
#Patch2002: 2002-opae-add-Kconfig-and-Makefile.patch

#    300X: Sysdig
#Patch3001: 3001-Add-sysdig-0.20-driver.patch
#Patch3002: 3002Add-sysdig-to-kernel-build-system.patch

#
#   400X: Wireguard
#
Patch4001: 4001-WireGuard-fast-modern-secure-kernel-VPN-tunnel.patch

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files

%prep
%setup -q -n linux-4.18.5

#     0000  preempt_rt
%patch0000 -p1

#     000X  cve, bugfixes patches

#     00XY  Mainline patches, upstream backports

#     01XX  Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
#%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1

# Clear Linux KVM Memory Optimization
#%patch0151 -p1
#%patch0152 -p1
#%patch0153 -p1
#%patch0154 -p1

#
# Small tweaks
#
%patch0500 -p1
%patch0501 -p1

#    200X: Open Programmable Acceleration Engine (OPAE)
#%patch2001 -p1
#%patch2002 -p1

#	300X: sysdig
#%patch3001 -p1
#%patch3002 -p1

#
#   400X: Wireguard
#
%patch4001 -p1


cp %{SOURCE2} .

cp -a /usr/lib/firmware/i915 firmware/
cp -a /usr/lib/firmware/intel-ucode firmware/

%build
BuildKernel() {

    Target=$1
    Arch=x86_64
    ExtraVer="-%{release}.${Target}"

    rm -f localversion-rt

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make O=${Target} -s mrproper
    cp config ${Target}/.config

    make O=${Target} -s ARCH=${Arch} olddefconfig
    make O=${Target} -s ARCH=${Arch} CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} %{?sparse_mflags}
}

BuildKernel %{ktarget}

%install

InstallKernel() {

    Target=$1
    Kversion=$2
    Arch=x86_64
    KernelDir=%{buildroot}/usr/lib/kernel

    mkdir   -p ${KernelDir}
    install -m 644 ${Target}/.config    ${KernelDir}/config-${Kversion}
    install -m 644 ${Target}/System.map ${KernelDir}/System.map-${Kversion}
    install -m 644 ${Target}/vmlinux    ${KernelDir}/vmlinux-${Kversion}
    install -m 644 %{SOURCE3}           ${KernelDir}/cmdline-${Kversion}
    cp  ${Target}/arch/x86/boot/bzImage ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules
    make O=${Target} -s ARCH=${Arch} INSTALL_MOD_PATH=%{buildroot}/usr modules_install

    rm -f %{buildroot}/usr/lib/modules/${Kversion}/build
    rm -f %{buildroot}/usr/lib/modules/${Kversion}/source

    # Kernel default target link
    ln -s org.clearlinux.${Target}.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-${Target}

}


InstallKernel %{ktarget}  %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.%{ktarget}.%{version}-%{release}
/usr/lib/kernel/default-%{ktarget}
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
/usr/lib/kernel/vmlinux-%{kversion}

