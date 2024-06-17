import requests
import os
from joblib import Memory


memory = Memory("cache")

PATH = os.path.dirname(os.path.realpath(__file__))
DISASSEMBLED_FILE = os.path.join(PATH, "../../resources/disassembled.evm")
CONTRACT_BYTECODE_FILE = os.path.join(PATH, "../../resources/contract.bytecode")
TARGET_FILE = os.path.join(PATH, "../../../src/Jared.huff")

COMMAND_SHIFT = 0x06

HUFF_MAIN_START = "#define macro MAIN() = takes (0) returns (0) {"
HUFF_TABLE_START = "#define table {name} {"

COMMANDS = {0x04: {"name": "univ2_weth_token", "comment": "uniswap v2 WETH -> TOKEN",
                   "example": "https://etherscan.io/tx/0x4cc87bdbb974e8df68403a44f37adc48f1911af9dc4ab26084429ae1016ee551"},
            0x02: {"name": "univ3_remove_liq", "comment": "uni v3 remove liquidity + swap",
                   "example": "https://etherscan.io/tx/0xcfbb2c3fe3d8314e7c0aa8416b5cb361742eb53b4dbea621533c00974b4a0f5a"},
            0x09: {"name": "univ3_add_liq", "comment": "add v3 liq + swap",
                   "example": "https://etherscan.io/tx/0x54b3de5b4fc4434e59e308d881e160462dfb8c6605b96d0bb3ab830971dbe0c4"},
            0x0d: {"name": "univ2_uscd_token", "comment": "uni v2 TOKEN (USCD) - TOKEN",
                   "example": "https://etherscan.io/tx/0x2c6d64fbded7aa9a88794153f5ab1aa2e60c199d61cbf3d466c231da363130f4"},
            0x0f: {"name": "univ2_univ3_arb", "comment": "univ2, v3",
                   "example": "https://etherscan.io/tx/0xde0bc1b5cb64e1dcdaf56bc420525c2d4ff7f30897a89bc7d052a25b30ac80f6"},
            0x13: {"name": "univ2_usdt_token", "comment": "usdt -> token univ2",
                   "example": "https://etherscan.io/tx/0x103697cc14a3bdfe7934e43debccd389b86fe3754dee816eea02a1fb8171c5c5"},
            0x15: {"name": "univ2_usdt_multi", "comment": "univ2 USDT - univ2 multiple",
                   "example": "https://etherscan.io/tx/0xb6d9836aef79dd02c46e48fa40e73fc8b0a5a3965cf2f4b520b3d0fea29738b7"},
            0x19: {"name": "sushi_token_weth", "comment": "sushi token -> weth",
                   "example": "https://etherscan.io/tx/0xcbcf2f04125d142328abc53360abe2533516973f0f7e6870ba6413245fc83947"},
            0x1b: {"name": "sushi_tokhen_weth_again", "comment": "sushiswap token -> weth",
                   "example": "https://etherscan.io/tx/0x6e3584149b8ba05f5d839c632a8f4ea5508581d7bda5fbbdfdaf0c45d0bd208f"},
            0x1d: {"name": "sushi_uni_arb", "comment": "sushi, uni arb",
                   "example": "https://etherscan.io/tx/0x71ea0ad0179b3887639408b1561c884159bf519dde33ddd2a79984b238c463f8"},
            0x1f: {"name": "sushi_two", "comment": "two swaps sushi",
                   "example": "https://etherscan.io/tx/0x9d099d1329a725ab3c12c52d2ee9a411f535c9bc05f84e47deba1fb3e2d15b59"},
            0x23: {"name": "univ2_token_usdc", "comment": "univ2 TOKEN -> TOKEN (USDC)",
                   "example": "https://etherscan.io/tx/0x6d2477dbf665c9561d056033f869d0e4ea9d7bc87d1febd02f0d65f64194671e"},
            0x25: {"name": "univ2_multi", "comment": "univ2 - multiple",
                   "example": "https://etherscan.io/tx/0x1e41c03cf37a1435c5f15239066aba31c3973f2972a58b9a9f4c175558357107"},
            0x27: {"name": "univ2_token_usdc_again", "comment": "token -> usdc univ2",
                   "example": "https://etherscan.io/tx/0xba5b98252105561b58b977f7c64d95fd26d1a390f41c2c63614eb7e061ca1e63"},
            0x29: {"name": "univ2_v3_swap", "comment": "swaps univ2, v3",
                   "example": "https://etherscan.io/tx/0xef4c146f49acf8742ad111ac75df14b1ea6b8c581651ef526b390bea0acbadae"},
            0x2b: {"name": "univ2_arb_token_token", "comment": "univ2 arb token-token",
                   "example": "https://etherscan.io/tx/0xec055cffb6c01fce66b71cae9826c575b65ab056162d8778eeccccde377f4304"},
            0x2d: {"name": "withdraw_eth", "comment": "withdraw ETH",
                   "example": "https://etherscan.io/tx/0xf48772f5a49a18e7ee0a7f005229396a8cd32e8f1630a09884b5500c6510eae4"},
            0x2e: {"name": "self_destruct", "comment": "self destruct",
                   "example": "https://etherscan.io/tx/0xc1d028ab9f0a2f50e22ff1963f5e1fe6ab8bd364c0c2b81a6875aa89a8ec6e88"},
            0x57: {"name": "univ3_usdt_weth", "comment": "USDT -> WETH univ3",
                   "example": "https://etherscan.io/tx/0x090ceb83d76f40864aa03c6aa43fc9ed4585e253e5c7e217a045cd71c0cfe4dc"},
            0x59: {"name": "univ3_weth_token", "comment": "swap v3 WETH -> TOKEN",
                   "example": "https://etherscan.io/tx/0x0680c5c80774ee28749a0e5a66e3bc6c4ef7373f9976a7def0f313be2f1e8d54"},
            0x5c: {"name": "univ3_usdt_weth_again", "comment": "usdt -> weth univ3",
                   "example": "https://etherscan.io/tx/0xba028689d9b4a3e40d3aeae676e03b2c788a63a72ac1670603417d173d59c943"},
            0x5e: {"name": "univ3_token_weth", "comment": "swap v3 TOKEN -> WETH",
                   "example": "https://etherscan.io/tx/0x8d80af5cf67eb1943f4004380770ee4eb0f69ac2fdd353dd296da8c51d4ef1d9"},
            0x7c: {"name": "univ2_token_weth_other", "comment": "univ2 token -> weth",
                   "example": "https://etherscan.io/tx/0xe952bd1a30235ca6c4cd7411cb04603b17be968a30d2ee08e0d72531e023ed01"},
            0x7f: {"name": "univ3_liq_swap", "comment": " univ3 liq + swap",
                   "example": "https://etherscan.io/tx/0xe235466395c4b549e6697a6d5bab3fcc4ed0deaec041eddbcbb4256b9c1c2e8b"},
            0x82: {"name": "univ2_token_weth_other2", "comment": "uniswap v2 TOKEN -> WETH",
                   "example": "https://etherscan.io/tx/0xe98f6d05e578f40d803f1e42f088d5d3a85b1fe761c74bce44f5a20185145eca"},
            0x85: {"name": "univ2_token_token", "comment": "arb univ2 token -> token",
                   "example": "https://etherscan.io/tx/0xfd0e326c17956bee753b63ebcc45ced4bbdd7dd38cd9d38881ca4e80f8b99167"},
            }


