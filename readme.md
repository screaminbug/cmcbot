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
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `ticker` VARCHAR(10) NULL DEFAULT NULL,
  `pair` VARCHAR(45) NULL DEFAULT NULL,
  `exchange` VARCHAR(45) NULL DEFAULT NULL,
  `price_usd` DECIMAL(16,8) NULL DEFAULT NULL,
  `price_btc` DECIMAL(16,8) NULL DEFAULT NULL,
  `volume_usd` DECIMAL(16,8) NULL DEFAULT NULL,
  `volume_btc` DECIMAL(16,8) NULL DEFAULT NULL,
  `market_percent` DECIMAL(16,8) NULL DEFAULT NULL,
  `last_updated` TIMESTAMP(6) NULL DEFAULT NULL,
  `updated` TIMESTAMP(6) NULL DEFAULT NULL,
  PRIMARY KEY (`guid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;```

Create a cmcbot user and give it access to the database

Run scrapy from project directory:
```
scrapy crawl markets
```

Enjoy
