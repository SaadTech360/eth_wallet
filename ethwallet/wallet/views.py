from django.shortcuts import render
from web3  import Web3
import requests,json
from decouple import config
from django.http import HttpResponse, JsonResponse

KEY = config('API_KEY')

API_URL = f"https://mainnet.infura.io/v3/{KEY}"
web3 = Web3(Web3.HTTPProvider(API_URL))

def create_account(request):
    account = web3.eth.account.create('enter password')
    request.session['account']={
        'privateKey': account.key.hex(),
        'address': account.address,
    }
    return JsonResponse(data=request.session['account'])

with open('erc20_abi.json') as f:
    erc20_abi = json.load(f)

def get_balance(request,contract_address):
    address = request.session.get('account').get('address')
    checksum_address = Web3.to_checksum_address(address)
    print(checksum_address)
    contract = web3.eth.contract(address=contract_address, abi=erc20_abi)
    balance = contract.functions.balanceOf(checksum_address).call()
    return JsonResponse(data=balance,safe=False)

def send_transaction(request):
    try:
        addr = '0x2AC03BF434db503f6f5F85C3954773731Fc3F056'
        nonce = web3.eth.get_transaction_count(request.session['account']['address'])
        transaction_dict = {

                # 'to': data['to'],
                'to': addr,

                # 'value': web3.toWei(data['amount'], 'ether'),
                'value': web3.to_wei(100, 'ether'),

                'gas': 2000000,

                'gasPrice': web3.to_wei('40', 'gwei'),

                'nonce': nonce,

                'chainId': 1
            }

        signed_transaction = web3.eth.account.sign_transaction(transaction_dict, request.session['account']['privateKey'])
        transaction_hashed = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    except:
        return HttpResponse('low fund')
        return JsonResponse(json.dumps(data=transaction_hashed.hex()))




"""def send_transaction(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    # Parse JSON (Django doesn't have request.get_json())
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Validate required fields
    if 'to' not in data or 'amount' not in data:
        return JsonResponse({'error': 'Missing "to" or "amount"'}, status=400)

    # Get sender details from session (adjust based on your auth system)
    if 'account' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    account = request.session['account']
    
    try:
        # Prepare transaction
        nonce = web3.eth.get_transaction_count(account['address'])
        txn_dict = {
            'to': data['to'],
            'value': web3.to_wei(float(data['amount']), 'ether'),
            'gas': 2000000,
            'gasPrice': web3.to_wei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3  # Ropsten testnet
        }

        # Sign and send
        signed_txn = web3.eth.account.sign_transaction(txn_dict, account['privateKey'])
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return JsonResponse({
            'transaction_hash': txn_hash.hex()
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)"""