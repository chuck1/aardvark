
deepcopy = function(a) {
	if(a instanceof Array) {
		console.log('is array');
	} else if(a instanceof Object) {
		console.log('is object');
	} else {
		console.log('is type', typeof(a));
		return a;
	}
	return a;
}

union = function(setA, setB) {
	var union = new Set(setA);
	for (var elem of setB) {
		union.add(elem);
	}
	return union;
}


function navigate(a, address) {
	address.forEach(function(line) {
		a = line.navigate(a);
	});
	return a;
}

class Operation {
	constructor(address = []) {
		// TODO this is a shallow copy. but do I need a deep copy here?
		this.address = address.slice();
	}
	apply(a) {
		a = navigate(a, this.address)
		this.apply2(a)
	}
	apply2(a) {
		//raise NotImplementedError()
	}
}

class OperationPair extends Operation {
	constructor(address, pair) {
		super(address);
		this.pair = copy.deepcopy(pair)
	}
	repr() {
		return '<'+' address='+' pair='+'>'
	}
}
class OperationPairRemove extends OperationPair {
}
class OperationPairAdd extends OperationPair {
	apply2(a) {
		a[this.pair[0]] = this.pair[1];
	}
}
class OperationReplace extends Operation {
	constructor(a, b, address) {
		super(address);
		this.type = "OperationReplace";
		this.a = deepcopy(a);
		this.b = deepcopy(b);
	}
	repr() {
		return '<{elf.__class__.__name__} a={elf.a} b={elf.b} address={elf.address}>'
	}
}
class AddressLine {
}
class AddressLineKey {
	constructor(key) {
		this.type = "AddressLineKey";
		this.key = key;
	}
	navigate(a) {
		return a[this.key];
	}
	repr() {
		return '<{lf.__class__.__name__} key={elf.key}>';
	}
}
class AddressLineIndex {
	constructor(index) {
		this.index = index
	}
	navigate(a) {
		return a[this.index];
	}
}
function* diff_dicts(a, b, address) {

	var keys_a = new Set(Object.keys(a));
	var keys_b = new Set(Object.keys(b));
	var just_a = keys_a - keys_b;
	var just_b = keys_b - keys_a;
	var a_and_b = union(keys_a, keys_b);


	for(var k in just_a) {
		yield (new OperationPairRemove(address, (k, a[k])));
	}
	for(var k in just_b) {
		yield (new OperationPairAdd(address, (k, b[k])));
	}
	for(var k of a_and_b) {
		for(let d of diff(a[k], b[k], address.concat([new AddressLineKey(k)]))) {
			yield d;
		}
	}
}

//[Symbol.iterator]

diff = function* (a, b, address=[]) {
	if(a == b) {
		//return;
	} else {

		if((a instanceof Object) && (b instanceof Object)) {
			//var arr = diff_dicts(a, b, address);
			//for(var i = 0; i < arr.length; ++i) {
			for(let d of diff_dicts(a, b, address)) {
				//yield (arr[i]);
				yield d;
			}
		} else {
			yield (new OperationReplace(a, b, address));
		}
	}
}

function apply(a, diff_list) {
	a = copy.deepcopy(a)
	diff_list.forEach(function(d) {
		d.apply(a);
	});
	return a;
}

module.exports.diff = diff;





