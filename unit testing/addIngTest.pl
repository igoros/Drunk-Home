#!/usr/bin/perl
#print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use warnings;
use Data::Dumper;
use updates qw( updAdminPage );
use dh_utils qw( form2data updatePage sqlQueryHandler );

my $data = shift;
my $status = shift;
#preparing the query  -  check if the ingredientis is already in the system
my $query = "SELECT count(*) FROM Ingredients WHERE IngredientName='$data'";

#sending the query

my $response = &sqlQueryHandler($query,"YES");
my $amount;
$response->bind_columns(undef,\$amount);
$response->fetch();

##on a case where the ingredient already exists
if ($amount == 1)
{	
	print STDERR "The ingredient is already in the system\n";
	if ($status == 1)
	{	
		print STDERR "Test OK\n";
	}
	else
	{
		print STDERR "unexpected result to test!\n";
	}
	exit;
}

##the ingredient wasn't part of the ingredient list:
#adding ingredient to database using the addIng script
system ("./addIng.cgi ingName=$data");

#preparing the query  -  check if the ingredient was entered
$query = "SELECT count(*) FROM Ingredients WHERE IngredientName='$data'";

#sending the query

my $amount2;
my $response2 = &sqlQueryHandler($query,"YES");
$response2->bind_columns(undef,\$amount2);
$response2->fetch();

if($amount2 == 1){
	print STDERR "the ingredient was enter successfully into the DB!\n";
	if ($status == 1)
	{
		print STDERR "unexpected result to test!\n";
	}
	else
	{
		print STDERR "Test OK!\n";
	}
	#delete the added drink
	$query = "DELETE FROM Ingredients WHERE IngredientName='$data'";
	&sqlQueryHandler($query,"NO");
	exit;
}
else{
		print STDERR "the ingredient wasn't entered into the database.\nunexpected result to test!\n";
}



1;
