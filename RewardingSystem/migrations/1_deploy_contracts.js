const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 199999999901000;
  const initialHolder = '0xfD1Ce8c692E55e2D227BB2138B045862b7e194b4'; 
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply, initialHolder);
};
