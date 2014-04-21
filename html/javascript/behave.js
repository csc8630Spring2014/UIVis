//collapse parent on click
function click(d) {
	if (d.children) {
		d._children = d.children;
		d.children = null;
	} else {
		d.children = d._children;
		d._children = null;
	}
	update(d);
}

function color(d) {
	if (!d.children) {
		var c = ""
		try {
			c = colorList[d.organism];
		} catch (e) {
			console.log(d.organism + " " + colorList[d.organism]);
		}
	}	
	//console.log("count = " + d.children.length);
	return d._children ? "#3182bd" : d.children ? "#c6dbef" : c;
}

function changeText(d)
{
	text = textnode.textContent
	textnode.textContent = "test"
}

function restoreText()
{
	textnode.textContent = text
}

function nodeClick(d)
{

}