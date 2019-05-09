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
		
		let d = createElement("td", new Date(data[row][0]*1000).toUTCString()); // TIME
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
	
	
	

	timeMin = document.getElementById("tMin");
	
	let minDT = new Date(data[0][0]*1000).toISOString();
	minDT = minDT.substring(0, minDT.length-5);
	timeMin.value = minDT;

	
	
	timeMax = document.getElementById("tMax");
	
	let maxDT = new Date(data[data.length-1][0]*1000).toISOString();
	maxDT = maxDT.substring(0, maxDT.length-8);
	timeMax.value = maxDT;
	
	timeMin.min = minDT;
	timeMin.max = maxDT;
	timeMax.min = minDT;
	timeMax.max = maxDT;
	
}

function keyPressed(){

		
		filtered = false;
		let children = table.child();
	
		for(let i = 2; i < children.length; i++){
		
			if(int(children[i].cells[1].innerHTML) != filter){
				children[i].style.display="";
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

function filterTableByTime(){
		
	let children = table.child();
	
	const fMin = (+new Date(timeMin.value)+3600000)/1000;
	const fMax = (+new Date(timeMax.value)+3600000)/1000;
	
	console.log(fMax);
		
	for(let i = 0; i < data.length; i++){
		
		if(data[i][0] < fMin || data[i][0] > fMax){
			children[i+2].style.display="none";
		}else{
			children[i+2].style.display="";
		}
	}
	
}

