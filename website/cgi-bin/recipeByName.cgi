#!/usr/bin/perl
#print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use dh_utils qw( form2data updatePage sqlQueryHandler getRatingPic getComments );
#print "in second script";
#my $FormData = "myCocktailSearch=B-28";
# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;
if(!$FormData)
{
	$FormData =  shift;
 #       print Dumper $FormData;
}
else
{
	print "Content-type:text/html\n\n";
}

my $list={'myCocktailSearch'=>"",
	  'cocktailList'=>""
	 };

&form2data($FormData,$list);

#print Dumper $list;
#exit;
my $cockName;
my $mobileFlag;
if($FormData =~ /wvsubmit/)
{
	$mobileFlag = 0;
	$cockName = $list->{myCocktailSearch};
}
else
{	
	$mobileFlag=1;
	$cockName = $list->{cocktailList};
}
##getting the ID of the cocktail

my $getCockID = "SELECT CocktailID FROM Cocktails WHERE CocktailName='$cockName'";
my $cockID;
my $idHandler = &sqlQueryHandler($getCockID, "YES");
$idHandler->bind_columns(undef, \$cockID);
$idHandler->fetch();

##checking if the cocktail exists
if(!($cockID))
{		
	if($mobileFlag)
	{
		system ("cat ../search_by_name-mobile.html");
        	print ("<h2 style=\"color:red\">Please choose a cocktail before submitting</h2>");
        	exit;
	}
	else
	{
		system ("cat ../search_by_name.html");
		print ("<h2 style=\"color:red\">Cocktail does not exist! Choose one from the list!</h2>");
		exit;
	}
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
my ($parts,$ing);
my $ingString="<br>Ingredients:<br>\n";
foreach my $ingAndParts (@ings)
{	($ing,$parts) = split ('#',$ingAndParts);
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
		if ($parts !=0)
		{
			$ingString .= "$parts "."parts of "."$mainIngName";
		}
		else
		{
			$ingString .= "$mainIngName";
		}

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
if($picPath =~/^$/)
{
	$picPath = "no_pic.gif";
}

##get rating

my $rating = &getRatingPic($cockID);

## get comments

my $commentsString = &getComments($cockID);	
##generating the recipe

my $timestamp = time();
my $randomNum = int(rand(9999999)+1);
my $newfile = "recipe$timestamp$randomNum";

$recipeText =~ s/(.*)/Recipe:<br>\n$1/;
&updatePage("recipe_template.txt",$newfile,$cockName,"COCKNAME");

&updatePage($newfile,$newfile,$ingString,"INGREDIENTS");

if($mobileFlag)
{
	$backURL = "<a href=\""."../search_by_name-mobile.html"."\">Back</a>";
}
else
{
	$backURL = "<a href=\""."../search_by_name.html"."\">Back</a>";
}

&updatePage($newfile,$newfile,$backURL,"BACK_URL");

&updatePage($newfile,$newfile,$recipeText,"RECIPE");

&updatePage($newfile,$newfile,$picPath,"COCKPIC");

&updatePage($newfile,$newfile,$rating,"RATING");

&updatePage($newfile,$newfile,$commentsString,"COMMENTS");

if($mobileFlag)
{
	&updatePage($newfile,$newfile,"NAME##"."cocktailList##mobilesubmit","RECPARAMS");
}
else
{
	 &updatePage($newfile,$newfile,"NAME##"."myCocktailSearch##wvsubmit","RECPARAMS");
}
system ("cat $newfile");

system ("rm $newfile");


1;
