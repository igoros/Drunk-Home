-- @dovtu: added "Trivial" enum field to Ingredients Table, Trivial Ingredients are best described be example: suger, salt, ice, etc
-- @dovtu: added "Basic" enum field to Ingredients Table, basic Ingredients are best described by example: Juices, Cola, etc...
-- @dovtu: changed 'add_blank_pic_path_here' to the actual no_pic.gif on the server
-- @mosheshpilman: @dovtu's changes were correct although partial, we have to completly split the "comments" table to 2 tables
-- @mosheshpilman: I split Comments table to: 1. Comments 2. rating, before I split it didnt make any sense at all,
-- @mosheshpilman: for each comment there was ITS OWN RATING which ment that there can be 1+ diffrent ratings, all unconnected...
-- @mosheshpilman: also added the 'alter table' command to add foreign key to the new table "Rating".
-- @igoros: all your changes are relevamt and correct, but you forgot 1 critical thing... we changed the DB format to UTF-8 so that we can have special chars inside recipes/comments...
-- @igoros: i added the 'DEFAULT CHARSET=utf8' to all tables...
-- -----------------------------------------------------
-- Table mydb.Cocktails
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Cocktails
(
  CocktailID INT(10),
  CocktailName VARCHAR(100) NOT NULL ,
  PRIMARY KEY (CocktailID)
)DEFAULT CHARSET=utf8;

-- -----------------------------------------------------
-- Table mydb.Pictures
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Pictures
(
  CocktailID INT(10),
  PicturePath VARCHAR(100) NOT NULL DEFAULT 'no_pic.gif' ,
  PRIMARY KEY (CocktailID)
)DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table mydb.Recipes
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Recipes (
  CocktailID INT(10),
  PRIMARY KEY (CocktailID),
  IngredientIDs VARCHAR(1000) NOT NULL ,
  RecipeText VARCHAR(10000) NULL

)DEFAULT CHARSET=utf8;



-- -----------------------------------------------------
-- Table mydb.Comments
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Comments (
  CocktailID int(10) DEFAULT NULL,
  Text varchar(300) DEFAULT NULL
)DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Rating (
  CocktailID int(10) DEFAULT NULL,
  CurrentRating float DEFAULT NULL,
  Votes int(10) DEFAULT NULL
)DEFAULT CHARSET=utf8;



-- -----------------------------------------------------
-- Table mydb.Ingredients
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Ingredients 
(
  IngredientName VARCHAR(100) NULL ,
  AltID INT(10) ZEROFILL NULL ,
  IngredientID INT(10) NOT NULL ,
  Basic ENUM('1','0') DEFAULT '0',
  Trivial ENUM('1','0') DEFAULT '0',
  PRIMARY KEY (IngredientID) 
)DEFAULT CHARSET=utf8;


ALTER TABLE Pictures
	ADD FOREIGN KEY (CocktailID) REFERENCES Cocktails(CocktailID)
    ON DELETE CASCADE
    ON UPDATE NO ACTION;

ALTER TABLE Recipes
	ADD FOREIGN KEY (CocktailID) REFERENCES Cocktails (CocktailID)
		ON DELETE CASCADE
		ON UPDATE CASCADE;

ALTER TABLE Comments
	ADD FOREIGN KEY (CocktailID) REFERENCES Cocktails (CocktailID)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION;

ALTER TABLE Comments
	ADD FOREIGN KEY (CocktailID) REFERENCES Cocktails (CocktailID)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION;