def shl(value, shift):
    return value << shift


names = {}
new_commands_shifted = {}
for command, command_details in COMMANDS.items():
    # validate no duplicate names
    if command_details['name'] in names:
        print(f"Duplicate: {command_details['name']}")
        exit()
    names[command_details['name']] = command
    # all shifted by: push1 0x06, shl
    new_commands_shifted[shl(command, COMMAND_SHIFT)] = command_details
COMMANDS = new_commands_shifted

KNOWN_JUMP_ADDRESSES = {
    0x28: {"name": "dispatcher", "comment": "dispatcher", "example": ""},
    0x342f: {"name": "univ3_callback", "comment": "univ3 callback", "example": ""}
}
COMMANDS = COMMANDS | KNOWN_JUMP_ADDRESSES


def load_data():
    data = open(DISASSEMBLED_FILE).read()
    lines = data.strip().split('\n')

    parsed_data = []
    for line in lines:
        parts = line.split(maxsplit=1)
        instruction = {
            'address': parts[0],
            'operation': parts[1].strip().lower() if len(parts) > 1 else None
        }
        parsed_data.append(instruction)

    return parsed_data


@memory.cache
def get_signature(fourbytes):
    r = requests.get(f"https://raw.githubusercontent.com/ethereum-lists/4bytes/master/signatures/{fourbytes}")
    if r.status_code == 200:
        return r.text
    else:
        return ''


