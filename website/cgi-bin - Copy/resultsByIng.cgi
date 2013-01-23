#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use updates qw( updAdminPage );
use dh_utils qw( form2data updatePage sqlQueryHandler );
my $debug = 0;
# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;

#my $FormData = "ing=37&ing=6&ing=14&ing=9&ing=1&ing=3&ing=10&ing=11";
my @userIngs;
while ($FormData =~ /ing=(\d+)/)
{
	$FormData = $';
	push (@userIngs, $1);
}
	
my $query = "SELECT * FROM Recipes";
my $queryHandler = &sqlQueryHandler($query, "YES");

my ($cockID,$ingsIds,$recipe);

my $altQuery;
my @userMainIngs;
my $altID;
my $altHandler;
my $userIngsString = "";
foreach my $userIng (@userIngs)##get the main ingredient ID and create an array of no altID ingredients
{	
	$altQuery = "SELECT altID FROM Ingredients WHERE IngredientID='$userIng'";
	$altHandler = &sqlQueryHandler($altQuery, "YES");
	if ( $altID = $altHandler->fetchrow())
	{
		if ($altID != 0)
		{
			push (@userMainIngs, "$altID:$userIng");
			$userIngsString .= "$altID:$userIng-";
		}
	}
	else
	{	
		push (@userMainIngs, $userIng);
		$userIngsString .= "$userIng-";
	}
}

my @validatedCocks;
my $cockMainIng;
my $userMainIng;
my $mainFlag;
while(($cockID,$ingsIds,$recipe) = $queryHandler->fetchrow())
{	$mainFlag = 1;
	if($debug){print STDERR "checking ID $cockID where ingredient string is $ingsIds\n"};
	my @cockIngs = split (';',$ingsIds);	
	foreach my $cockIng (@cockIngs)
	{	
		
		if ($cockIng =~ /(.*?):.*/)
		{
			$cockMainIng = $1;
		}
		else
		{
			$cockMainIng = $cockIng;
		}
		if($debug){print STDERR "comparing ingredient $cockMainIng:\n";}
		my $subFlag=0;
		foreach my $userIng (@userMainIngs)
		{		
			
			if($userIng =~ /(.*?):.*/)
			{
				$userMainIng = $1;
			}
			else
			{
				$userMainIng = $userIng;
			}
			if($debug){print STDERR "checking user ing $userMainIng\n";}
			if ($userMainIng == $cockMainIng)
			{
				if($debug){print STDERR "found!!! (in if where subflag is set to 1)\n";}
				$subFlag = 1;	
				last;
			}
		}
		if ($subFlag == 0)
		{ 
			if($debug){print STDERR "the ingredient wasn't found , setting mainflag to 0\n";}
			$mainFlag =0;
			last;
		}
	}
	if ($mainFlag ==1)
	{
		if($debug){print "after entire cocktail check. added cocktail $cockID\n";}
		push (@validatedCocks, $cockID);
	}
}

##CREATE RESULTS PAGE

my $picPath;
my $picQuery;
my $picHandler;
my $cockName;
my $cockNameQuery;
my $cockNameHandler;
my $cocktailsList = "";

my $timestamp = time();
my $random_num = int(rand(9999999)+1);
my $temp_html = "../results/results$timestamp$random_num.html";

foreach my $val_cock (@validatedCocks)
{	
	if ((!$val_cock)){last;}
	$picQuery = "SELECT PicturePath FROM Pictures WHERE CocktailID=$val_cock";
	if($debug){print STDERR "path query = $picQuery\n";}
	$picHandler = &sqlQueryHandler($picQuery, "YES");
	$picPath = $picHandler->fetchrow();
	$cockNameQuery = "SELECT CocktailName FROM Cocktails WHERE CocktailID=$val_cock";
	if($debug){print STDERR "name= $cockNameQuery\n";}
	$cockNameHandler = &sqlQueryHandler($cockNameQuery, "YES");
	$cockName= $cockNameHandler->fetchrow();
	my $recipeParams = "param="."$val_cock"."--"."$userIngsString"."-"."$temp_html";
	my $cockPattern="<table class=\"bord\">
                        <tr>
                        <td rowspan=\"2\" >
                        <img src=\"../pic/PICPATH\" alt=\"search by ing\" class=\"picture\"/>
                        </td >
                        <td colspan=\"2\" >
                        Name:<a href=\"recipeByIng.cgi?RECIPE_PARAM\">COCKNAME</a>
                        </td>
                        </tr>
                        <tr>
                        <td>
                        Rank:
                        </td>
                        <td>
                        <img src=\"../pic/rating_4_5.gif\" alt=\"rating pic\" class=\"reatingPic\">
                        </td>
                        </tr>
                </table>";
	$cockPattern =~ s/PICPATH/$picPath/;
	$cockPattern =~ s/COCKNAME/$cockName/;
	$cockPattern =~ s/RECIPE_PARAM/$recipeParams/;
	$cocktailsList .= "$cockPattern\n";
}	
#my $timestamp = time();
#my $random_num = int(rand(9999999)+1);
#my $temp_html = "results/results$timestamp$random_num";


&updatePage("results_template.txt", $temp_html, $cocktailsList, "COCKTAILSLIST");

system ("cat $temp_html");





1;
