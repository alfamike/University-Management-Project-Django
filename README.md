# University Hyperledger Fabric Network

This repository contains the Docker Compose configuration to set up a Hyperledger Fabric network for a university, including a CA, Orderer, two Peers with CouchDB, and a Django application for interaction with the blockchain.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Hyperledger Fabric binaries](https://hyperledger-fabric.readthedocs.io/)

Add the binaries to the PATH of your host.

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
   configtxgen -profile OrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block
   ```
3. Create the channel configuration transaction:
   ```bash
   configtxgen -profile RegistrationAppChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID registrtion-channel
   ```
4. Prepare for creation of clients for the Django app and the CouchDB instances
   ```bash
   export FABRIC_CA_CLIENT_HOME=$PWD/ca-client
   export FABRIC_CA_CLIENT_TLS_CERTFILES=$PWD/fabric-ca-server-config/ca.org1.university.eu-cert.pem
   ```
   Disable TLS in CA Server and re-run docker-compose file
5. Enroll an admin user
   ```bash
   fabric-ca-client enroll -u http://admin:adminpw@localhost:7054
   ```
6. Enroll 2 couchdb users
   ```bash
   fabric-ca-client enroll -u http://couch0:couch0pw@localhost:7054
   fabric-ca-client enroll -u http://couch1:couch1pw@localhost:7054
   ```
7. Enroll the django client
   ```bash
   fabric-ca-client enroll -u http://django:djangopw@localhost:7054
   ```
8. Convert .pem files into .crt and copy all certificates and keys into certs/

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
| `couchdb0.org1.university.eu`  | CouchDB for Peer 0              | 5984 |
| `couchdb1.org1.university.eu`  | CouchDB for Peer 1              | 5984 |
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

## Accesing CouchDB Fauxton UI
- [CouchDB 0](http://localhost:5984/_utils/#login)
- [CouchDB 1](http://localhost:5985/_utils/#login)

---

For detailed documentation, refer to the [Hyperledger Fabric documentation](https://hyperledger-fabric.readthedocs.io/).
@ Álvaro Menacho Rodríguez 2024