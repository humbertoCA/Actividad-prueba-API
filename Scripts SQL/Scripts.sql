use test_db;
select * from transactions;
TRUNCATE TABLE transactions;
ALTER TABLE transactions ADD UNIQUE (folio);
