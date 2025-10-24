# Proxmox Network Configuration

*Source: https://pve.proxmox.com/wiki/Network_Configuration*

## Key Concepts

### Configuration File
All network configuration is in `/etc/network/interfaces`. GUI changes write to `/etc/network/interfaces.new` for safety.

### Applying Changes

**ifupdown2 (recommended):**
```bash
# Apply from GUI or run:
ifreload -a
```

**Reboot method:**
The `pvenetcommit` service activates staging file before `networking` service applies it.

## Naming Conventions

### Current (Proxmox VE 5.0+)
- Ethernet: `en*` (systemd predictable names)
  - `eno1` - first on-board NIC
  - `enp3s0f1` - function 1 of NIC on PCI bus 3, slot 0
- Bridges: `vmbr[0-4094]`
- Bonds: `bond[N]`
- VLANs: Add VLAN number after period: `eno1.50`, `bond1.30`

### Legacy (pre-5.0)
- Ethernet: `eth[N]` (eth0, eth1, ...)

### Pinning Naming Scheme Version
Add to kernel command line to prevent name changes:
```bash
net.naming-scheme=v252
```

### Overriding Device Names

**Automatic tool:**
```bash
# Generate .link files for all interfaces
pve-network-interface-pinning generate

# With custom prefix
pve-network-interface-pinning generate --prefix myprefix

# Pin specific interface
pve-network-interface-pinning generate --interface enp1s0 --target-name if42
```

**Manual method** (`/etc/systemd/network/10-enwan0.link`):
```ini
[Match]
MACAddress=aa:bb:cc:dd:ee:ff
Type=ether

[Link]
Name=enwan0
```

After creating link files:
```bash
update-initramfs -u -k all
# Then reboot
```

## Network Setups

### Default Bridged Configuration

```bash
auto lo
iface lo inet loopback

iface eno1 inet manual

auto vmbr0
iface vmbr0 inet static
        address 192.168.10.2/24
        gateway 192.168.10.1
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
```

VMs behave as if directly connected to physical network.

### Routed Configuration

For hosting providers that block multiple MACs:

```bash
auto lo
iface lo inet loopback

auto eno0
iface eno0 inet static
        address  198.51.100.5/29
        gateway  198.51.100.1
        post-up echo 1 > /proc/sys/net/ipv4/ip_forward
        post-up echo 1 > /proc/sys/net/ipv4/conf/eno0/proxy_arp

auto vmbr0
iface vmbr0 inet static
        address  203.0.113.17/28
        bridge-ports none
        bridge-stp off
        bridge-fd 0
```

### Masquerading (NAT)

For VMs with private IPs:

```bash
auto lo
iface lo inet loopback

auto eno1
iface eno1 inet static
        address  198.51.100.5/24
        gateway  198.51.100.1

auto vmbr0
iface vmbr0 inet static
        address  10.10.10.1/24
        bridge-ports none
        bridge-stp off
        bridge-fd 0
        post-up   echo 1 > /proc/sys/net/ipv4/ip_forward
        post-up   iptables -t nat -A POSTROUTING -s '10.10.10.0/24' -o eno1 -j MASQUERADE
        post-down iptables -t nat -D POSTROUTING -s '10.10.10.0/24' -o eno1 -j MASQUERADE
```

**Conntrack zones fix** (if firewall blocks outgoing):
```bash
post-up   iptables -t raw -I PREROUTING -i fwbr+ -j CT --zone 1
post-down iptables -t raw -D PREROUTING -i fwbr+ -j CT --zone 1
```

## Linux Bonding

### Bond Modes

1. **balance-rr** - Round-robin (load balancing + fault tolerance)
2. **active-backup** - Only one active NIC (fault tolerance only)
3. **balance-xor** - XOR selection (load balancing + fault tolerance)
4. **broadcast** - Transmit on all slaves (fault tolerance)
5. **802.3ad (LACP)** - IEEE 802.3ad Dynamic link aggregation (requires switch support)
6. **balance-tlb** - Adaptive transmit load balancing
7. **balance-alb** - Adaptive load balancing (balance-tlb + receive balancing)

