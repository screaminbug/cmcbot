# Coinmarketcap scraper

Scrape CMC for market data and store it to MySQL database.

Works with Python 3 (and probably 2.7 as well, not tried)

Requirements:
```
pip install scrapy
pip install mysqlclient
```

Create a MySQL database (the name of the database and the table can be changed in settings.py)

```sql
-- -----------------------------------------------------
-- Schema cmcbot
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cmcbot` DEFAULT CHARACTER SET utf8 ;
USE `cmcbot` ;

-- -----------------------------------------------------
-- Table `cmcbot`.`markets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cmcbot`.`markets` (
  `guid` CHAR(32) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT '?',
  `ticker` VARCHAR(10) NULL DEFAULT '?',
  `pair` VARCHAR(45) NULL DEFAULT '?',
  `exchange` VARCHAR(45) NULL DEFAULT '?',
  `price_usd` DECIMAL(16,4) NULL DEFAULT '0.0000',
  `price_btc` DECIMAL(16,8) NULL DEFAULT '0.00000000',
  `volume_usd` DECIMAL(16,4) NULL DEFAULT '0.0000',
  `volume_btc` DECIMAL(16,8) NULL DEFAULT '0.00000000',
  `market_percent` DECIMAL(8,4) NULL DEFAULT '0.0000',
  `last_updated` TIMESTAMP(6) NULL DEFAULT NULL,
  `updated` TIMESTAMP(6) NULL DEFAULT NULL,
  PRIMARY KEY (`guid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
```

Create a cmcbot user and give it access to the database

Run scrapy from project directory:

```
scrapy crawl markets
```

Enjoy
