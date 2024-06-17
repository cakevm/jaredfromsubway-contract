# Decypher jaredfromsubway.eth contract
Converting the contract of `jaredfromsubway.eth` from bytecode to Huff and write some test to validate the behavior.

## Motivation
The goal is to decompile the contract to understand its logic and create a readable version. This allows us all to learn for it. To achieve this, tests are created to validate the behavior of both the deployed and the decompiled contract.

## Status
The original contract was probably not created with Huff. Huff always appends the `CODECOPY` parts at the end of the contract. Jared's contract makes use of a wall of STOP operations to keep the data. For this reason, the decompiled version is longer, and there are some adjustments to keep the `JUMPDEST` instructions in the same place. Currently, not all jump destinations are likely in the correct place.

### Version:
The contract was deployed on Mar-09-2024 03:47:35 AM UTC.\
Contract: [0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80](https://etherscan.io/address/0x6b75d8af000000e20b7a7ddf000ba900b4009a80)\
Deployment: [tx](https://etherscan.io/tx/0xd786b2a619d2aaea4a8886598f5736911368ba6f9175dfd1f49f7c297c9918c6)


## Structure
```
src/
    Jared.huff <- decoded contract
decompile-contract/
    resources/
        disassembled.evm <- original contract
        disassembled.evm <- disassembled contract
    src/
        decompile_contract/convert_to_huff.py <- script to convert the contract to huff
test/
    BasicTests.t.sol <- test the Huff contract
```

## Getting Started

### Requirements
-   [Foundry](https://github.com/gakonst/foundry)
-   [Huff Compiler](https://docs.huff.sh/get-started/installing/)


### Run
In the test you can modify if the Huff or the deployed contract version should be used. The tests require an archive node.
```shell
export ETH_MAINNET_HTTP=<RPC PROVIDER>
forge test
```

### Disassemble contract
The disassembled version in `decompile-contract/resources/disassembled.evm` was created using [heimdall-rs](https://github.com/Jon-Becker/heimdall-rs).
```shell
heimdall disassemble 0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80
```

## Development
If you like to improve the decompiler I am happy to get your help. The decompiler is written in python

1. Create a python virtual environment and install the dependencies:
```shell
cd decompile-contract
pip install -e .
```
2. Run the decompiler:
```shell
python src/decompile_contract/convert_to_huff.py
```
