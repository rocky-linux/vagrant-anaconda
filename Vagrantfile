Vagrant.configure("2") do |config|
  config.vm.box = "rockylinux/9"
  config.vm.network "forwarded_port", guest: 5901, host: 5901
  config.vm.provision "shell", inline: <<-SHELL
    ulimit -n 4096
    echo "stg/rocky" > /etc/dnf/vars/contentdir
    dnf -y install cloud-utils-growpart
    growpart /dev/vda 1
    xfs_growfs /
    dnf -y install rsync  anaconda anaconda-widgets kexec-tools-anaconda-addon anaconda-install-env-deps anaconda-dracut xorg-x11-fonts-misc xorg-x11-drivers xorg-x11-server-Xorg xorg-x11-server-utils xorg-x11-xauth dbus-x11 gsettings-desktop-schemas nm-connection-editor librsvg2 grub2-tools-efi efibootmgr shim-x64 grub2-efi-x64-cdboot biosdevname memtest86+ syslinux grub2-tools grub2-tools-minimal grub2-tools-extra plymouth libmlx4 rdma-core xorg-x11-fonts-misc dejavu-sans-fonts dejavu-sans-mono-fonts dmidecode rng-tools hdparm mt-st smartmontools pciutils usbutils ipmitool nmap-ncat net-tools tigervnc-server-module tigervnc-server-minimal ethtool openssh-server nfs-utils openssh-clients volume_key libblockdev udisks2 udisks2-iscsi hostname xfsdump device-mapper-persistent-data rsyslog systemd-sysv systemd-units kbd kbd-misc tar xz curl bzip2 rpcbind cryptsetup initscripts prefixdevname dracut-network dracut-config-generic dracut-fips glibc-all-langpacks grubby xrdb spice-vdagent bitmap-fangsongti-fonts kacst-farsi-fonts kacst-qurn-fonts lklug-fonts lohit-assamese-fonts lohit-bengali-fonts lohit-devanagari-fonts lohit-gu*-fonts lohit-kannada-fonts lohit-odia-fonts lohit-tamil-fonts lohit-telugu-fonts madan-fonts  smc-meera-fonts thai-scalable-waree-fonts  sil-abyssinica-fonts aajohan-comfortaa-fonts abattis-cantarell-fonts sil-scheherazade-fonts jomolhari-fonts khmeros-base-fonts sil-padauk-fonts gnome-kiosk
    setenforce 0
  SHELL
  config.vm.synced_folder "anaconda/", "/usr/share/anaconda/",
    type: "rsync",
    rsync__args: ["--copy-unsafe-links"]

  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider :libvirt do |libvirt|
    libvirt.machine_virtual_size = 20
    #libvirt.storage :file, :size => '20G'
  end
end
