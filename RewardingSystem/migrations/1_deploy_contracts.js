const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 199999999901000;
  const initialHolder = '0x71C994D401783a87893B23D41AFefc125eC79748'; 
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply, initialHolder);
};
