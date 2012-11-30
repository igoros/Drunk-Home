-- -----------------------------------------------------
-- Table mydb.Cocktails
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Cocktails
(
  CocktailID INT(10),
  CocktailName VARCHAR(100) NOT NULL ,
  PRIMARY KEY (CocktailID)
);

-- -----------------------------------------------------
-- Table mydb.Pictures
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Pictures
(
  CocktailID INT(10),
  PicturePath VARCHAR(100) NOT NULL DEFAULT 'blank pic path here' ,
  PRIMARY KEY (CocktailID)
);


-- -----------------------------------------------------
-- Table mydb.Recipes
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Recipes (
  CocktailID INT(10),
  PRIMARY KEY (CocktailID),
  IngredientIDs VARCHAR(1000) NOT NULL ,
  RecipeText VARCHAR(10000) NULL

);



-- -----------------------------------------------------
-- Table mydb.Comments
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Comments 
(
  CocktailID INT(10),
  Rating FLOAT(4) NULL ,
  CommentText VARCHAR(100) NULL
);



-- -----------------------------------------------------
-- Table mydb.Ingredients
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS Ingredients 
(
  IngredientName VARCHAR(100) NULL ,
  AltID INT(10) ZEROFILL NULL ,
  IngredientID INT(10) NOT NULL ,
  PRIMARY KEY (IngredientID) 
);


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

