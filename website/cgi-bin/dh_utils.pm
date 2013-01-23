#!/usr/bin/perl
use Data::Dumper;
use DBI;
use DBD::mysql;
package dh_utils;

require Exporter;

our @ISA= qw( Exporter );
our @EXPORT_OK= qw( updatePage form2data sqlQueryHandler getRatingPic getComments );
our @EXPORT= qw( updatePage form2data sqlQueryHandler getRatingPic getComments);

sub updatePage{
   my $template;
   my $fileName;
   my $replacement;
   my $pattern;

   my $oldFileContent="";

   ($template,$fileName,$replacement,$pattern) = @_;
  
   open(DATA, "<$template");

   while(<DATA>){
   	$oldFileContent.="$_";
   }
   close(DATA);

   $oldFileContent =~ s/$pattern/$replacement/g;

   open(DATA,">$fileName");
   print DATA "$oldFileContent";
   close(DATA);
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


sub sqlQueryHandler{

# CONFIG VARIABLES
my $platform = "mysql";
my $database = "drunkathome";
my $host = "10.100.102.5";
my $port = "3306";
my $user = "mosh";
my $pw = "111";
my ($query,$feedback) = @_;
# DATA SOURCE NAME
my $dsn = "dbi:$platform:$database:$host:$port";

# PERL DBI CONNECT
my $connect = DBI->connect($dsn, $user, $pw);
# PREPARE THE QUERY
#my $query = "$query";
print STDERR "query=$query\n";
$query_handle = $connect->prepare($query);
# EXECUTE THE QUERY
$query_handle->execute();
# BIND TABLE COLUMNS TO VARIABLES
#$query_handle->bind_columns(undef, $columnString);

if($feedback =~ /YES/)
{
return $query_handle;
}
}

sub getRatingPic{
	
	my $cockID = shift;
	
	my $isRatedQuery = "SELECT COUNT(*) FROM Rating WHERE CocktailID=$cockID";
	my $isRatedHandler = &sqlQueryHandler($isRatedQuery,"YES");
	my $ratedCount = $isRatedHandler->fetchrow();

	if($ratedCount == 0)
	{
         	return "rating_2_5.gif";
	}

        my $currRating;
        my $ratingQuery = "SELECT CurrentRating from Rating WHERE CocktailID=$cockID";
        my $ratingHandler = &sqlQueryHandler($ratingQuery, "YES");
        $currRating= $ratingHandler->fetchrow(); 
	if($currRating < 0.25)
	{
		return "rating_0.gif";
	}
	elsif($currRating < 0.75)
	{
		return "rating_0_5.gif";
	}
	elsif($currRating <1.25)
	{
		return "rating_1.gif";
	}
	elsif($currRating < 1.75)
	{
		return "rating_1_5.gif";
	}
	elsif($currRating < 2.25)
	{
		return "rating_2.gif";
	}
	elsif($currRating < 2.75)
	{
		return "rating_2_5.gif";
	}
	elsif($currRating < 3.25)
	{
		return "rating_3.gif";
	}
	elsif($currRating <3.75)
	{
		return "rating_3_5.gif";
	}
	elsif($currRating < 4.25)
	{
		return "rating_4.gif";
	}
	elsif($currRating < 4.75)
	{
		return "rating_4_5.gif";
	}
	else
	{
		return "rating_5.gif";
	}

}


sub getComments{

	my $commentsString = "";
	my $comment;
	my $cockID = shift;
	my $commentsQuery = "SELECT Text from Comments WHERE CocktailID=$cockID";
	my $commentsHandler = &sqlQueryHandler($commentsQuery, "YES");
	
	while($comment = $commentsHandler->fetchrow())
	{
		$commentsString .="     <tr colspan=\"2\" border=\"1\">
        				 	<td>
	        				<div class=\"myBorder\">
        					Comment:<br>
  					      	$comment
        					</div>
 					       </td>
        				</tr>"
	}

	return $commentsString;
}










	

















1;
