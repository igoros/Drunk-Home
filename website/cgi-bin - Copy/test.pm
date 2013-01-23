#!/usr/bin/perl

# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use dh_utils qw( updatePage sqlQueryHandler );
use updates qw( updAdminPage updSrchByName updSearchByIng );
use Data::Dumper;


my $results = &updSearchByIng;
print "$results";
