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
   my $openingPattern;
   my $closingPattern;

   my $oldFileContent="";

   ($fileName,$replacement,$openingPattern,$closingPattern) = @_;
  
   open(DATA, "<$fileName");

   while(<DATA>){
   	$oldFileContent.="$_";
   }
   close(DATA);
   my $prefix;
   my $postfix;
   print STDERR "before substitute:$oldFileContent";
   if($oldFileContent =~ /(.*?)$openingPattern.*?$closingPattern(.*?)/){

	$prefix = $1;
	$postfix = $2;
	print STDERR "pre:$prefix\n post:$postfix";
	$oldFileContent = "$prefix$replacement$postfix";
   print STDERR "file content after manual change:\n$oldFileContent\n"; 
   }
   open(DATA,">$fileName");

   print STDERR "old file at the end: $oldFileContent\n";

   print DATA "$oldFileContent";
   close(DATA);
}

1;
