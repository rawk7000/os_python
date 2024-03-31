import os
import requests
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct, encode_structured_data, encode_typed_data

load_dotenv('.env.local')

w3 = Web3(Web3.HTTPProvider("https://celo-mainnet.infura.io/v3/493939980300497a8998c48dcd98dd41"))

APIKEY = os.environ.get("OPENSEA_APIKEY")
PRIVATE_KEY = os.environ.get("OPENSEA_PRIVATEKEY")

def listNFT(signatureFinal, parameters):
       
    payload = {
        "parameters" : parameters,
        "protocol_address": "0x00000000000000adc04c56bf30ac9d3c0aaf14dc",
        "signature": signatureFinal
    }

    print(payload)

    headers = {
            "x-api-key": APIKEY,
            "content-type": "application/json",
            "accept": "application/json",
        }
            
    url = "https://api.opensea.io/api/v2/orders/matic/seaport/listings"
    response = requests.post(url, json=payload, headers=headers)

    return response.json()  


parameters = {
        "offerer": "0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
        "offer": [
            {
                "itemType": "3",
                "token": "0x53Ae8AEDCa420c1b26f3b972B43F1Dc42f605585",
                "identifierOrCriteria": "8",
                "endAmount": "1",
                "startAmount": "1",
            }
        ],
        "consideration": [
            {
                "itemType": "0",
                "token": "0x0000000000000000000000000000000000000000",
                "identifierOrCriteria": "0",
                "startAmount": "97500000000000000000",
                "endAmount": "97500000000000000000",
                "recipient": "0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
            },
            {
                "itemType":"0",
                "token":"0x0000000000000000000000000000000000000000",
                "identifierOrCriteria":"0",
                "startAmount":"2500000000000000000",
                "endAmount":"2500000000000000000",
                "recipient":"0x0000a26b00c1F0DF003000390027140000fAa719"
            }
        ],
        "startTime": "1711923567",
        "endTime": "1714515567",
        "orderType": "1",
        "zone": "0x0000000000000000000000000000000000000000",
        "zoneHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "salt": "24446860302761739304752683030156737591518664810215442929817756370764078432657",
        "conduitKey": "0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
        "totalOriginalConsiderationItems": "2",
        "counter": "0"
}

def create_signature(parameters, private_key):

    message_schema = {
        'types': {
            'EIP712Domain': [{'name': 'name', 'type': 'string'},
                            {'name': 'version', 'type': 'string'},
                            {'name': 'chainId', 'type': 'uint256'},
                            {'name': 'verifyingContract', 'type': 'address'}],
            'OrderComponents': [{'name': 'offerer', 'type': 'address'},
                                {'name': 'zone', 'type': 'address'},
                                {'name': 'offer', 'type': 'OfferItem[]'},
                                {'name': 'consideration', 'type': 'ConsiderationItem[]'},
                                {'name': 'orderType', 'type': 'uint8'},
                                {'name': 'startTime', 'type': 'uint256'},
                                {'name': 'endTime', 'type': 'uint256'},
                                {'name': 'zoneHash', 'type': 'bytes32'},
                                {'name': 'salt', 'type': 'uint256'},
                                {'name': 'conduitKey', 'type': 'bytes32'},
                                {'name': 'counter', 'type': 'uint256'}],
            'OfferItem': [{'name': 'itemType', 'type': 'uint8'},
                         {'name': 'token', 'type': 'address'},
                         {'name': 'identifierOrCriteria', 'type': 'uint256'},
                         {'name': 'startAmount', 'type': 'uint256'},
                         {'name': 'endAmount', 'type': 'uint256'}],                      
            'ConsiderationItem': [{'name': 'itemType', 'type': 'uint8'},
                                 {'name': 'token', 'type': 'address'},
                                 {'name': 'identifierOrCriteria', 'type': 'uint256'},
                                 {'name': 'startAmount', 'type': 'uint256'},
                                 {'name': 'endAmount', 'type': 'uint256'},
                                 {'name': 'recipient', 'type': 'address'}],                      
        },
        "primaryType": "OrderComponents",
        "domain": {
            "name": "Seaport",
            "version": "1.6",
            "chainId": "137",
            "verifyingContract": "0x0000000000000068F116a894984e2DB1123eB395",
        },
        "message": parameters
    }
    
    print(message_schema)

    #account = Account.from_key(private_key)
    #signable_message = encode_structured_data(message_schema)
    #signed_message = account.sign_message(signable_message)
    #signed_message_2 = Account.sign_typed_data(private_key, full_message=message_schema)
    encoded_data = encode_typed_data(full_message=message_schema)
    signed_message = w3.eth.account.sign_message(encoded_data, private_key=private_key)
    
    print(signed_message)
    print("----------")
    return signed_message.signature.hex()


signatureFinal = create_signature(parameters, PRIVATE_KEY)

print("----------")
print(signatureFinal)
print("----------")
test = listNFT(signatureFinal, parameters)

print(test)


