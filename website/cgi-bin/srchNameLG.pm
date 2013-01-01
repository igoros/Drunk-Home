#!/usr/bin/perl

# PERL MODULES WE WILL BE USING
use DBI;
use DBD::mysql;
use dh_utils qw( updatePage );

# HTTP HEADER 
print "Content-type: text/html \n\n";

# CONFIG VARIABLES
my $platform = "mysql";
my $database = "drunkathome";
my $host = "10.100.102.5";
my $port = "3306";
my $tablename = "Cocktails";
my $user = "mosh";
my $pw = "111";

# DATA SOURCE NAME
my $dsn = "dbi:$platform:$database:$host:$port";

# PERL DBI CONNECT
my $connect = DBI->connect($dsn, $user, $pw);

# PREPARE THE QUERY
my $query = "SELECT CocktailName FROM $tablename";
$query_handle = $connect->prepare($query);



# EXECUTE THE QUERY
$query_handle->execute();

# BIND TABLE COLUMNS TO VARIABLES
$query_handle->bind_columns(undef, \$CocktailName);

# LOOP THROUGH RESULTS AND CREATE A LIST FOR THE SEARCH BY NAME LIST
my $params="<datalist id=\"cocktailList\">\n";

while ($query_handle->fetch())
{
        $params.="<option value=\"$CocktailName\">\n";
}

$params.="</datalist>\n";
# SWITCH THE OLD LIST WITH THE UPDATED LIST

my $template = "search_by_name.txt";
my $fileName = "../search_by_name.html";
my $pattern = "<datalist id=\"cocktailList\">";

&updatePage($template,$fileName,$params,$pattern);

1;
