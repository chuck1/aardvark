var aard = require("./aardvark.js");

a = new Object();
b = new Object();

a['a'] = 1;
b['a'] = 2;

for(let d of aard.diff(a, b)) {
	console.log(d);
	console.log(JSON.stringify(d));
}



