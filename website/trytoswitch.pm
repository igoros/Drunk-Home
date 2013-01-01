#!/usr/bin/perl

use strict;
use dh_utils qw( updatePage );
#require 'dh_util.pm';
my $string = "<content to replace>.*?</content to replace>";
my $rep = "<replcedby>\n<newdata1>\n<newdata2>\n<newdata3>\n</replacedby>";
&updatePage("testfile.html",$rep,$string);

