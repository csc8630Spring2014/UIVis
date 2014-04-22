function showDetail(d) {
	//window.open(d.pdb_url); 
	//window.open(d.cath_url);
	var left = 950, top = 10, offset = 385, element, id;
	top = top + (offset * window.clicked);

	var detailDiv = document.createElement('div');
	if(window.clicked == 0)
	{
		id = '#detail0';
		ZOT(id);
		window.clicked += 1;
	} else {
		id = '#detail1';
		ZOT(id);
		window.clicked = 0;
	}
	console.log(id);
	detailDiv.setAttribute("id", id);
	detailDiv.setAttribute("class", id);
	detailDiv.setAttribute("style", "border-style:solid;border-color:#a9a9C2;border-radius:15px;position:absolute;top:"+top+"px;left:"+left+"px;z-index:100;width:300px;height:380;pxbackground-color:#FFFFFF;whitespace:pre-wrap;");
	detailDiv.innerHTML += '<p style="margin-left: 1.5em;">'+ d.organism + '<br>PDB ID: <a target="_blank" href="' + d.pdb_url + '">' + d.name + '</a> <br>' + d.pdb_class;
	var name = d.name.substring(0,4).toLowerCase();
	detailDiv.innerHTML += '<a target="_blank" href="' + d.pdb_url + '">';
	detailDiv.innerHTML += '<center><img src="http://www.rcsb.org/pdb/images/'+name+'_bio_r_500.jpg" width=200 height=200 alt="Protein Structure"></a></center>';
	detailDiv.innerHTML += '<p style="margin-left: 1.5em;">Residues : ' + d.residues + '<br> Weight : ' + d.weight + '<br>Superfamily : <a target="_blank" href="' + d.cath_url + '">'  + d.cathid +'</a>';
	document.body.appendChild(detailDiv);	
}
	

function isFloat(n) {
    return n === +n && n !== (n|0);
}

function isInteger(n) {
    return n === +n && n === (n|0);
}

function ZOT(id) {
	var element = document.getElementById(id);
	if(element)
		element.parentNode.removeChild(element);
	return false;
}