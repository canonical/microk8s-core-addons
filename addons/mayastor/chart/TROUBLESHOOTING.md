# curl: (56) OpenSSL SSL_read: Connection reset by peer, errno 104

When building for arm64, lots of errors like these were encountered with multiple derivations:

```
curl: (56) OpenSSL SSL_read: Connection reset by peer, errno 104
error: cannot download crate-nix-0.22.3.tar.gz from any mirror
```

Simply re-run the nix-build command.

# Link Failed

Tip: you might see an error like this:

```
/nix/store/77i6h1kjpdww9zzpvkmgyym2mz65yff1-binutils-2.35.1/bin/ld.bfd: final link failed: No space left on device
```

If `df -h` shows that the disk is in fact not full, e.g.
```
/dev/vda1        39G  7.0G   32G  19% /
tmpfs           4.7G  312M  4.4G   7% /run/user/1000
```

Then you might have to increase the size of your XDG_RUNTIME_DIR (the shown tmpfs above). Note that 30% refers to your system RAM, as this is a tmpfs filesystem. To do this:

```
echo 'RuntimeDirectorySize=70%' | sudo tee -a '/etc/systemd/logind.conf'
sudo reboot
```

Alternatively, just bind mount this to a different directory

```
mkdir ~/xdgtmp
sudo mount --bind $XDG_RUNTIME_DIR ~/xdgtmp
```

The XDG_RUNTIME_DIR needs about 15GB to build without issues.
