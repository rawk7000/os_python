import copy
import json
import os
import eth_account
import requests
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct, encode_structured_data, encode_typed_data

load_dotenv('.env.local')

APIKEY = os.environ.get("OPENSEA_APIKEY")
PRIVATE_KEY = os.environ.get("OPENSEA_PRIVATEKEY")

def listNFT(signatureFinal, parametersInside):

    print(parametersInside)

    payload = {
        "parameters" : parametersInside,
        "protocol_address": "0x00000000000000adc04c56bf30ac9d3c0aaf14dc",
        "signature": signatureFinal
    }
    
    print(payload)

    headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": APIKEY
        }
            
    url = "https://api.opensea.io/api/v2/orders/matic/seaport/listings"
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

    return response.json()  


def create_signature():

    message_types = {
        "OrderComponents":[
            { "name":"offerer", "type":"address" },
            { "name":"zone", "type":"address" },
            { "name":"offer", "type":"OfferItem[]" },
            { "name":"consideration", "type":"ConsiderationItem[]" },
            { "name":"orderType", "type":"uint8" },
            { "name":"startTime", "type":"uint256" },
            { "name":"endTime", "type":"uint256" },
            { "name":"zoneHash", "type":"bytes32" },
            { "name":"salt", "type":"uint256" },
            { "name":"conduitKey", "type":"bytes32" },
            { "name":"counter", "type":"uint256" }
        ],
        "OfferItem":[
            { "name":"itemType", "type":"uint8" },
            { "name":"token", "type":"address" },
            { "name":"identifierOrCriteria", "type":"uint256" },
            { "name":"startAmount", "type":"uint256" },
            { "name":"endAmount", "type":"uint256" }
        ],
        "ConsiderationItem":[
            { "name":"itemType", "type":"uint8" },
            { "name":"token", "type":"address" },
            { "name":"identifierOrCriteria", "type":"uint256" },
            { "name":"startAmount", "type":"uint256" },
            { "name":"endAmount", "type":"uint256" },
            { "name":"recipient", "type":"address" }
        ]                     
    }

    domain_data = {
        "name":"Seaport",
        "version":"1.6",
        "chainId":137,
        "verifyingContract":"0x0000000000000068F116a894984e2DB1123eB395"
    }

    message_data = {
        "offerer":"0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
        "offer":[
            {
                "itemType":3,
                "token":"0x53Ae8AEDCa420c1b26f3b972B43F1Dc42f605585",
                "identifierOrCriteria":"8",
                "startAmount":"1",
                "endAmount":"1"
            }
        ],
        "consideration":[
            {
                "itemType":0,
                "token":"0x0000000000000000000000000000000000000000",
                "identifierOrCriteria":"0",
                "startAmount":"97500000000000000000",
                "endAmount":"97500000000000000000",
                "recipient":"0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b"
            },
            {
                "itemType":0,
                "token":"0x0000000000000000000000000000000000000000",
                "identifierOrCriteria":"0",
                "startAmount":"2500000000000000000",
                "endAmount":"2500000000000000000",
                "recipient":"0x0000a26b00c1F0DF003000390027140000fAa719"
            }
        ],
        "startTime":"1711923567",
        "endTime":"1714515567",
        "orderType":1,
        "zone":"0x0000000000000000000000000000000000000000",
        "zoneHash":"0x0000000000000000000000000000000000000000000000000000000000000000",
        "salt":"0x0000000000000000000000000000000000000000000000000000000000000000",
        "conduitKey":"0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
        "totalOriginalConsiderationItems":2,
        "counter":"0"
    }

    signable_message = encode_typed_data(domain_data, message_types, message_data)
    signed_message = Account.sign_message(signable_message, PRIVATE_KEY)

    print(signed_message)

    return signed_message.signature.hex()




parameters = {
    "offerer":"0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b",
    "offer":[
        {
            "itemType":3,
            "token":"0x53Ae8AEDCa420c1b26f3b972B43F1Dc42f605585",
            "identifierOrCriteria":"8",
            "startAmount":"1",
            "endAmount":"1"
        }
    ],
    "consideration":[
        {
            "itemType":0,
            "token":"0x0000000000000000000000000000000000000000",
            "identifierOrCriteria":"0",
            "startAmount":"97500000000000000000",
            "endAmount":"97500000000000000000",
            "recipient":"0xD95AD53A6A18aD26f71f1D631c60F0C9A1a7892b"
        },
        {
            "itemType":0,
            "token":"0x0000000000000000000000000000000000000000",
            "identifierOrCriteria":"0",
            "startAmount":"2500000000000000000",
            "endAmount":"2500000000000000000",
            "recipient":"0x0000a26b00c1F0DF003000390027140000fAa719"
        }
    ],
    "startTime":"1711923567",
    "endTime":"1714515567",
    "orderType":1,
    "zone":"0x0000000000000000000000000000000000000000",
    "zoneHash":"0x0000000000000000000000000000000000000000000000000000000000000000",
    "salt":"0x0000000000000000000000000000000000000000000000000000000000000000",
    "conduitKey":"0x0000007b02230091a7ed01230072f7006a004d60a8d4e71d599b8104250f0000",
    "totalOriginalConsiderationItems":2,
    "counter":"0"
}

signatureFinal = create_signature()

print("----------")
print(signatureFinal)
print("----------")
test = listNFT(signatureFinal, parameters)

print(test)


