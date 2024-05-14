const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 10000;
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply);
};