def split_string(input_string, chunk_size=64):
    chunks = [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]
    return chunks


def operation_to_huff(operation):
    data = operation.split()
    if len(data) == 1:
        return operation
    return f"{data[0]} 0x{data[1]}"


def parse_codecopy(ops):
    ret = []
    for op in ops:
        op = op['operation']
        if op == 'push0':
            ret.append(0)
        else:
            ret.append(int(op.split(' ')[1], 16))
    return ret


def create_table(table_name, size, offset, original_contract):
    result = []
    table_data = original_contract[offset * 2:offset * 2 + size * 2]
    signature = get_signature(table_data[:8])
    if signature:
        result.append(f"// {signature}")
    result.append(HUFF_TABLE_START.replace("{name}", table_name))
    chunks = split_string(table_data, 64)
    for chunk in chunks:
        result.append(f"    0x{chunk}")

    result.append("}\n")
    return result


def jump_dest_header(address):
    command_address = int(address, 16)
    if command_address in COMMANDS:
        name = f"{COMMANDS[command_address]['name']}"
        comment = f"// {COMMANDS[command_address]['comment']}\n"
        if COMMANDS[command_address]['example']:
            comment += f"// example: {COMMANDS[command_address]['example']}\n"
    else:
        name = f"unknown"
        comment = ""

    return f"\n{comment}_jump_dest_{name}_{address}:"


def main():
    data = load_data()
    original_contract = open(CONTRACT_BYTECODE_FILE).read()
    tables = []
    result = [HUFF_MAIN_START]

    codecopy_count = 0
    for idx, instruction in enumerate(data):
        op = instruction['operation']
        if instruction['operation'] == 'jumpdest':
            for i in range(codecopy_count):
                if 'stop' in result[-1]:
                    del result[-1]

            codecopy_count = 0
            result.append(jump_dest_header(instruction['address']))
        elif instruction['operation'] == 'unknown':
            result.append(f"    stop")
        elif instruction['operation'] == 'codecopy':
            is_create_table = True
            for c in data[idx - 3:idx]:
                if c['operation'] == 'unknown':
                    is_create_table = False
            if is_create_table:
                (size, offset, dest_offset) = parse_codecopy(data[idx - 3:idx])
                table_name = f"table_{idx}"
                tables.append(create_table(table_name, size, offset, original_contract))
                result[-3] = f"    __tablesize({table_name})"
                result[-2] = f"    __tablestart({table_name})"
                if offset <= 255:
                    codecopy_count += 1
                if "PUSH2 00" in data[idx - 3]['operation']:
                    codecopy_count += 1
            result.append(f"    codecopy")
        else:
            result.append(f"    {operation_to_huff(op)}")

    result.append("}")

    # Workarounds:
    # 001703 PUSH2 00e4
    result.insert(4463, "    stop")

    for table in tables:
        result += table

    open(TARGET_FILE, 'w').write("\n".join(result))


if __name__ == '__main__':
    main()
