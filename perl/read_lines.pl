#!/usr/bin/env perl
#------------------------------------------------------
# Example program for Martin Depner.
# Read lines from a text file. Count how many times
# the string "Martin" appears in the file.
#
# See read_lines.py for the Python counterpart.
#------------------------------------------------------

my $file_name = "martin1.in";
my $str = "Martin";

my $count = 0;
open(MYINPUTFILE, "<$file_name");
while (<MYINPUTFILE>)
 {
     my($line) = $_;
     chomp($line);
     if ($line eq $str)
     {
	 $count = $count + 1;
     }
 }

print "Number of times $str appears = $count\n";
