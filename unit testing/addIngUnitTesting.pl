#!/usr/bin/perl


my $counter = 1;
my $ing = shift;
my $status = shift;
print STDERR "======================\n";
do
{
	print STDERR "test $counter where ingredient is $ing:\n";
	system ("./addIngTest.pl $ing $status");
	print STDERR "\n======================\n";
	$ing = shift;
	$status = shift;
	$counter++;	
}while($ing);

1;
	
