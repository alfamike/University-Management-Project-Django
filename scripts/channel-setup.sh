#!/bin/bash

echo "Waiting for orderer to start..."
sleep 10
export ORDERER_TLS_CA="/etc/hyperledger/fabric/crypto-config/ordererOrganizations/university.eu/tlsca/tlsca.university.eu-cert.pem"
export ADMIN_CERT_FILE="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/signcerts/Admin@org1.university.eu-cert.pem"
export ADMIN_KEY_FILE="/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/users/Admin@org1.university.eu/msp/keystore/priv_sk"

# Create the channel
echo "Creating the channel..."
peer channel create -o orderer.university.eu:7050 -c registration-channel -f /etc/hyperledger/fabric/channel-artifacts/registration-channel.tx --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE  --certfile $ADMIN_CERT_FILE --outputBlock /etc/hyperledger/fabric/channel-artifacts/registration-channel.block

# Join the peer0 to the channel
echo "Peer0 joining the channel..."
peer channel join -b /etc/hyperledger/fabric/channel-artifacts/registration-channel.block --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE  --certfile $ADMIN_CERT_FILE

# Join the peer1 to the channel
echo "Peer1 joining the channel..."
export CORE_PEER_ADDRESS=peer1.org1.university.eu:8051
export CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/peers/peer1.org1.university.eu/tls/ca.crt
peer channel join -b /etc/hyperledger/fabric/channel-artifacts/registration-channel.block --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE  --certfile $ADMIN_CERT_FILE

# Setup completed
echo "Channel setup completed!"

sleep 5
echo "Init chaincodes deployment..."

# Deploy Title Chaincode
echo $PWD
echo < ls -l
peer lifecycle chaincode package title_cc.tar.gz --path /etc/hyperledger/fabric/chaincodes/TitleChaincode.java --lang java --label title_cc_1_0 --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE  --certfile $ADMIN_CERT_FILE
peer lifecycle chaincode install ./title_cc.tar.gz --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE   --certfile $ADMIN_CERT_FILE
peer lifecycle chaincode queryinstalled --tls --cafile $ORDERER_TLS_CA --clientauth --keyfile $ADMIN_KEY_FILE  --certfile $ADMIN_CERT_FILE
peer lifecycle chaincode approveformyorg \
   --channelID registration-channel \
   --name title_cc \
   --version 1.0 \
   --sequence 1 \
   --package-id title_cc_1.0:HASH \
   --orderer orderer.university.eu:7050 \
   --tls \
   --cafile $ORDERER_TLS_CA
peer lifecycle chaincode checkcommitreadiness \
   --channelID registration-channel \
   --name title_cc \
   --version 1.0 \
   --sequence 1 \
   --tls \
   --cafile $ORDERER_TLS_CA
peer lifecycle chaincode commit \
   --channelID registration-channel \
   --name title_cc \
   --version 1.0 \
   --sequence 1 \
   --orderer orderer.university.eu:7050 \
   --tls \
   --cafile $ORDERER_TLS_CA \
   --peerAddresses peer0.org1.university.eu:7051 \
   --tlsRootCertFiles /etc/hyperledger/fabric/crypto-config/peerOrganizations/org1.university.eu/peers/peer0.org1.university.eu/tls/ca.crt
peer lifecycle chaincode querycommitted --channelID registration-channel --name title_cc


