#!/usr/bin/perl
print "Content-type: text/html\n\n";
print "Hello Wrold<br><br>";

my $i;
for($i=0; $i<10; $i++)
{
        print $i."<br>";
}

1;