**Recommendation:**
- If switch supports LACP → use 802.3ad
- Otherwise → use active-backup

### Bond with Fixed IP

```bash
auto lo
iface lo inet loopback

iface eno1 inet manual
iface eno2 inet manual

auto bond0
iface bond0 inet static
      bond-slaves eno1 eno2
      address  192.168.1.2/24
      bond-miimon 100
      bond-mode 802.3ad
      bond-xmit-hash-policy layer2+3

auto vmbr0
iface vmbr0 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports eno3
        bridge-stp off
        bridge-fd 0
```

### Bond as Bridge Port

For fault-tolerant guest network:

```bash
auto lo
iface lo inet loopback

iface eno1 inet manual
iface eno2 inet manual

auto bond0
iface bond0 inet manual
      bond-slaves eno1 eno2
      bond-miimon 100
      bond-mode 802.3ad
      bond-xmit-hash-policy layer2+3

auto vmbr0
iface vmbr0 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports bond0
        bridge-stp off
        bridge-fd 0
```

## VLAN Configuration (802.1Q)

### VLAN Awareness on Bridge

**Guest VLANs** - Configure VLAN tag in VM settings, bridge handles transparently.

**Bridge with VLAN awareness:**
```bash
auto vmbr0
iface vmbr0 inet manual
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
        bridge-vlan-aware yes
        bridge-vids 2-4094
```

### Host Management on VLAN

**With VLAN-aware bridge:**
```bash
auto lo
iface lo inet loopback

iface eno1 inet manual

auto vmbr0.5
iface vmbr0.5 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1

auto vmbr0
iface vmbr0 inet manual
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
        bridge-vlan-aware yes
        bridge-vids 2-4094
```

**Traditional VLAN:**
```bash
auto lo
iface lo inet loopback

iface eno1 inet manual
iface eno1.5 inet manual

auto vmbr0v5
iface vmbr0v5 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports eno1.5
        bridge-stp off
        bridge-fd 0

auto vmbr0
iface vmbr0 inet manual
        bridge-ports eno1
        bridge-stp off
        bridge-fd 0
```

### VLAN with Bonding

```bash
auto lo
iface lo inet loopback

iface eno1 inet manual
iface eno2 inet manual

auto bond0
iface bond0 inet manual
      bond-slaves eno1 eno2
      bond-miimon 100
      bond-mode 802.3ad
      bond-xmit-hash-policy layer2+3

iface bond0.5 inet manual

auto vmbr0v5
iface vmbr0v5 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports bond0.5
        bridge-stp off
        bridge-fd 0

auto vmbr0
iface vmbr0 inet manual
        bridge-ports bond0
        bridge-stp off
        bridge-fd 0
```

## Advanced Features

### Disable MAC Learning

Available since Proxmox VE 7.3:

```bash
auto vmbr0
iface vmbr0 inet static
        address  10.10.10.2/24
        gateway  10.10.10.1
        bridge-ports ens18
        bridge-stp off
        bridge-fd 0
        bridge-disable-mac-learning 1
```

Proxmox VE manually adds VM/CT MAC addresses to forwarding database.

### Disable IPv6

Create `/etc/sysctl.d/disable-ipv6.conf`:

```ini
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

Then: `sysctl -p /etc/sysctl.d/disable-ipv6.conf`

## Troubleshooting

### Avoid ifup/ifdown

**Don't use** `ifup`/`ifdown` on bridges as they interrupt guest traffic without reconnecting.

**Use instead:**
- GUI "Apply Configuration" button
- `ifreload -a` command
- Reboot

### Network Changes Not Applied

1. Check `/etc/network/interfaces.new` exists
2. Click "Apply Configuration" in GUI or run `ifreload -a`
3. If issues persist, reboot

### Bond Not Working with Corosync

Some bond modes are problematic for Corosync. Use multiple networks instead of bonding for cluster traffic.
