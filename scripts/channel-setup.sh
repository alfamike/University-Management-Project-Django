#!/bin/bash

echo "Waiting for orderer to start..."
sleep 10

# Create the channel
echo "Creating the channel..."
peer channel create -o orderer.university.eu:7050 -c registration-channel -f /etc/hyperledger/fabric/channel-artifacts/registration-channel.tx --tls --cafile /etc/hyperledger/fabric/crypto-config/ordererOrganizations/university.eu/tlsca/tlsca.university.eu-cert.pem --clientauth --keyfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/keystore/priv_sk  --certfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/signcerts/Admin@org1.university.eu-cert.pem --outputBlock /etc/hyperledger/fabric/channel-artifacts/registration-channel.block

# Join the peer0 to the channel
echo "Peer0 joining the channel..."
peer channel join -b /etc/hyperledger/fabric/channel-artifacts/registration-channel.block --tls --cafile /etc/hyperledger/fabric/crypto-config/ordererOrganizations/university.eu/tlsca/tlsca.university.eu-cert.pem --clientauth --keyfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/keystore/priv_sk  --certfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/signcerts/Admin@org1.university.eu-cert.pem

# Join the peer1 to the channel
echo "Peer1 joining the channel..."
export CORE_PEER_ADDRESS=peer1.org1.university.eu:8051
export CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/peers/peer1.org1.university.eu/tls/ca.crt
peer channel join -b /etc/hyperledger/fabric/channel-artifacts/registration-channel.block --tls --cafile /etc/hyperledger/fabric/crypto-config/ordererOrganizations/university.eu/tlsca/tlsca.university.eu-cert.pem --clientauth --keyfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/keystore/priv_sk  --certfile /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/signcerts/Admin@org1.university.eu-cert.pem

# Setup completed
echo "Channel setup completed!"
