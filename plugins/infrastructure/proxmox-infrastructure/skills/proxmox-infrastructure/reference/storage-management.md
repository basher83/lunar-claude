# Proxmox Storage Management

## Overview

Proxmox VE supports multiple storage backends. This guide focuses on the storage architecture of the Matrix cluster: LVM-thin for boot disks and CEPH for distributed storage.

## Matrix Cluster Storage Architecture

### Hardware Configuration

**Per Node (Foxtrot, Golf, Hotel):**

```text
nvme0n1  - 1TB Crucial P3        → Boot disk + LVM
nvme1n1  - 4TB Samsung 990 PRO   → CEPH OSD (2 OSDs)
nvme2n1  - 4TB Samsung 990 PRO   → CEPH OSD (2 OSDs)
```

**Total Cluster:**

- 3× 1TB boot disks (LVM local storage)
- 6× 4TB NVMe drives (24TB raw CEPH capacity)
- 12 CEPH OSDs total (2 per NVMe drive)

### Storage Pools

```text
Storage Pool     Type       Backend    Purpose
-------------    ----       -------    -------
local            dir        Directory  ISO images, templates, backups
local-lvm        lvmthin    LVM-thin   VM disks (local)
ceph-pool        rbd        CEPH RBD   VM disks (distributed, HA)
ceph-fs          cephfs     CephFS     Shared filesystem
```

## LVM Storage

### LVM-thin Configuration

**Advantages:**

- Thin provisioning (overcommit storage)
- Fast snapshots
- Local to each node (low latency)
- No network overhead

**Disadvantages:**

- No HA (tied to single node)
- No live migration with storage
- Limited to node's local disk size

**Check LVM usage:**

```bash
# View volume groups
vgs

# View logical volumes
lvs

# View thin pool usage
lvs -a | grep thin
```

**Example output:**

```text
  LV            VG  Attr       LSize   Pool Origin Data%
  data          pve twi-aotz-- 850.00g             45.23
  vm-101-disk-0 pve Vwi-aotz--  50.00g data        12.45
```

### Managing LVM Storage

**Extend thin pool (if boot disk has space):**

```bash
# Check free space in VG
vgs pve

# Extend thin pool
lvextend -L +100G pve/data
```

**Create VM disk manually:**

```bash
# Create 50GB disk for VM 101
lvcreate -V 50G -T pve/data -n vm-101-disk-0
```

## CEPH Storage

### CEPH Architecture for Matrix

**Network Configuration:**

```text
vmbr1 (192.168.5.0/24, MTU 9000) → CEPH Public Network
vmbr2 (192.168.7.0/24, MTU 9000) → CEPH Private Network
```

**OSD Distribution:**

```text
Node      NVMe       OSDs    Capacity
-------   ------     ----    --------
foxtrot   nvme1n1    2       4TB
foxtrot   nvme2n1    2       4TB
golf      nvme1n1    2       4TB
golf      nvme2n1    2       4TB
hotel     nvme1n1    2       4TB
hotel     nvme2n1    2       4TB
-------   ------     ----    --------
Total                12      24TB raw
```

**Usable capacity (replica 3):** ~8TB

### CEPH Deployment Commands

**Install CEPH:**

```bash
# On first node (foxtrot)
pveceph install --version reef

# Initialize cluster
pveceph init --network 192.168.5.0/24 --cluster-network 192.168.7.0/24
```

**Create Monitors (3 for quorum):**

```bash
# On each node
pveceph mon create
```

**Create Manager (on each node):**

```bash
pveceph mgr create
```

**Create OSDs:**

```bash
# On each node - 2 OSDs per NVMe drive

# For nvme1n1 (4TB)
pveceph osd create /dev/nvme1n1 --crush-device-class nvme

# For nvme2n1 (4TB)
pveceph osd create /dev/nvme2n1 --crush-device-class nvme
```

**Create CEPH Pool:**

```bash
# Create RBD pool for VMs
pveceph pool create ceph-pool --add_storages

# Create CephFS for shared storage
pveceph fs create --name cephfs --add-storage
```

### CEPH Configuration Best Practices

**Optimize for NVMe:**

```bash
# /etc/pve/ceph.conf
[global]
    public_network = 192.168.5.0/24
    cluster_network = 192.168.7.0/24
    osd_pool_default_size = 3
    osd_pool_default_min_size = 2

[osd]
    osd_memory_target = 4294967296  # 4GB per OSD
    osd_max_backfills = 1
    osd_recovery_max_active = 1
```

**Restart CEPH services after config change:**

```bash
systemctl restart ceph-osd@*.service
```

### CEPH Monitoring

**Check cluster health:**

```bash
ceph status
ceph health detail
```

**Example healthy output:**

```text
cluster:
  id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
  health: HEALTH_OK

services:
  mon: 3 daemons, quorum foxtrot,golf,hotel
  mgr: foxtrot(active), standbys: golf, hotel
  osd: 12 osds: 12 up, 12 in

data:
  pools:   2 pools, 128 pgs
  objects: 1.23k objects, 45 GiB
  usage:   135 GiB used, 23.8 TiB / 24 TiB avail
  pgs:     128 active+clean
```

**Check OSD performance:**

```bash
ceph osd df
ceph osd perf
```

**Check pool usage:**

```bash
ceph df
rados df
```

## Storage Configuration in Proxmox

### Add Storage via Web UI

**Datacenter → Storage → Add:**

1. **Directory** - For ISOs and backups
2. **LVM-Thin** - For local VM disks
3. **RBD** - For CEPH VM disks
4. **CephFS** - For shared files

