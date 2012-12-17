#!/usr/bin/perl
#print "Content-type: text/html\n\n";


# Read the standard input (sent by the form):
#read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});

use Test::Simple tests=>4;

#test1
ok(&maain("ingName=Brandy") eq "Brandy...","Catching one Argument from Form\n");
#test2
ok(&maain("ingName=Brandy&altName=Cognac") eq "Brandy.Cognac..","Catching two Arguments from Form\n");
#test3
ok(&maain("ingName=Brandy&altName=Cognac&basic=on") eq "Brandy.Cognac.on.","Catching three Arguments from Form\n");
#test4
ok(&maain("ingName=Brandy&altName=Cognac&basic=on&category=alcoholic") eq "Brandy.Cognac.on.alcoholic","Catching four Arguments from Form\n");


sub maain($FormData)
{
my $list={'ingName'=>"",
	  'category'=>"",
	  'altName'=>"",
	  'basic'=>""
	};
my $FormData=shift;

&form2data($FormData,$list);


return "$list->{'ingName'}.$list->{'altName'}.$list->{'basic'}.$list->{'category'}";
}

sub form2data{

my $FormData = shift;
my $parsedForm = shift;
# Get the name and value for each form input:
@pairs = split(/&/, $FormData);

# Then for each name/value pair....
foreach $pair (@pairs) {

	# Separate the name and value:
	($name, $value) = split(/=/, $pair);

	# Convert + signs to spaces:
	$value =~ tr/+/ /;

	# Convert hex pairs (%HH) to ASCII characters:
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# Store values in a hash called %FORM:
	$parsedForm->{$name} = $value;
}
return $parsedForm;
}
1;


