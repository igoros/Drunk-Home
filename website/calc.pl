#!/usr/bin/perl -w

use strict;
use CGI qw/:standard/;

# Declare and initialize variables.
my $num1 = 0;
my $num2 = 0;
my $result = 0;
my $operation = "";
my $output = "";
my @input_form = ();
my $output_html = "";

# Get input from "param" via CGI.pm.
$num1 = param("num1");
$num2 = param("num2");
$operation = param("operation");

# Act on supplied input.
if ($operation eq "a") { $result = $num1 + $num2; }
if ($operation eq "s") { $result = $num1 - $num2; }
if ($operation eq "m") { $result = $num1 * $num2; }
if ($operation eq "d")
{
    if ($num2 == 0)
    {
        $result = "Cannot divide by zero.";
    }
    else { $result = $num1 / $num2; }
}

# Read in the HTML template file.
open (HTMLFILE, "<input_form.dat");
@input_form = <HTMLFILE>;
close HTMLFILE;
foreach (@input_form)
{
    $output_html .= $_;
}

# Insert result in HTML template.
$output_html =~ s/\$RESULT/$result/g;

# Send HTML to the browser.
print "Content-type:text/html\n\n";
print $output_html;