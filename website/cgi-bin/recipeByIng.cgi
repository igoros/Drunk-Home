#!/usr/bin/perl
#print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use dh_utils qw( form2data updatePage sqlQueryHandler getRatingPic getComments );
#print "got to second script";
use CGI;
my $cgi = CGI->new();
my $param = $cgi->param('param');
if(!$param)
{
	my $data =  shift;
	#print Dumper $data;
	if($data =~ /param=(.*)/)
	{
		$param = $1;
	}
}
else
{
	print "Content-type:text/html\n\n";
}
#print "input $userinput";
#print Dumper $param;
#exit;
#my $param = "33--9:53-4:16-14";
my ($cockID,$userIngs,$backURL) = split ('--',$param);

my @userIngsArray = split ('-',$userIngs);

#print "<a href=\"$backURL\">Back to results</a>\n";

##getting the data of the recipe

my $getRecipe = "SELECT IngredientIDs,RecipeText FROM Recipes WHERE CocktailID='$cockID'";
my $recipeHandler = &sqlQueryHandler($getRecipe, "YES");
my ($ingsIDs,$recipeText)=$recipeHandler->fetchrow();

##splitting the ingredients into array and preparing the string for the replacement
my @ings = split (';', $ingsIDs);
my $getMainIng;
my $getRecIng;
my $getOptIng;
my $mainIngHandler;
my $recIngHandler;
my $optIngHandler;
my $mainIngName;
my $recIngName;
my $optIngName;
my $mainIngID;
my $recIngID;
my $optIngID;
my ($ing,$parts);
my $ingString="<br>Ingredients:<br>\n";
foreach my $ingAndParts (@ings)
{
	($ing,$parts) = split ('#',$ingAndParts);
	if($ing)
	{
		if($ing =~ /(.*?):(.*)/)
		{	
			$mainIngID = $1;
			$recIngID = $2;
			$getRecIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$recIngID";
			$recIngHandler = &sqlQueryHandler ($getRecIng, "YES");
			$recIngHandler->bind_columns(undef, \$recIngName);
			$recIngHandler->fetch();
			 print STDERR "print of getting RecID, recName is: $recIngName\n";

		}
		else
		{
			$mainIngID = $ing;
		}
		
		foreach my $userIng (@userIngsArray)
		{
			print STDERR "inside foreach of getting the optional. user ing is $userIng\n;";
			if($userIng =~ /(.*?):(.*)/)
			{
				$userMainIng = $1;
				$optIngID = $2;
				print STDERR "before if of comparison. user main = $userMainIng ; cock main = $mainIngID\n";
				if($userMainIng == $mainIngID)
				{
					$getOptIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$optIngID";
					$optIngHandler = &sqlQueryHandler($getOptIng, "YES");
					$optIngHandler->bind_columns(undef,\$optIngName);
					$optIngHandler->fetch();
					print STDERR "print of getting optID, recName is: $optIngName\n";
					last;
				}
			}
		}
		
		$getMainIng = "SELECT IngredientName FROM Ingredients WHERE IngredientID=$mainIngID";
		$mainIngHandler = &sqlQueryHandler($getMainIng, "YES");
		$mainIngHandler->bind_columns(undef, \$mainIngName);
		$mainIngHandler->fetch();
		if($parts != 0)
		{
			$ingString .= "$parts"." parts of "."$mainIngName";
		}
		else
		{
			$ingString .= "$mainIngName";
		}

		if($recIngName && $optIngName)
		{
			if ($recIngName eq $optIngName)
			{
				$ingString .= " (Recommended: $recIngName)";
			}	
			else
			{
				$ingString .= " (Recommended: $recIngName , Optional:$optIngName)";
			}
		}
		elsif ($recIngName)
		{
			$ingString .= " (Recommended: $recIngName)";
		}
		elsif($optIngName)
		{
			$ingString .= " (Optional: $optIngName)";
		}
		$optIngName = "";
		$recIngName = "";
	}
	

$ingString .= "<br>\n";
}
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

##get comments

my $commentsString = &getComments($cockID);

##getting the name of the cocktail
my $cockName;
my $getCockName = "SELECT CocktailName FROM Cocktails WHERE CocktailID=$cockID";
my $cockNameHandler = &sqlQueryHandler($getCockName, "YES");
$cockNameHandler->bind_columns(undef, \$cockName);
$cockNameHandler->fetch();

##generating the recipe

my $timestamp = time();
my $randomNum = int(rand(9999999)+1);
my $newfile = "recipe$timestamp$randomNum";

$recipeText =~ s/(.*)/Recipe:<br>\n$1/;
&updatePage("recipe_template.txt",$newfile,$cockName,"COCKNAME");

&updatePage($newfile,$newfile,$ingString,"INGREDIENTS");

$backURL = "<a href=\""."$backURL"."\">Back to results</a>";
&updatePage($newfile,$newfile,$backURL,"BACK_URL");

&updatePage($newfile,$newfile,$recipeText,"RECIPE");

&updatePage($newfile,$newfile,$picPath,"COCKPIC");

&updatePage($newfile,$newfile,$rating,"RATING");

&updatePage($newfile,$newfile,$commentsString,"COMMENTS");

&updatePage($newfile,$newfile,"ING##"."$param","RECPARAMS");

#&updatePage($newfile,$newfile,$userIngs,"USERINGS");

system ("cat $newfile");

system ("rm $newfile");


1;
