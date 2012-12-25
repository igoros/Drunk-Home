#!/usr/bin/perl
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use updates qw( updAdminPage );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
my $FormData = shift;
#print Dumper $FormData;
my $list={'ingName'=>"",
	  'category'=>"",
	  'altName'=>""
	};

&form2data($FormData,$list);

my $query;
#CHECK IF INGREDIENT ALREADY EXISTS
my $checkVal;
my $checkIfExist = "SELECT COUNT(*) FROM Ingredients WHERE IngredientName='$list->{ingName}'";
my $checkReturn = &sqlQueryHandler($checkIfExist, "YES");
$checkReturn->bind_columns(undef, \$checkVal);
$checkReturn->fetch();
my $response;
if($checkVal == 1)
{
	$response = "The ingredient you entered already exists.";
}
elsif ($list->{altName} =~ /\w+/)# IN CASE OF AN ALTERNATIVE NAME
{	my $altID;	#will carry the altID value
	my $altQuery = "SELECT IngredientID FROM Ingredients WHERE IngredientName='$list->{altName}'"; #query for getting the altID using the altName
	my $altReturn = &sqlQueryHandler($altQuery,"YES");#execute the query 
	$altReturn->bind_columns(undef, \$altID);
	$altReturn->fetch();#set the altID into $altID
        $query = "INSERT INTO Ingredients (IngredientName,AltID, Category) VALUES ('$list->{ingName}','$altID','$list->{category}')";
	$response = "The ingredient was added successfully!";
	&sqlQueryHandler($query,"NO");
}
else  #NO ALT ID
{
$query = "INSERT INTO Ingredients (IngredientName, Category) VALUES ('$list->{ingName}','$list->{category}')";#insert without altID
$response = "The ingredient was added successfully!";
&sqlQueryHandler($query,"NO");
}

##UPDATE ADMIN
#&updAdminPage;
#print "$response\n";
##RETURN PAGE WITH INSERTION STATUS
#my $actionResult;
#system("cat ../admin_page.html");
#$resPattern= "<h3>";
#$actionresult =~ s/$resPattern/<h3>$response/;
#$actionResult =~ s/src=\"(.*?)\"/\.\.$1/g;


#print " suppose to be page:\n$actionResult";


1;
