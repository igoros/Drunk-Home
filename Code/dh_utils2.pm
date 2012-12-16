#!/usr/bin/perl

package dh_utils;
use strict;
use locale;

require Exporter;

our @ISA= qw( Exporter );
our @EXPORT_OK= qw( updatePage );
our @EXPORT= qw( updatePage );

sub updatePage{

   my $fileName;
   my $replacement;
   my $pattern;
   my $oldFileContent="";

   ($fileName,$replacement,$pattern) = @_;

   open(DATA, "<$fileName");

   while(<DATA>){
   	$oldFileContent.="$_";
   }
   close(DATA);

   $oldFileContent =~ s/$pattern/$replacement/;

   open(DATA,">$fileName");

   print DATA "$oldFileContent";
   close(DATA);
}

1;
