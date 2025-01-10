# University Hyperledger Fabric Network

This repository contains the Docker Compose configuration to set up a Hyperledger Fabric network for a university, including a CA, Orderer, two Peers with CouchDB, and a Django application for interaction with the blockchain.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Hyperledger Fabric binaries](https://hyperledger-fabric.readthedocs.io/)

## Network Architecture

The network includes:
1. **Certification Authority (CA):** Handles identity management.
2. **Orderer:** Manages the consensus for the blockchain network.
3. **Peers:** Nodes where transactions are validated and stored.
4. **CouchDB:** Database for managing state.
5. **Django Application:** Backend service to interact with the Fabric network.

## File Structure

```
.
├── crypto-config/          # Cryptographic material
├── channel-artifacts/      # Genesis block and channel configuration
├── university_management/  # Django application code
├── certs/                  # Certificates for CouchDB and Django
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # This README file
```

## Setting Up the Network

### Step 1: Generate Cryptographic Material and Artifacts
Before starting the network, generate the required cryptographic materials and channel artifacts using `cryptogen` and `configtxgen` tools:
1. Generate crypto material:
   ```bash
   cryptogen generate --config=./crypto-config.yaml
   ```
2. Generate the genesis block:
   ```bash
   configtxgen -profile TwoOrgsOrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block
   ```
3. Create the channel configuration transaction:
   ```bash
   configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID universitychannel
   ```

### Step 2: Start the Network
Run the following command to bring up the network:
```bash
docker-compose up -d
```

### Step 3: Set Up the Channel
Once the network is running:
1. Create the channel:
   ```bash
   docker exec -it cli peer channel create -o orderer.university.eu:7050 -c registration_app -f ./channel-artifacts/channel.tx --tls --cafile /etc/hyperledger/orderer/tls/ca.crt
   ```
2. Join peers to the channel:
   ```bash
   docker exec -it cli peer channel join -b registration_app.block
   ```

### Step 4: Launch Django Application
The Django application interacts with the blockchain network. It will be available at `https://localhost:8000`. Certificates are used to secure communication.

Access the application via a web browser:
```
https://localhost:8000
```

## Services Overview

| Service Name                   | Description                     | Port |
|--------------------------------|---------------------------------|------|
| `ca.org1.university.eu`        | Certification Authority         | 7054 |
| `orderer.university.eu`        | Orderer Node                    | 7050 |
| `peer0.org1.university.eu`     | Peer Node 0                     | 7051 |
| `peer1.org1.university.eu`     | Peer Node 1                     | 8051 |
| `couchdb0.org1.university.eu`  | CouchDB for Peer 0              | 6984 |
| `couchdb1.org1.university.eu`  | CouchDB for Peer 1              | 6984 |
| `django`                       | Django Application Backend      | 8000 |

## Stopping the Network
To stop and clean up the network, run:
```bash
docker-compose down -v
```

## Logs and Debugging
- View logs for a specific service:
  ```bash
  docker logs <container_name>
  ```
- Access a service's shell:
  ```bash
  docker exec -it <container_name> bash
  ```


---

For detailed documentation, refer to the [Hyperledger Fabric documentation](https://hyperledger-fabric.readthedocs.io/).