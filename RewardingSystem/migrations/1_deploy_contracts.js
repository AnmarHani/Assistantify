const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 199999999901000;
  const initialHolder = '0x35BcFfFAD827B28F0492592c5564De7E26585174'; 
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply, initialHolder);
};
