#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use dh_utils qw( form2data updatePage sqlQueryHandler );

use CGI;
my $cgi = CGI->new();
my $param = $cgi->param('param');

print Dumper $param;

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
print Dumper $FormData;
exit;

my $list={'myCocktailSearch'=>""};

&form2data($FormData,$list);

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
my $getIng;
my $ingHandler;
my $ingName;
my $ingString="<br>Ingredients:<br>\n";
foreach my $ing (@ings)
{
	if($ing)
	{
		$getIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$ing";
		$ingHandler = &sqlQueryHandler($getIng, "YES");
		$ingHandler->bind_columns(undef, \$ingName);
		$ingHandler->fetch();
		$ingString .= "$ingName<br>\n";
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
