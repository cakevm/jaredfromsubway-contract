// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.15;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "forge-std/console.sol";

interface IMain {
}


interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}
interface IWETH9 is IERC20 {
}


contract BasicTests is Test {
    address constant public OWNER = 0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13;
    address constant public UNDER_TEST_ADDRESS = 0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80;

    address constant public WETH_TOKEN = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address constant public TOKEN = 0xd749B369d361396286f8CC28a99Dd3425AC05619;


    IERC20 public token;
    IWETH9 public wethToken;

    IMain public underTest;

    /// Setup the testing environment.
    function setUp() public {
        token = IERC20(TOKEN);
        wethToken = IWETH9(WETH_TOKEN);

        string memory rpc = vm.envString("ETH_MAINNET_HTTP");
        uint forkId = vm.createFork(rpc, 20055365);
        vm.selectFork(forkId);

        // Comment those two lines to test against deployed contract
        IMain tmp = IMain(HuffDeployer.deploy("Jared"));
        vm.etch(UNDER_TEST_ADDRESS, address(tmp).code);

        underTest = IMain(UNDER_TEST_ADDRESS);
    }

    function buildCalldataSwapV2(
        bytes1 command0,
        bytes1 command1,
        address pair,
        bytes4 amount1Out
    ) public pure returns (bytes memory) {
        return abi.encodePacked(
            command0,
            command1,
            pair,
            amount1Out
        );
    }

    function overwriteLastByte(bytes32 a, bytes32 b) public pure returns (bytes32) {
        bytes32 mask = hex"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00";
        bytes32 result = (a & mask) | (b & hex"00000000000000000000000000000000000000000000000000000000000000FF");
        return result;
    }

    function testUniV2Swap() public {
        // Test for: https://etherscan.io/tx/0xd8b2c5c012bbcfb5e63c96a0e762b2307b16e5bd999901f461db6b6d901171a0
        assertEq(token.balanceOf(address(UNDER_TEST_ADDRESS)), 10983779858320589424235925);
        assertEq(wethToken.balanceOf(address(UNDER_TEST_ADDRESS)), 788712975340832617691);

        // modify target block number because foundry always reads state for full block height
        bytes32 lastByteBlockNumber = bytes32(uint256(block.number & 0xFF)); // jared checks first byte for block number
        bytes32 originalTxValue = bytes32(uint256(34039030598));
        uint256 newValue = uint256(overwriteLastByte(originalTxValue, lastByteBlockNumber));
        console.log("new", newValue);
        // 0x39 = position in calldata of 03006d18
        bytes memory dataBuy = buildCalldataSwapV2(hex"04", hex"39", address(0xDe85312e4483811e24D9A590848bF5eF34D5A259), hex"03006d18");

        // call value 7ECE26345 + 000000 wed transfer
        // tx was +1 block there it is 7ECE26346 000000 = 571080168773255168
        vm.prank(OWNER);
        (bool res1,) = address(UNDER_TEST_ADDRESS).call{value: newValue}(dataBuy); // BUY
        assert(res1);

        assertEq(token.balanceOf(address(UNDER_TEST_ADDRESS)), 14612569741650768199751061);
        assertEq(wethToken.balanceOf(address(UNDER_TEST_ADDRESS)), 788141895172076139739);

        // Frontrunned tx
        bytes memory inputFrontrun = hex"3593564c000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000006665d5f300000000000000000000000000000000000000000000000000000000000000040b080604000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000028000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000011c37937e08000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000011c37937e080000000000000000000000000000000000000000000000006615883bfd617b37814900000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000d749b369d361396286f8cc28a99dd3425ac056190000000000000000000000000000000000000000000000000000000000000060000000000000000000000000d749b369d361396286f8cc28a99dd3425ac05619000000000000000000000000000000fee13a103a10d593b9ae06b3e05f2e7e1c00000000000000000000000000000000000000000000000000000000000000190000000000000000000000000000000000000000000000000000000000000060000000000000000000000000d749b369d361396286f8cc28a99dd3425ac0561900000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000065d432c6146d65c9ed1e";
        vm.prank(address(0xBCbe23B75b39DCcAe1C8c453e986980Ae91343E2));
        (bool res2,) = address(address(0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD)).call{value: 0.08 ether}(inputFrontrun);
        assert(res2);

        // Modify target block number because foundry always reads state for full block height
        bytes32 originalTxValueSell = bytes32(uint256(34267739206));
        uint256 newValueSell = uint256(overwriteLastByte(originalTxValueSell, lastByteBlockNumber));

        // amount1Out = 3006d17 + 00000000000000 = 3628789811272584737587200 token
        bytes memory dataSell = buildCalldataSwapV2(hex"82", hex"39", address(0xd749B369d361396286f8CC28a99Dd3425AC05619), hex"03006d17");

        vm.prank(OWNER);
        (bool res3,) = address(UNDER_TEST_ADDRESS).call{value: newValueSell}(dataSell); // BUY
        assert(res3);

        assertEq(token.balanceOf(address(UNDER_TEST_ADDRESS)), 10983779930378183462163861);
        assertEq(wethToken.balanceOf(address(UNDER_TEST_ADDRESS)), 788716812434550093019);
    }

    function testWithdrawETH() public {
        assertEq(address(OWNER).balance, 166_110626569390645681);

        bytes32 lastByteBlockNumber = bytes32(uint256(block.number & 0xFF));
        bytes32 originalTxValue = bytes32(uint256(5960464477626));
        uint256 newValue = uint256(overwriteLastByte(originalTxValue, lastByteBlockNumber));

        bytes memory data = hex"2d";
        vm.prank(OWNER);
        (bool res,) = address(UNDER_TEST_ADDRESS).call{value: newValue}(data);
        assert(res);

        assertEq(address(OWNER).balance, 266_110655972722991066);
    }

    function testSelfdestruct() public {
        assertEq(address(OWNER).balance, 166_110626569390645681);

        bytes32 lastByteBlockNumber = bytes32(uint256(block.number & 0xFF));
        bytes32 originalTxValue = bytes32(uint256(0));
        uint256 newValue = uint256(overwriteLastByte(originalTxValue, lastByteBlockNumber));

        bytes memory data = hex"2e";
        vm.prank(OWNER);
        (bool res,) = address(UNDER_TEST_ADDRESS).call{value: newValue}(data);
        assert(res);

        assertEq(address(OWNER).balance, 166_110655973227356122);
    }
}