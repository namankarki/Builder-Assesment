from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
    )

algorand = AlgorandClient.default_local_net()
dispenser = algorand.account.dispenser()

creator = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )  )

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender= creator.address,
        total= 5000,
        asset_name="MAXER",
        unit_name= "MAX",
        manager=creator.address,
        clawback=creator.address,
        freeze= creator.address
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
print(asset_id)

receiver = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver.address,
        amount=10_000_000
    )
 )
group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender= receiver.address,
        asset_id= asset_id
    )
)

group_tx.add_payment(
    PayParams(
        sender= receiver.address,
        receiver= creator.address,
        amount= 1_000_000
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender= creator.address,
        receiver= receiver.address,
        asset_id= asset_id,
        amount= 100
    )
)

group_tx.execute()

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])

algorand.send.asset_transfer(
    AssetTransferParams(
        sender= creator.address,
        asset_id= asset_id,
        clawback_target= receiver.address,
        amount= 1,
        receiver= creator.address
    )
)
print("Receiver Account Asset Balance:", algorand.account.get_information(receiver.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])
