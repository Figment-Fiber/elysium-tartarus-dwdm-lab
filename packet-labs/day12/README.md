# Day 12 leaf-spine topology

A synthetic packet lab alongside the Elysium–Tartarus optical project. It contains two FRRouting leaves, two FRRouting spines and two Alpine hosts. Each leaf connects to both spines and its local host.

## Verified November 17, 2026

The lab deployed in Ubuntu on WSL 2 using Containerlab 0.83.0 and Docker Engine 29.8.1. Deployment output showed all six containers running and all six data links created. The topology was opened in Containerlab TopoViewer and its layout saved. The companion annotations JSON contains those node positions.

This milestone covers topology deployment and visual inspection. Service IP addresses, BGP neighbors and host routes still need configuration. Host-to-host reachability, ECMP and failover have not yet been tested.

## Run and view

From Ubuntu or another Linux environment with Docker and Containerlab installed, open this directory and run:

~~~bash
sudo clab deploy -t leaf-spine.clab.yml
~~~

The lab uses FRR image quay.io/frrouting/frr:containerlab-10.7.1 and Alpine image alpine:3. Docker pulls the images if needed. The Alpine tag can change over time.

To view the saved layout, open this directory in VS Code connected to WSL, install the Containerlab extension in that environment, open leaf-spine.clab.yml, then use Graph with TopoViewer (Ctrl+Alt+G). Keep the topology and annotations files together.

## Ports

| Device | Port | Connection |
| --- | --- | --- |
| leaf1 | eth1 | spine1 eth1 |
| leaf1 | eth2 | spine2 eth1 |
| leaf1 | eth3 | host-a eth1 |
| leaf2 | eth1 | spine1 eth2 |
| leaf2 | eth2 | spine2 eth2 |
| leaf2 | eth3 | host-b eth1 |

Containerlab creates eth0 on each device for management. The data links above are separate from that management network.

## Stop

From this directory:

~~~bash
sudo clab destroy -t leaf-spine.clab.yml
~~~

This removes the running containers and lab links. Keep any configurations you want to retain in the project before removing a lab.

## Next exercise

Configure and inspect the fabric's routing, test host reachability, and compare forwarding before and after an uplink failure.