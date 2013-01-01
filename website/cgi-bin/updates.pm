#!/usr/bin/perl
use Data::Dumper;
use DBI;
use DBD::mysql;
use dh_utils qw( updatePage sqlQueryHandler );

package updates;

require Exporter;
require dh_utils;
our @ISA= qw( Exporter );
our @EXPORT_OK= qw( updAdminPage updSrchByName updSearchByIng);
our @EXPORT= qw( UpdAdminPage updSrchByName updSearchByIng );

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
       		$params.="\t<option value=\"$name\">\n";
	}

	$params.="</datalist>\n";
	print STDERR "params = $params\n";
	&dh_utils::updatePage("search_by_name.txt","../search_by_name.html",$params,"<datalist id=\"cocktailList\">");

}

sub updSearchByIng{
	
	my $arrayList = "var ingNumList = [";
        my $ingList = "<datalist id=\"inglist\">\n";
        my $catList1= "";
	my $catList2= "";
	my $ingQuery = "SELECT IngredientId,IngredientName,Category From Ingredients"; 
	my $ingHandler = &dh_utils::sqlQueryHandler($ingQuery,"YES");
	my ($ingId,$ingName,$category);
	my $flag = 0;
	
	while(($ingId,$ingName,$category)=$ingHandler->fetchrow())
	{	if($flag){
			$arrayList .= ",";
		}
		else{
			$flag=1;
		}
		$ingList .= "<option value=\"$ingName\">\n";
		$arrayList .= "\"$ingName\",\"$ingId\"";
		if ($category eq "alc")
		{
			$catList1 .= "<a onmouseover=\"\" style=\"cursor: pointer;\" onclick=\"addEvent('$ingName')\">$ingName</a><br>\n";
		}
		else
		{
			$catList2 .= "<a onmouseover=\"\" style=\"cursor: pointer;\" onclick=\"addEvent('$ingName')\">$ingName</a><br>\n";
		}
	}
#	print STDERR "ingList = $ingList\narray=$arrayList\ncetegory1=$catList1\ncategory2=$catList2\n";
	$arrayList .= "]";
	$ingList .= "</datalist>\n";
	&dh_utils::updatePage("searchIng_Template.txt","temp_searchIng.html",$arrayList,"VAR_ARRAY");
	&dh_utils::updatePage("temp_searchIng.html","temp_searchIng.html",$ingList,"INGREDIENTLIST");
	&dh_utils::updatePage("temp_searchIng.html","temp_searchIng.html",$catList1,"CATLIST1");
	&dh_utils::updatePage("temp_searchIng.html","../search_by_ing.html",$catList2,"CATLIST2");

}






1;


