-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema guia_canino
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema guia_canino
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `guia_canino` DEFAULT CHARACTER SET utf8 ;
USE `guia_canino` ;

-- -----------------------------------------------------
-- Table `guia_canino`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rol` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `number_phone` VARCHAR(45) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `address` VARCHAR(200) NOT NULL,
  `is_admin` TINYINT NOT NULL DEFAULT 0,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `rol_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_roles_idx` (`rol_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_roles`
    FOREIGN KEY (`rol_id`)
    REFERENCES `guia_canino`.`roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`races`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`races` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `danger` TINYINT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`dogs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`dogs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  `color` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `owner_id` INT NOT NULL,
  `race_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_dogs_users1_idx` (`owner_id` ASC) VISIBLE,
  INDEX `fk_dogs_races1_idx` (`race_id` ASC) VISIBLE,
  CONSTRAINT `fk_dogs_users1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dogs_races1`
    FOREIGN KEY (`race_id`)
    REFERENCES `guia_canino`.`races` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`walkers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`walkers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `users_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_walkers_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_walkers_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `guia_canino`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`walks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`walks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_start` DATETIME NOT NULL,
  `date_end` DATETIME NOT NULL,
  `walker_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_walks_walkers1_idx` (`walker_id` ASC) VISIBLE,
  CONSTRAINT `fk_walks_walkers1`
    FOREIGN KEY (`walker_id`)
    REFERENCES `guia_canino`.`walkers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `guia_canino`.`dogs_has_walks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `guia_canino`.`dogs_has_walks` (
  `dog_id` INT NOT NULL,
  `walk_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`dog_id`, `walk_id`),
  INDEX `fk_dogs_has_walks_walks1_idx` (`walk_id` ASC) VISIBLE,
  INDEX `fk_dogs_has_walks_dogs1_idx` (`dog_id` ASC) VISIBLE,
  CONSTRAINT `fk_dogs_has_walks_dogs1`
    FOREIGN KEY (`dog_id`)
    REFERENCES `guia_canino`.`dogs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dogs_has_walks_walks1`
    FOREIGN KEY (`walk_id`)
    REFERENCES `guia_canino`.`walks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE `guia_canino`.`users`
CHANGE COLUMN `created_at` `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ;




SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
