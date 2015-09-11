import math
import logging
from functools import partial

from bitcoin import *

# from contracts.json via Truffle
TOKEN_FACTORY_BINARY = '60606040526110e8806100136000396000f30060606040526000357c01000000000000000000000000000000000000000000000000000000009004806305215b2f1461004f5780635f8dead31461008c578063dc3f65d3146100cf5761004d565b005b610060600480359060200150610231565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100a3600480359060200180359060200150610124565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600450610175565b60405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390f35b60006000506020528160005260406000206000508181548110156100025790600052602060002090016000915091509054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6020604051908101604052806000815260200150600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005080548060200260200160405190810160405280929190818152602001828054801561022257602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16815260200190600101908083116101ee575b5050505050905061022e565b90565b600060006000600084604051610c7f8061046983390180828152602001915050604051809103906000f092508291508173ffffffffffffffffffffffffffffffffffffffff1663c86a90fe8633604051837c0100000000000000000000000000000000000000000000000000000000028152600401808381526020018273ffffffffffffffffffffffffffffffffffffffff168152602001925050506020604051808303816000876161da5a03f1156100025750505060405151506001600060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000508181540191508181548183558181151161036957818360005260206000209182019101610368919061034a565b80821115610364576000818150600090555060010161034a565b5090565b5b505050905082600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060018303815481101561000257906000526020600020900160006101000a81548173ffffffffffffffffffffffffffffffffffffffff0219169083021790555080600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081815481835581811511610454578183600052602060002091820191016104539190610435565b8082111561044f5760008181506000905550600101610435565b5090565b5b50505050829350610460565b50505091905056006060604052604051602080610c7f8339016040526060805190602001505b80600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b50610c1d806100626000396000f300606060405236156100b6576000357c0100000000000000000000000000000000000000000000000000000000900480631fa03a2b146100b857806321af4feb146100e557806327e235e314610112578063673448dd1461013957806367eae67214610160578063930b7a2314610193578063bbd39ac0146101ac578063c86a90fe146101d3578063d26c8a8a14610200578063daea85c514610221578063f4b1604514610234578063fbf1f78a14610261576100b6565b005b6100cf600480359060200180359060200150610ac0565b6040518082815260200191505060405180910390f35b6100fc600480359060200180359060200150610bf2565b6040518082815260200191505060405180910390f35b610123600480359060200150610ba2565b6040518082815260200191505060405180910390f35b61014a6004803590602001506109df565b6040518082815260200191505060405180910390f35b61017d6004803590602001803590602001803590602001506103a8565b6040518082815260200191505060405180910390f35b6101aa60048035906020018035906020015061077b565b005b6101bd600480359060200150610666565b6040518082815260200191505060405180910390f35b6101ea600480359060200180359060200150610274565b6040518082815260200191505060405180910390f35b61020b60045061062a565b6040518082815260200191505060405180910390f35b6102326004803590602001506106a4565b005b61024b600480359060200180359060200150610bbd565b6040518082815260200191505060405180910390f35b610272600480359060200150610843565b005b600082600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156103985782600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555082600060005060008473ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146856040518082815260200191505060405180910390a3600190506103a2566103a1565b600090506103a2565b5b92915050565b6000600083600060005060008773ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156106215760009050600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561045c57600190508050610524565b600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054841015610523576001905080506000600260005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b5b60018114156106175783600060005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555083600060005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146866040518082815260200191505060405180910390a36001915061062256610620565b60009150610622565b5b5b509392505050565b6000600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050549050610663565b90565b6000600060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061069f565b919050565b6001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060016040518082815260200191505060405180910390a35b50565b80600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e836040518082815260200191505060405180910390a35b5050565b6000600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060006040518082815260200191505060405180910390a38073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e60006040518082815260200191505060405180910390a35b50565b60006001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610aac57506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610aba5760019050610abb565b5b919050565b60006001600160005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610b8d57506000600260005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610b9b5760019050610b9c565b5b92915050565b60006000506020528060005260406000206000915090505481565b60016000506020528160005260406000206000506020528060005260406000206000915091509054906101000a900460ff1681565b600260005060205281600052604060002060005060205280600052604060002060009150915050548156'
TOKEN_FACTORY_ABI = '[{"inputs":[{"type":"uint256","name":"_initialAmount"}],"constant":false,"name":"createStandardToken","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"uint256","name":""}],"constant":true,"name":"created","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[],"constant":false,"name":"createdByMe","outputs":[{"type":"address[]","name":""}],"type":"function"}]';

