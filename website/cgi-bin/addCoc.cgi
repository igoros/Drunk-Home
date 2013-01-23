#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use CGI;
use Data::Dumper;
###
use Encode;
use URI::Escape;

#my $in = "%C3%B3";
#my $text = Encode::decode('utf8', uri_unescape($in));
###

use updates qw( updSrchByName );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;

#my $decodedForm = Encode::decode('utf8',uri_unescape($FormData));
#print Dumper $decodedForm;
#exit;

#$FormData = $decodedForm;
#print Dumper $FormData;
#$FormData =~ s/'/''/g;
#my $testData = "pic=&CocktailName=dakiri&recipe=oonon&ing1=klnkln&ing2=lknln&ing3=&ing4=&ing5=&ing6=&ing7=&ing8=&cocktailsubmit=submit";
my $list={'CocktailName'=>"",
	  'recipe'=>"",
	  'ing1'=>"",
	  'ing2'=>"",
	  'ing3'=>"",
	  'ing4'=>"",
	  'ing5'=>"",
	  'ing6'=>"",
	  'ing7'=>"",
	  'ing8'=>"",
	  'pic'=>"",
	  'part1'=>"",
          'part2'=>"",
          'part3'=>"",
          'part4'=>"",
          'part5'=>"",
          'part6'=>"",
          'part7'=>"",
          'part8'=>""
	};


&form2data($FormData,$list);
#print "before decoding and swiching\n";
#exit;
my $tempRecipe = Encode::decode('utf8',uri_unescape($list->{recipe}));
$list->{recipe} = $tempRecipe;
$list->{recipe} =~ s/'/''/g;
#print "recipe = $list->{recipe}";
#exit;

my $query;
#CHECK IF Cocktail ALREADY EXISTS
my $checkVal;
my $checkIfExist = "SELECT COUNT(*) FROM Cocktails WHERE CocktailName='$list->{CocktailName}'";
my $checkReturn = &sqlQueryHandler($checkIfExist, "YES");
$checkReturn->bind_columns(undef, \$checkVal);
$checkReturn->fetch();
my $response;
#print STDERR "before if";
if($checkVal)
{
	$response = "The Cocktail you entered already exists.";
}
else{
#print  "in start of else";
my $ingString="";
my ($ingID,$altID);
my $i;
for($i=1;$i<=8;$i++)
{	
	my $cur=$list->{"ing$i"};
	my $parts=$list->{"part$i"};
	#print "parts$i = $parts\n";
	
	if (($cur) && ($parts eq ""))
	{
		print "<p style=\"color:red\">You haven't filled the parts for $cur! enter the parts and re-submit.</p>";
		exit;
	}
 	
	if (!($cur) && ($parts))
	{
		print "<p style=\"color:red\">You filled one of the parts fields but didn't entered an ingredient for it! check your entry!</p>";
		exit;	
	}
	
	if($cur =~ /\w+/)
	{	
		if (!($parts =~ /^[0-9\.]+$/))
        	{
               		print "<p style=\"color:red\">The parts value MUST be a number! check you entry!</p>";
        	        exit;
	        }
		#print "in for loop $i\n";
		my $ingQuery="SELECT IngredientID,AltID FROM Ingredients WHERE IngredientName='$cur'";
		my $ingReturn = &sqlQueryHandler($ingQuery,"YES");#execute the query 
        	($ingID,$altID) = $ingReturn->fetchrow();
		if($altID){
			$ingString .= "$altID:$ingID#$parts;";
		}
		else{
			$ingString .= "$ingID#$parts;";
		}
	}

}
#print STDERR "after for\n ing string = $ingString\n";
my $addCocktail = "INSERT INTO Cocktails (CocktailName) VALUES ('$list->{CocktailName}')";
&sqlQueryHandler($addCocktail,"NO");
#print "after first insert\n";
my $theID;
my $getID = "SELECT CocktailID FROM Cocktails WHERE CocktailName='$list->{CocktailName}'";

my $IdReturn = &sqlQueryHandler($getID,"YES");#execute the query 
#print STDERR "after first select\n";
$IdReturn->bind_columns(undef, \$theID);
$IdReturn->fetch();
my $addRecipe = "INSERT INTO Recipes (CocktailID,IngredientIDs,RecipeText) VALUES ('$theID','$ingString','$list->{recipe}')";
#print Dumper $addRecipe;
#exit
&sqlQueryHandler($addRecipe,"NO");
#print STDERR "after second insert\n";
$response = "The cocktail was added successfully!";


my $addPic = "INSERT INTO Pictures (CocktailID,PicturePath) VALUES ('$theID','$list->{pic}')";
&sqlQueryHandler ($addPic, "NO");

}

&updSrchByName;
print "<p style=\"color:red\">$response</p>\n";

1;
