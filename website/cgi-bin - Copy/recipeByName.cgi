#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use dh_utils qw( form2data updatePage sqlQueryHandler );

#my $FormData = "myCocktailSearch=B-28";
# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;

my $list={'myCocktailSearch'=>""};

&form2data($FormData,$list);

#print Dumper $list;

##getting the ID of the cocktail

my $getCockID = "SELECT CocktailID FROM Cocktails WHERE CocktailName='$list->{myCocktailSearch}'";
my $cockID;
my $idHandler = &sqlQueryHandler($getCockID, "YES");
$idHandler->bind_columns(undef, \$cockID);
$idHandler->fetch();

##checking if the cocktail exists
if(!($cockID))
{
	system ("cat ../search_by_name.html");
	print ("<h2 style=\"color:red\">Cocktail does not exist! Choose one from the list!</h2>");
	exit;
}
##getting the data of the recipe

my $getRecipe = "SELECT IngredientIDs,RecipeText FROM Recipes WHERE CocktailID='$cockID'";
my $recipeHandler = &sqlQueryHandler($getRecipe, "YES");
my ($ingsIDs,$recipeText)=$recipeHandler->fetchrow();

##splitting the ingredients into array and preparing the string for the replacement
my @ings = split (';', $ingsIDs);
my $getMainIng;
my $getRecIng;
my $mainIngHandler;
my $recIngHandler;
my $mainIngName;
my $recIngName;
my ($mainIngID,$recIngID);
my $ingString="<br>Ingredients:<br>\n";
foreach my $ing (@ings)
{
	if($ing)
	{
		if ($ing =~ /(.*?):(.*)/)
		{
			($mainIngID,$recIngID) = ($1,$2);
		}
		else
		{
			$mainIngID = $ing;
		}
		print STDERR "Before getting the main ingredient name. mainID=$mainIngID, ing of foreach=$ing\n";
		$getMainIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$mainIngID";
		$mainIngHandler = &sqlQueryHandler($getMainIng, "YES");
		$mainIngHandler->bind_columns(undef, \$mainIngName);
		$mainIngHandler->fetch();
		$ingString .= "$mainIngName";

		if ($recIngID)
		{
			$getRecIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$recIngID";
			$recIngHandler = &sqlQueryHandler($getRecIng, "YES");
			$recIngHandler->bind_columns(undef, \$recIngName);
			$recIngHandler->fetch();
			$ingString .= "(Recommended: $recIngName)</br>\n";
		}
		else
		{
			$ingString .= "</br>\n";
		}
		$mainIngName = "";
		$recIngName = "";
		$recIngID = 0;
		$mainIngID = 0;
	}
}

$ingString .= "<br>\n";

##getting the picture of the cocktail
my $getPic = "SELECT PicturePath FROM Pictures WHERE CocktailID=$cockID";
my $picHandler = &sqlQueryHandler($getPic, "YES");
my $picPath;
$picHandler->bind_columns(undef,\$picPath);
$picHandler->fetch();

##generating the recipe

my $timestamp = time();
my $randomNum = int(rand(9999999)+1);
my $newfile = "recipe$timestamp$randomNum";

$recipeText =~ s/(.*)/Recipe:<br>\n$1/;
&updatePage("recipe_template.txt",$newfile,$list->{myCocktailSearch},"COCKNAME");

&updatePage($newfile,$newfile,$ingString,"INGREDIENTS");

&updatePage($newfile,$newfile,$recipeText,"RECIPE");

&updatePage($newfile,$newfile,$picPath,"COCKPIC");

system ("cat $newfile");

system ("rm $newfile");


1;
