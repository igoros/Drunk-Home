SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Cocktails`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Cocktails` (
  `CocktailID` INT NOT NULL ,
  `CocktailName` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`CocktailID`) ,
  UNIQUE INDEX `CocktailName_UNIQUE` (`CocktailName` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pictures`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Pictures` (
  `CocktailID` INT NOT NULL AUTO_INCREMENT ,
  `PicturePath` VARCHAR(100) NOT NULL DEFAULT 'blank pic path here' ,
  PRIMARY KEY (`CocktailID`) ,
  INDEX `CocktailID` (`CocktailID` ASC) ,
  CONSTRAINT `CocktailID`
    FOREIGN KEY (`CocktailID` )
    REFERENCES `mydb`.`Cocktails` (`CocktailID` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Recipes`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Recipes` (
  `CocktailID` INT NOT NULL ,
  `IngredientIDs` VARCHAR(1000) NOT NULL ,
  `RecipeText` VARCHAR(10000) NULL ,
  PRIMARY KEY (`CocktailID`) ,
  INDEX `CocktailID` (`CocktailID` ASC) ,
  CONSTRAINT `CocktailID`
    FOREIGN KEY (`CocktailID` )
    REFERENCES `mydb`.`Cocktails` (`CocktailID` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Comments`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Comments` (
  `CocktailID` INT NOT NULL ,
  `Rating` FLOAT(4) NULL ,
  `CommentText` VARCHAR(45) NULL ,
  INDEX `CocktailID` (`CocktailID` ASC) ,
  CONSTRAINT `CocktailID`
    FOREIGN KEY (`CocktailID` )
    REFERENCES `mydb`.`Cocktails` (`CocktailID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Ingredients`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `mydb`.`Ingredients` (
  `IngredientName` VARCHAR(100) NULL ,
  `AltID` INT(10) ZEROFILL NULL ,
  `IngredientID` INT(10) NOT NULL ,
  UNIQUE INDEX `IngredientName_UNIQUE` (`IngredientName` ASC) ,
  PRIMARY KEY (`IngredientID`) )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
