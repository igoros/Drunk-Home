#!/usr/bin/perl
#print "Content-type:text/html\n\n";
# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;

use Data::Dumper;
use updates qw( updAdminPage updSearchByIng );
use dh_utils qw( form2data updatePage sqlQueryHandler );

# Read the standard input (sent by the form):
read(STDIN, $FormData, $ENV{'CONTENT_LENGTH'});
print Dumper $FormData;
exit;


