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

