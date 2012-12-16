#!/usr/bin/perl
use Data::Dumper;
use DBI;
use DBD::mysql;
use dh_utils qw( updatePage sqlQueryHandler );

package updates;

require Exporter;
require dh_utils;
our @ISA= qw( Exporter );
our @EXPORT_OK= qw( updAdminPage updSrchByName );
our @EXPORT= qw( UpdAdminPage updSrchByName);

sub updAdminPage{
	##update ingredients for "add a cocktail"
	my ($ID,$ing);
	my $ingQuery = "SELECT IngredientID,IngredientName FROM Ingredients";
	my $ing_handler = &dh_utils::sqlQueryHandler($ingQuery, "YES");
	my $ingList = "<datalist id=\"inglist\">\n";
	while(($ID,$ing) = $ing_handler->fetchrow())
	{
		$ingList.="<option value=\"$ing\" id=\"$ID\">\n";
	}
	$ingList.="</datalist>\n";

	&dh_utils::updatePage("admin_template.txt","temp_admin.html",$ingList, "<datalist id=\"inglist\">");


	##update alternative name box' list
	my $altQuery = "SELECT IngredientID,IngredientName FROM Ingredients WHERE AltID IS NULL";
	my $alt_handler = &dh_utils::sqlQueryHandler($altQuery, "YES");
	my $altList = "<datalist id=\"group\">\n";
	
	while(($ID,$ing) = $alt_handler->fetchrow())
	{
		$altList .= "<option value=\"$ing\" id=\"$ID\">\n";
	}
	$altList.="</datalist>\n";

	&dh_utils::updatePage("temp_admin.html","../admin_page.html",$altList, "<datalist id=\"group\">");
}

sub updSrchByName{
	
	my ($ID,$name);
	my $query = "SELECT CocktailID,CocktailName FROM Cocktails";
	my $query_handler = &dh_utils::sqlQueryHandler($query, "YES");
	my $params="<datalist id=\"cocktailList\">\n";

	while (($ID,$name) = $query_handler->fetchrow())
	{
       		$params.="\t<option value=\"$ID\">$name</option>\n";
	}

	$params.="</datalist>\n";
	print STDERR "params = $params\n";
	&dh_utils::updatePage("search_by_name.txt","../search_by_name.html",$params,"<datalist id=\"cocktailList\">");

}
1;
