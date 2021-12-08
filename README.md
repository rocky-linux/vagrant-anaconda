# Rocky Anaconda Dev Box

A Vagrant box built to work directly on Anaconda.

## Requirements

- [Vagrant](https://vagrantup.com)
- A hypervisor (i.e. libvirt, hyper-v, virtualbox)
- [vagrant-rsync-back](https://github.com/smerrill/vagrant-rsync-back)

## Installation & Usage

To use this, first ensure you have met the requirements described above. Then,
run `vagrant up` -- a CentOS 8 box will be provisioned & created for you.

Next, you need to initialize the Anaconda environment.

```
$ vagrant rsync-back
```

This command will pull the files found in `/usr/share/anaconda` into the
`anaconda/` directory.

You should now be able to edit the Anaconda files and push them back to the VM
with the following command:

```
$ vagrant rsync
```

Now, you should be able to run the following to start a Anaconda in headless
mode, which will make the installer available on VNC (`vnc://localhost:5901`).

```
$ vagrant ssh -c 'anaconda --vnc'
```

## Rebasing to new anaconda content

To upgrade to a new minor/major, or to utilize the content from another anaconda, simply extract the ISO's RPM or the
RPM from Koji and re-symlink anaconda to the /usr/share/anaconda/ path inside. The python files are located in
anaconda-core.rpm.

For example, you can use this to download the RPM and extract the contents:

```
curl https://kojidev.rockylinux.org/kojifiles/packages/anaconda/33.16.5.6/1.el8.rocky.1/x86_64/anaconda-core-33.16.5.6-1.el8.rocky.1.x86_64.rpm | rpm2cpio | cpio -D anaconda-src -id './usr/share/anaconda*'
```
