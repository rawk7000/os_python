import os
from opensea import OpenseaAPI
from loguru import logger
import requests
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct, encode_structured_data

load_dotenv('../.env.local')

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
        "orderType": 0,
        "offerer": "0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
        "offer": [
            {
                "itemType": 3,
                "endAmount": 1,
                "startAmount": 1,
                "identifierOrCriteria": 8,
                "token": "0x53Ae8AEDCa420c1b26f3b972B43F1Dc42f605585"
            }
        ],
        "consideration": [
            {
                "itemType": 0,
                "startAmount": 10000000000000000000,
                "endAmount": 10000000000000000000,
                "recipient": "0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
                "identifierOrCriteria": 0,
                "token": "0x0000000000000000000000000000000000000000"
            }
        ],
        "startTime": 1711881384,
        "endTime": 1713827242,
        "zone": "0x0000000000000000000000000000000000000000",
        "zoneHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "salt": 3424543334654,
        "conduitKey": "0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
        "totalOriginalConsiderationItems": 10000000000000000000,
        "counter": 0
}

def create_signature(parameters, private_key):
    message_schema = {
        'types': {
            'ConsiderationItem': [{'name': 'itemType', 'type': 'uint8'},
                                 {'name': 'token', 'type': 'address'},
                                 {'name': 'identifierOrCriteria', 'type': 'uint256'},
                                 {'name': 'startAmount', 'type': 'uint256'},
                                 {'name': 'endAmount', 'type': 'uint256'},
                                 {'name': 'recipient', 'type': 'address'}],
           'EIP712Domain': [{'name': 'name', 'type': 'string'},
                            {'name': 'version', 'type': 'string'},
                            {'name': 'chainId', 'type': 'uint256'},
                            {'name': 'verifyingContract', 'type': 'string'}],
           'OfferItem': [{'name': 'itemType', 'type': 'uint8'},
                         {'name': 'token', 'type': 'address'},
                         {'name': 'identifierOrCriteria', 'type': 'uint256'},
                         {'name': 'startAmount', 'type': 'uint256'},
                         {'name': 'endAmount', 'type': 'uint256'}],
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
                               {'name': 'totalOriginalConsiderationItems', 'type': 'uint256'},
                               {'name': 'counter', 'type': 'uint256'}]
        },
        "primaryType": "OrderComponents",
        "domain": {
            "name": "Seaport",
            "version": "1.1",
            "chainId": 137,
            "verifyingContract": "0x00000000000000adc04c56bf30ac9d3c0aaf14dc",
        },
        "message": parameters
    }
    
    account = Account.from_key(private_key)
    signable_message = encode_structured_data(message_schema)
    signed_message = account.sign_message(signable_message)
    return signed_message.signature.hex()


signatureFinal = create_signature(parameters, PRIVATE_KEY)
test = listNFT(signatureFinal, parameters)

print(test)