TOKEN_CONTRACT_ABI = '[{"inputs":[{"type":"address","name":"_target"},{"type":"address","name":"_proxy"}],"constant":true,"name":"isApprovedFor","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved_once","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""}],"constant":true,"name":"balances","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_proxy"}],"constant":true,"name":"isApproved","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_from"},{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoinFrom","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"who","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[],"constant":true,"name":"sendr","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_maxValue"}],"constant":false,"name":"approveOnce","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"coinBalanceOf","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoin","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[],"constant":true,"name":"coinBalance","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"approve","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved","outputs":[{"type":"bool","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"unapprove","outputs":[],"type":"function"},{"inputs":[{"type":"uint256","name":"_initialAmount"}],"type":"constructor"},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"CoinTransfer","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"bool","name":"result"}],"type":"event","name":"AddressApproval","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"AddressApprovalOnce","anonymous":false}]'

TOKEN_ENDOWMENT = 2**200
REWARD_PER_HEADER = 1000
FEE_VERIFY_TX = 12 * REWARD_PER_HEADER

#
# helper functions for relayTx testing
#

def initBtcRelayTokens(cls, tester):
    tfAddr = cls.s.evm(TOKEN_FACTORY_BINARY.decode('hex'))
    _abi = TOKEN_FACTORY_ABI
    TOKEN_FACTORY = tester.ABIContract(cls.s, _abi, tfAddr, listen=True, log_listener=None)

    tokenContractAddr = cls.c.initTokenContract(TOKEN_FACTORY.address)

    _abi = TOKEN_CONTRACT_ABI
    _address = hex(tokenContractAddr)[2:-1].decode('hex')
    cls.xcoin = tester.ABIContract(cls.s, _abi, _address, listen=True, log_listener=None)


def makeMerkleProof(header, hashes, txIndex):
    proof = mk_merkle_proof(header, hashes, txIndex)  # from pybitcointools

    txHash = int(proof['hash'], 16)
    siblings = map(partial(int,base=16), proof['siblings'])
    txBlockHash = int(proof['header']['hash'], 16)

    return [txHash, txIndex, siblings, txBlockHash]


def randomMerkleProof(blocknum, txIndex=-1, withMerkle=False):
    header = get_block_header_data(blocknum)
    hashes = get_txs_in_block(blocknum)

    numTx = len(hashes)
    if numTx == 0:
        print('@@@@ empty blocknum='+str(blocknum))
        return

    index = random.randrange(numTx) if txIndex == -1 else txIndex

    print('txStr='+hashes[index])

    proof = mk_merkle_proof(header, hashes, index)

    print('@@@@@@@@@@@@@@@@ blocknum='+str(blocknum)+'\ttxIndex='+str(index))

    txHash = int(hashes[index], 16)
    siblings = map(partial(int,base=16), proof['siblings'])
    txBlockHash = int(header['hash'], 16)

    ret = [txHash, index, siblings, txBlockHash]  # note: just 'index' here
    if withMerkle:
        ret.append(int(proof['header']['merkle_root'], 16))
    return ret


def dblSha256Flip(rawBytes):
    return int(bin_sha256(bin_sha256(rawBytes))[::-1].encode('hex'), 16)


def disablePyethLogging():
    logging.getLogger('eth.pb').setLevel('INFO')
    logging.getLogger('eth.pb.msg').setLevel('INFO')
    logging.getLogger('eth.pb.msg.state').setLevel('INFO')
    logging.getLogger('eth.pb.tx').setLevel('INFO')
    logging.getLogger('eth.vm').setLevel('INFO')
    logging.getLogger('eth.vm.op').setLevel('INFO')
    logging.getLogger('eth.vm.exit').setLevel('INFO')
    logging.getLogger('eth.chain.tx').setLevel('INFO')
    logging.getLogger('transactions.py').setLevel('INFO')
    logging.getLogger('eth.msg').setLevel('INFO')
