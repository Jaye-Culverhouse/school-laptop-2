let table;
let filtered;

let timeMin;
let timeMax;

function setup() {
	noCanvas();
	let body = table = select("body");
	filtered = false;
	table = select("#TABLE_CONT");
	table.center();
	for(row in data){
		
		let r = createElement("tr");
		
		let d = createElement("td", new Date(data[row][0]*1000).toLocaleString("en-GB", dateOptions)); // TIME
		r.child(d);
		
		d = createElement("td", data[row][1]); // DEVICE NAME
		d.mouseClicked(filterTableByDevice);
		r.child(d);
		
		d = createElement("td", data[row][2]); // DEVICE OPERATION
		r.child(d);
		
		d = createElement("td", data[row][3]); // NAME
		d.mouseClicked(filterTableByName);
		r.child(d);
		
		r.parent(table);
	}
	
	let children = table.child();
	
	let flags = Array(children.length-2).fill(false);
	
	for(let i = 2; i < children.length; i++){
		let x = i-2;
		if(flags[x] || children[i]["cells"][2].innerHTML == "IN"){
			continue;
		}
		flags[x] = true;
		
		let h = children[i]["cells"][1].innerHTML+children[i]["cells"][3].innerHTML;
		
		for(let j = i+1; j < children.length; j++){
			let h2 = children[j]["cells"][1].innerHTML+children[j]["cells"][3].innerHTML;
			if(h === h2){
				flags[j-2] = true;
				let c = "rgb("+random(100,230)+","+random(100,230)+","+random(100,230)+")";
				children[i].style.backgroundColor = c;
				children[j].style.backgroundColor = c;
				break;
			}
		}
	}
	

}

function keyPressed(){
	if(filtered){
		
		filtered = false;
		let children = table.child();
	
		for(let i = 2; i < children.length; i++){
		
			if(int(children[i].cells[1].innerHTML) != filter){
				children[i].style.display="";
			}
		
		}
		
		
	}
}

function filterTableByDevice(){
	
	let filter = int(event["path"][0].innerHTML);
	filtered = true;
	
	let children = table.child();
	
	for(let i = 2; i < children.length; i++){
		
		if(int(children[i].cells[1].innerHTML) != filter){
			children[i].style.display="none";
			
		}
		
	}
		
}

function filterTableByName(){
	
	let filter = event["path"][0].innerHTML;
	filtered = true;
	
	let children = table.child();
	
	for(let i = 2; i < children.length; i++){
		
		if(children[i].cells[3].innerHTML != filter){
			children[i].style.display="none";
			
		}
		
	}
		
}

