#!/usr/bin/perl
print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use Encode;
use URI::Escape;

use Data::Dumper;
use updates qw( updAdminPage updSearchByIng );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
#print Dumper $FormData;

my $list = { 'cocktailName'=>'',
	     'rank'=>'',
	     'comment'=>''
	   };
&form2data($FormData,$list);
my ($cocktailName,$dest,$fieldName,$isMobile,$destParams);
if($FormData =~ /ING/)
{
	($cocktailName,$dest,$destParams) = split(/##/,$list->{cocktailName});
}
else
{
	($cocktailName,$dest,$fieldName,$isMobile) = split(/##/,$list->{cocktailName});
#	print "$cocktailName,$dest,$fieldName,$isMobile";
}
#       print "$cocktailName,$dest,$fieldName,$isMobile";

#exit;
#print "$cocktailName......$dest.....$destParams\n";
#print Dumper $list;
#exit;
my $cockIDQuery= "SELECT CocktailID FROM Cocktails WHERE CocktailName='$cocktailName'";
my $cockIDHandler = &sqlQueryHandler($cockIDQuery,"YES");
my $cockID = $cockIDHandler->fetchrow();

if ($list->{rank})
{
	my $isRankedQuery = "SELECT COUNT(*) FROM Rating WHERE CocktailID=$cockID";
	my $isRankedHandler = &sqlQueryHandler($isRankedQuery,"YES");
	my $isRanked = $isRankedHandler->fetchrow();
	my $newRating;
	my $voters;
	
	if($isRanked == 0)
	{
		$newRating = $list->{rank};
		$voters = 1;
	        my $newRatingQuery = "INSERT INTO Rating (CocktailID,CurrentRating,Votes) VALUES ('$cockID','$newRating','$voters')";
	        my $newRatingHandler = &sqlQueryHandler($newRatingQuery, "NO");

	}	
	else
	{
		my $oldParamsQuery = "SELECT CurrentRating,Votes FROM Rating WHERE CocktailID=$cockID";
		my $oldParamsHandler = &sqlQueryHandler($oldParamsQuery,"YES");
		my ($oldRating,$oldNumOfVotes) = $oldParamsHandler->fetchrow();
		$newRating = ($oldRating*$oldNumOfVotes+$list->{rank})/($oldNumOfVotes+1);
		$voters = $oldNumOfVotes+1;	
	}
        my $newRatingQuery = "UPDATE Rating SET CurrentRating='$newRating', Votes='$voters' WHERE CocktailID=$cockID";
        my $newRatingHandler = &sqlQueryHandler($newRatingQuery, "NO");
}
if ($list->{comment})
{
	my $comment = Encode::decode('utf8',uri_unescape($list->{comment}));	
	$comment =~ s/'/''/g;
	my $commentQuery = "INSERT INTO Comments (CocktailID,Text) VALUES ('$cockID','$comment')";
	my $commentHandler = &sqlQueryHandler($commentQuery,"NO");
}

if ($dest eq "ING")
{	my $script = "recipeByIng.cgi";
	my @my_args;
	push(@my_args, "param=$destParams");
	local @ARGV = @my_args;
#	print "./recipeByIng.cgi param=$destParams";
	do "recipeByIng.cgi";
}
else
{
	my $script = "recipeByName.cgi";
	my $parameters= "$fieldName"."="."$cocktailName"."&"."$isMobile";
        my @my_args;
        push(@my_args, $parameters);
        local @ARGV = @my_args;
#       print "./recipeByIng.cgi param=$destParams";
        do "recipeByName.cgi";
}
#print "added successfully";