### Add Storage via CLI

**CEPH RBD:**

```bash
pvesm add rbd ceph-pool \
  --pool ceph-pool \
  --content images,rootdir \
  --nodes foxtrot,golf,hotel
```

**CephFS:**

```bash
pvesm add cephfs cephfs \
  --path /mnt/pve/cephfs \
  --content backup,iso,vztmpl \
  --nodes foxtrot,golf,hotel
```

**NFS (if using external NAS):**

```bash
pvesm add nfs nas-storage \
  --server 192.168.3.10 \
  --export /mnt/tank/proxmox \
  --content images,backup,iso \
  --nodes foxtrot,golf,hotel
```

## VM Disk Management

### Create VM Disk on CEPH

**Via CLI:**

```bash
# Create 100GB disk for VM 101 on CEPH
qm set 101 --scsi1 ceph-pool:100
```

**Via API (Python):**

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('192.168.3.5', user='root@pam', password='pass')
proxmox.nodes('foxtrot').qemu(101).config.put(scsi1='ceph-pool:100')
```

### Move VM Disk Between Storage

**Move from local-lvm to CEPH:**

```bash
qm move-disk 101 scsi0 ceph-pool --delete 1
```

**Move with live migration:**

```bash
qm move-disk 101 scsi0 ceph-pool --delete 1 --online 1
```

### Resize VM Disk

**Grow disk (can't shrink):**

```bash
# Grow VM 101's scsi0 by 50GB
qm resize 101 scsi0 +50G
```

**Inside VM (expand filesystem):**

```bash
# For ext4
sudo resize2fs /dev/sda1

# For XFS
sudo xfs_growfs /
```

## Backup and Restore

### Backup to Storage

**Create backup:**

```bash
# Backup VM 101 to local storage
vzdump 101 --storage local --mode snapshot --compress zstd

# Backup to CephFS
vzdump 101 --storage cephfs --mode snapshot --compress zstd
```

**Scheduled backups (via Web UI):**

Datacenter → Backup → Add:

- Schedule: Daily at 2 AM
- Storage: cephfs
- Mode: Snapshot
- Compression: ZSTD
- Retention: Keep last 7

### Restore from Backup

**List backups:**

```bash
ls /var/lib/vz/dump/
# OR
ls /mnt/pve/cephfs/dump/
```

**Restore:**

```bash
# Restore to same VMID
qmrestore /var/lib/vz/dump/vzdump-qemu-101-2024_01_15-02_00_00.vma.zst 101

# Restore to new VMID
qmrestore /var/lib/vz/dump/vzdump-qemu-101-2024_01_15-02_00_00.vma.zst 102 --storage ceph-pool
```

## Performance Tuning

### CEPH Performance

**For NVMe OSDs:**

```bash
# Set proper device class
ceph osd crush set-device-class nvme osd.0
ceph osd crush set-device-class nvme osd.1
# ... repeat for all OSDs
```

**Create performance pool:**

```bash
ceph osd pool create fast-pool 128 128
ceph osd pool application enable fast-pool rbd
```

**Enable RBD cache:**

```bash
# /etc/pve/ceph.conf
[client]
    rbd_cache = true
    rbd_cache_size = 134217728  # 128MB
    rbd_cache_writethrough_until_flush = false
```

### LVM Performance

**Use SSD discard:**

```bash
# Enable discard on VM disk
qm set 101 --scsi0 local-lvm:vm-101-disk-0,discard=on,ssd=1
```

## Troubleshooting

### CEPH Not Healthy

**Check OSD status:**

```bash
ceph osd tree
ceph osd stat
```

**Restart stuck OSD:**

```bash
systemctl restart ceph-osd@0.service
```

**Check network connectivity:**

```bash
# From one node to another
ping -c 3 -M do -s 8972 192.168.5.6  # Test MTU 9000
```

### LVM Out of Space

**Check thin pool usage:**

```bash
lvs pve/data -o lv_name,data_percent,metadata_percent
```

**If thin pool > 90% full:**

```bash
# Extend if VG has space
lvextend -L +100G pve/data

# OR delete unused VM disks
lvremove pve/vm-XXX-disk-0
```

### Storage Performance Issues

**Test disk I/O:**

```bash
# Test sequential write
dd if=/dev/zero of=/tmp/test bs=1M count=1024 oflag=direct

# Test CEPH RBD performance
rbd bench --io-type write ceph-pool/test-image
```

**Monitor CEPH latency:**

```bash
ceph osd perf
```

## Best Practices

1. **Use CEPH for HA VMs** - Store critical VM disks on CEPH for live migration
2. **Use LVM for performance** - Non-critical VMs get better performance on local LVM
3. **MTU 9000 for CEPH** - Always use jumbo frames on CEPH networks
4. **Separate networks** - Public and private CEPH networks on different interfaces
5. **Monitor CEPH health** - Set up alerts for HEALTH_WARN/HEALTH_ERR
6. **Regular backups** - Automated daily backups to CephFS or external NAS
7. **Plan for growth** - Leave 20% free space in CEPH for rebalancing
8. **Use replica 3** - Essential for data safety, especially with only 3 nodes

## Further Reading

- [Proxmox VE Storage Documentation](https://pve.proxmox.com/wiki/Storage)
- [CEPH Documentation](https://docs.ceph.com/)
- [Proxmox CEPH Guide](https://pve.proxmox.com/wiki/Deploy_Hyper-Converged_Ceph_Cluster)
