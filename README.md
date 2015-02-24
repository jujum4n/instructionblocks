# Instruction Blocks

Instruction Blocks is an open source program that creates a VM and stores its instructions in a given Blockstore key value pair on the Bitcoin Blockchain. Instruction blocks built in VM is currently extraordinarily basic, currently it just has a few branching statements, and addition, subtraction, more complicated VM's will be explored later (Emscripten).

  - Written in Python
  - Pick and Run different Algorithims directly from the Blockchain
  - Magic so far because it does not work and I don't know how to make it work exactly.

### Version
v0.0.1

### Technology

Instruction Blocks uses a number of open source projects to work at a high level you will need:

* [Blockstore] - Using Blockstored server
* [Bitcoin] - Bitcoin Core for bitcoind node
* [Instruction Blocks] - InstructionBlocks functions
* [pybitcointools] - Vbuterins Pybitcointools for address generation / validation functions Could be replaced with RPC calls

### Installation

You need: Python 2.7.x, Blockstored, fully updated valid Bitcoind node,

```sh
$ pip install Blockstore
$ pip install pybitcointools
$ pip install InstructionBlocks
```
### Usage
```sh
$ python ibgen <.blockpy application> <privatekey>
$ Application <applicationname> stored with key <applicationname> in <blocknumber> with <privatekey>
$To retreive this application call on <applicationname>
```

### Development

Want to contribute? Great!
Contact juju@protonmail.ch

### Todo's

 - Better VM, more instructions, more registers etc. 
 - Emscripten route
 - Web Interface of Algorithims in Chain
 - Private Public Algorithims
 - Coolness

License
----
MIT

[Blockstore]:https://github.com/openname/blockstore
[Bitcoin]:http://www.bitcoin.org

