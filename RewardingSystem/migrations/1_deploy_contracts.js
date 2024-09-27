const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 199999999901000;
  const initialHolder = '0xF479dd7a42AbCc74C67d9e427d11b2C4873049CD'; 
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply, initialHolder);
};
