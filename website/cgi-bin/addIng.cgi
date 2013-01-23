#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use updates qw( updAdminPage updSearchByIng );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;
#exit;

#my $FormData = "ingName=Whiskey&altName=&category=Spirits&ingsubmit=submit";

my $list={'ingName'=>"",
	  'category'=>"",
	  'altName'=>"",
	  'basic'=>"",
	  'trivial'=>""
	};

&form2data($FormData,$list);

if ($list->{trivial} && $list->{basic})
{
	print "<p style=\"color:red\">An ingredient can't be both trivial and basic - think about it...(we added trivial for a reason)</p>";
	exit;
}

my $trivial;

if($list->{trivial})
{
        $trivial = "1";
}
else
{
        $trivial = "0";
}



my $query;
#CHECK IF INGREDIENT ALREADY EXISTS
my $checkVal;
my $checkIfExist = "SELECT COUNT(*) FROM Ingredients WHERE IngredientName='$list->{ingName}'";
my $checkReturn = &sqlQueryHandler($checkIfExist, "YES");
$checkReturn->bind_columns(undef, \$checkVal);
$checkReturn->fetch();
my $response;
my $basic;
if($list->{basic})
{
	$basic = "1";
}
else
{
	$basic = "0";
}

if($checkVal)
{
	$response = "The ingredient you entered already exists.";
}
elsif ($list->{altName} =~ /\w+/)# IN CASE OF AN ALTERNATIVE NAME
{	my $altID;	#will carry the altID value
	my $altQuery = "SELECT IngredientID FROM Ingredients WHERE IngredientName='$list->{altName}'"; #query for getting the altID using the altName
	my $altReturn = &sqlQueryHandler($altQuery,"YES");#execute the query 
	$altReturn->bind_columns(undef, \$altID);
	$altReturn->fetch();#set the altID into $altID
	if($altID != 0)
	{
        	$query = "INSERT INTO Ingredients (IngredientName, AltID, Category, Basic, Trivial) VALUES ('$list->{ingName}','$altID','$list->{category}','$basic','$trivial')";
		$response = "The ingredient was added successfully!";
		&sqlQueryHandler($query,"YES");
	}
	else
	{
		$response = "The alternative name doesn't exist! please choose one from the list!\n";
	}
}
else  #NO ALT ID
{
$query = "INSERT INTO Ingredients (IngredientName, Category, Basic, Trivial) VALUES ('$list->{ingName}','$list->{category}','$basic','$trivial')";#insert without altID
$response = "The ingredient was added successfully!";
&sqlQueryHandler($query,"NO");
}

##UPDATE ADMIN
&updAdminPage;

##UPDATE SEARCH BY INGREDIENT
&updSearchByIng;
print "<p style=\"color:red\">$response</p>\n";
##RETURN PAGE WITH INSERTION STATUS
#my $actionResult;
#system("cat ../admin_page.html");
#$resPattern= "<h3>";
#$actionresult =~ s/$resPattern/<h3>$response/;
#$actionResult =~ s/src=\"(.*?)\"/\.\.$1/g;


#print " suppose to be page:\n$actionResult";


1;
