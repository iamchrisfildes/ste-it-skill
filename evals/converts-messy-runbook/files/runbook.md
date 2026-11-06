# Restoring the inventory database

So if the inventory DB gets corrupted or someone drops a table by accident (it happens), here's how you get it back. First off, make sure you've actually got access to the backups bucket - you need to be in the `inventory-ops` group, otherwise the download is just going to fail with a 403 and you'll be scratching your head.

Grab the latest dump with `aws s3 cp s3://acme-inventory-backups/nightly/latest.dump ./latest.dump` and then stop the inventory service so nothing writes to the DB while you're mid-restore: `kubectl scale deployment inventory-api --replicas=0 -n inventory`.

Then kick off the restore with `pg_restore --clean --if-exists -d "$INVENTORY_DB_URL" ./latest.dump`. It'll take somewhere around 10-15 minutes for a full restore, so don't panic if it looks stuck.

Once that's done, bring the service back up with `kubectl scale deployment inventory-api --replicas=3 -n inventory` and hit `https://inventory.internal.acme.io/ready` to make sure it's happy - you should get a 200 back.

Oh and whatever you do, don't run the restore against prod without telling #inventory-oncall first, because the nightly reconciliation job will freak out and start firing alerts at everyone if the row counts suddenly change under it.
