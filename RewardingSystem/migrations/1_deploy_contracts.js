const Assistantoin = artifacts.require("Assistantoin");

module.exports = function(deployer) {
  // Update the constructor parameters if necessary
  const initialSupply = 199999999901000;
  const initialHolder = '0xb37c7B2c4EF5cBa06A2d10E68C241E6870810117'; 
  deployer.deploy(Assistantoin, "ASSISTANTOIN", "ATN", initialSupply, initialHolder);
};
