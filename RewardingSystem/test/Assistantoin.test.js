const Assistantoin = artifacts.require("Assistantoin");

contract("Assistantoin", (accounts) => {
  it("should put the initial supply in the first account", async () => {
    const instance = await Assistantoin.deployed();
    const balance = await instance.balanceOf.call(accounts[0]);
    assert.equal(
      balance.valueOf(),
      10000,
      "The first account doesn't have the initial supply"
    );
  });
});
