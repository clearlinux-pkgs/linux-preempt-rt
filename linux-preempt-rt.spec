#
# This is the kernel native kernel plus the Preempt-RT patches
#
#
#

Name:           linux-preempt-rt
Version:        6.1.92
Release:        156
License:        GPL-2.0
Summary:        The Linux kernel with Preempt-RT
Url:            https://www.kernel.org
Group:          kernel
Source0:        https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.92.tar.xz
Source1:        https://mirrors.kernel.org/pub/linux/kernel/projects/rt/6.1/patch-6.1.92-rt32.patch.gz
Source2:        config
Source3:        cmdline

%define ktarget  preempt_rt
%define kversion %{version}-%{release}.%{ktarget}

BuildRequires:  buildreq-kernel

Requires: systemd-bin
Requires: init-rdahead-extras
Requires: linux-preempt-rt-license = %{version}-%{release}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#Serie0.name Upstream_Preemt-RT
#Serie0.git  https://git.kernel.org/pub/scm/linux/kernel/git/rt/linux-rt-devel.git
#Serie0.tag  v6.1.92-rt52-patches
#Serie0.start
Patch0000: patch-6.1.92-rt32.patch.gz
#Serie0.end

#cve.start cve patches from 0001 to 050
#cve.end

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-Increase-the-ext4-default-commit-age.patch
Patch0103: 0103-silence-rapl.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0105: 0105-ksm-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0107: 0107-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0109: 0109-Initialize-ata-before-graphics.patch
Patch0110: 0110-give-rdrand-some-credit.patch
Patch0111: 0111-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0112: 0112-kernel-time-reduce-ntp-wakeups.patch
Patch0113: 0113-init-wait-for-partition-and-retry-scan.patch
Patch0114: 0114-print-fsync-count-for-bootchart.patch
Patch0115: 0115-Add-boot-option-to-allow-unsigned-modules.patch
Patch0116: 0116-Enable-stateless-firmware-loading.patch
Patch0117: 0117-Migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0118: 0118-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0119: 0119-add-scheduler-turbo3-patch.patch
Patch0121: 0121-do-accept-in-LIFO-order-for-cache-efficiency.patch
Patch0122: 0122-zero-extra-registers.patch
Patch0123: 0123-locking-rwsem-spin-faster.patch
Patch0124: 0124-ata-libahci-ignore-staggered-spin-up.patch
Patch0125: 0125-print-CPU-that-faults.patch
Patch0126: 0126-x86-microcode-Force-update-a-uCode-even-if-the-rev-i.patch
Patch0127: 0127-x86-microcode-echo-2-reload-to-force-load-ucode.patch
Patch0128: 0128-fix-bug-in-ucode-force-reload-revision-check.patch
Patch0129: 0129-nvme-workaround.patch
Patch0130: 0130-Don-t-report-an-error-if-PowerClamp-run-on-other-CPU.patch
Patch0131: 0131-overload-on-wakeup.patch
#Serie.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel
Requires:       linux-preempt-rt-license = %{version}-%{release}

%description extra
Linux kernel extra files

%package license
Summary: license components for the linux package.
Group: Default

%description license
license components for the linux package.

%package cpio
License:        GPL-2.0
Summary:        cpio file with kenrel modules
Group:          kernel

%description cpio
Creates a cpio file with some modules

%package dev
License:        GPL-2.0
Summary:        The Linux kernel
Group:          kernel
Requires:       linux-preempt-rt = %{version}-%{release}
Requires:       linux-preempt-rt-extra = %{version}-%{release}
Requires:       linux-preempt-rt-license = %{version}-%{release}

%description dev
Linux kernel build files

%prep
%setup -q -n linux-6.1.92

#Serie0.patch.start
%patch0000 -p1
#Serie0.patch.end

#cve.patch.start cve patches
#cve.patch.end

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
#%patch0110 -p1
%patch0111 -p1
#%patch0112 -p1
%patch0113 -p1
#%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
#%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
#Serie.patch.end

cp %{SOURCE2} .

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
    DevDir=%{buildroot}/usr/lib/modules/${Kversion}/build

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

    mkdir -p ${DevDir}
    find . -type f -a '(' -name 'Makefile*' -o -name 'Kbuild*' -o -name 'Kconfig*' ')' -exec cp -t ${DevDir} --parents -pr {} +
    find . -type f -a '(' -name '*.sh' -o -name '*.pl' ')' -exec cp -t ${DevDir} --parents -pr {} +
    cp -t ${DevDir} -pr ${Target}/{Module.symvers,tools}
    ln -s ../../../kernel/config-${Kversion} ${DevDir}/.config
    ln -s ../../../kernel/System.map-${Kversion} ${DevDir}/System.map
    cp -t ${DevDir} --parents -pr arch/x86/include
    cp -t ${DevDir}/arch/x86/include -pr ${Target}/arch/x86/include/*
    cp -t ${DevDir}/include -pr include/*
    cp -t ${DevDir}/include -pr ${Target}/include/*
    cp -t ${DevDir} --parents -pr scripts/*
    cp -t ${DevDir}/scripts -pr ${Target}/scripts/*
    find  ${DevDir}/scripts -type f -name '*.[cho]' -exec rm -v {} +
    find  ${DevDir} -type f -name '*.cmd' -exec rm -v {} +
    # Cleanup any dangling links
    find ${DevDir} -type l -follow -exec rm -v {} +

    # Kernel default target link
    ln -s org.clearlinux.${Target}.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-${Target}
}

# cpio file for keyboard drivers
createCPIO() {

    Target=$1
    Kversion=$2
    KernelDir=%{buildroot}/usr/lib/kernel
    ModDir=/usr/lib/modules/${Kversion}

    mkdir -p cpiofile${ModDir}/kernel/drivers/input/{serio,keyboard}
    mkdir -p cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/i8042.ko.zst      cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/libps2.ko.zst     cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/keyboard/atkbd.ko.zst   cpiofile${ModDir}/kernel/drivers/input/keyboard
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-dj.ko.zst    cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-hidpp.ko.zst cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-apple.ko.zst          cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/modules.order   cpiofile${ModDir}
    cp %{buildroot}${ModDir}/modules.builtin cpiofile${ModDir}

    # Decompress the modules for the cpio file
    find cpiofile${ModDir} -name '*.ko.zst' -exec zstd -d --rm {} \;

    depmod -b cpiofile/usr ${Kversion}

    (
      cd cpiofile
      find . | cpio --create --format=newc \
        | xz --check=crc32 --lzma2=dict=512KiB > ${KernelDir}/initrd-org.clearlinux.${Target}.%{version}-%{release}
    )
}

InstallKernel %{ktarget} %{kversion}

createCPIO %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-preempt-rt
cp COPYING %{buildroot}/usr/share/package-licenses/linux-preempt-rt/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-preempt-rt

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

%files license
%defattr(0644,root,root,0755)
/usr/share/package-licenses/linux-preempt-rt

%files cpio
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}

%files dev
%defattr(-,root,root)
/usr/lib/modules/%{kversion}/build
