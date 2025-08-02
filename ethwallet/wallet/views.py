from django.shortcuts import render
from web3  import Web3
from web3.exceptions import Web3RPCError, ContractLogicError, InvalidAddress
import requests,json
from decouple import config
from django.http import HttpResponse, JsonResponse

KEY = config('API_KEY')

API_URL = f"https://sepolia.infura.io/v3/{KEY}"
web3 = Web3(Web3.HTTPProvider(API_URL))

def create_account(request):
    account = web3.eth.account.create('test create')
    request.session['account']={
        'privateKey': account.key.hex(),
        'address': account.address,
    }
    return JsonResponse(data=request.session['account'])

with open('erc20_abi.json') as f:
    erc20_abi = json.load(f)

'''def get_balance(request,contract_address):
    address = request.session.get('account').get('address')
    checksum_address = Web3.to_checksum_address(address)
    print(checksum_address)
    contract = web3.eth.contract(address=contract_address, abi=erc20_abi)
    balance = contract.functions.balanceOf(checksum_address).call()
    return JsonResponse(data=balance,safe=False)'''

def get_balance(request,addr):
    balance_wei = web3.eth.get_balance(addr)
    balance = web3.from_wei(balance_wei,'ether')
    return JsonResponse(data=balance,safe=False)

def send_transaction(request):
    try:
        addr = '0x2AC03BF434db503f6f5F85C3954773731Fc3F056'
        nonce = web3.eth.get_transaction_count(request.session['account']['address'])
        transaction_dict = {

                # 'to': data['to'],
                'to': addr,

                # 'value': web3.toWei(data['amount'], 'ether'),
                'value': web3.to_wei(0.02, 'ether'),

                'gas': 21000,

                'gasPrice': web3.to_wei('2', 'gwei'),

                'nonce': nonce,

                'chainId': 11155111
                # 'chainId': 1
            }

        signed_transaction = web3.eth.account.sign_transaction(transaction_dict, request.session['account']['privateKey'])
        transaction_hashed = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    except Web3RPCError as e:
        return HttpResponse(e.message)
    except InvalidAddress as e:
        return HttpResponse(e.message)
    except ContractLogicError as ce:
        return HttpResponse(ce.message)
    return JsonResponse(data=json.dumps(transaction_hashed.hex()),safe=False)

