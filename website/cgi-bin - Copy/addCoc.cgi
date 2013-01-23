#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use CGI;
use Data::Dumper;
use updates qw( updSrchByName );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;
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
	  'pic'=>""
	};


&form2data($FormData,$list);

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
#print STDERR "in start of else";
my $ingString="";
my ($ingID,$altID);
my $i;
for($i=1;$i<=8;$i++)
{	
	my $cur=$list->{"ing$i"};
	if($cur =~ /\w+/)
	{	
#		print SRDERR "in for loop $i\n";
		my $ingQuery="SELECT IngredientID,AltID FROM Ingredients WHERE IngredientName='$cur'";
		my $ingReturn = &sqlQueryHandler($ingQuery,"YES");#execute the query 
        	($ingID,$altID) = $ingReturn->fetchrow();
		if($altID){
			$ingString .= "$altID:$ingID;";
		}
		else{
			$ingString .= "$ingID;";
		}
	}

}
#print STDERR "after for\n ing string = $ingString\n";
my $addCocktail = "INSERT INTO Cocktails (CocktailName) VALUES ('$list->{CocktailName}')";
&sqlQueryHandler($addCocktail,"NO");
#print STDERR "after first insert\n";
my $theID;
my $getID = "SELECT CocktailID FROM Cocktails WHERE CocktailName='$list->{CocktailName}'";

my $IdReturn = &sqlQueryHandler($getID,"YES");#execute the query 
#print STDERR "after first select\n";
$IdReturn->bind_columns(undef, \$theID);
$IdReturn->fetch();

my $addRecipe = "INSERT INTO Recipes (CocktailID,IngredientIDs,RecipeText) VALUES ('$theID','$ingString','$list->{recipe}')";
&sqlQueryHandler($addRecipe,"NO");
#print STDERR "after second insert\n";
$response = "The cocktail was added successfully!";


my $addPic = "INSERT INTO Pictures (CocktailID,PicturePath) VALUES ('$theID','$list->{pic}')";
&sqlQueryHandler ($addPic, "NO");

}

&updSrchByName;
print "<p style=\"color:red\">$response</p>\n";

1;
