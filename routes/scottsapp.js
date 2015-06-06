var mongo = require('mongodb');
 
var Server = mongo.Server,
Db = mongo.Db,
BSON = mongo.BSONPure;
 
var server = new Server('localhost', 27017, {auto_reconnect: true});
db = new Db('scottsapp', server);
 
db.open(function(err, db) {
		if(!err)
		{
			console.log("Connected to 'scottsapp' database");
			db.collection('cityevents', {strict:true}, function(err, collection)
			{
				if (err)
				{
					console.log("The 'cityevents' collection doesn't exist. Creating it with sample data...");
					populateDB();
				}
			});
		}
	}
);

exports.findById = function(req, res) {
var id = req.params.id;
console.log('Retrieving cityevents: ' + id);
db.collection('events', function(err, collection) {
collection.findOne({'_id':new BSON.ObjectID(id)}, function(err, cityevent) {
res.send(cityevent);
});
});
};
 
exports.findAll = function(req, res) {
db.collection('cityevents', function(err, collection) {
collection.find().toArray(function(err, cityevents) {
res.send(cityevents);
});
});
};
 
exports.addCityEvent = function(req, res) {
var cityevent = JSON.parse(req.body["string"]);
console.log('Adding event: ' + JSON.stringify(cityevent));
db.collection('cityevents', function(err, collection) {
collection.insert(cityevent, {safe:true}, function(err, result) {
if (err) {
res.send({'error':'An error has occurred'});
} else {
console.log('Success: ' + JSON.stringify(result[0]));
res.send(result[0]);
}
});
});
}
 
exports.updateCityEvent = function(req, res) {
	var id = req.params.id;
	var roadevent = JSON.parse(req.body["string"]);
	console.log("Update cityevent: " +id + " : "+ JSON.stringify(cityevent));
	db.collection('cityevents', function(err, collection) {
		collection.update({'_id':new BSON.ObjectID(id)}, cityevent, {safe:true}, function(err, result) {
			if (err) {
				console.log('Error updating cityevent: ' + err);
				res.send({'error':'An error has occurred'});
			} else {
				console.log('' + result + ' document(s) updated');
				cityevent._id = id;
				res.send(roadevent);
			}
		});
	});
}
 
exports.deleteCityEvent = function(req, res) {
var id = req.params.id;
console.log('Deleting cityevent: ' + id);
db.collection('cityevents', function(err, collection) {
collection.remove({'_id':new BSON.ObjectID(id)}, {safe:true}, function(err, result) {
if (err) {
res.send({'error':'An error has occurred - ' + err});
} else {
console.log('' + result + ' document(s) deleted');
res.send(req.body);
}
});
});
}
 
/*--------------------------------------------------------------------------------------------------------------------*/
// Populate database with sample data -- Only used once: the first time the application is started.
// You'd typically not find this code in a real-life app, since the database would already exist.
var populateDB = function()
{
	var cityevents = [
		{
			"title":"Make'm Smile",
			"description":"Join us for the BIGGEST PARTY celebrating kids with special needs in the United States! Make ‘m Smile is an annual community festival the first Saturday of every June dedicated to lovin’ on VIP Kids (kids with all types of special needs/disabilities) and their families. We invite people from the community to stroll around the park, while enjoying entertainment, food, and family activities.",
			"life": {
				"start":"2015/05/28",
				"end":"2015/06/07"
			},
			"url":"http://www.nathanielshope.org/events-programs/make-m-smile/",
			"contact":"For event information, contact 321.281.2053.",
			"roadevents": [
				{
					"type":"closure",
					"schedule":"6 p.m. Friday, June 5 and continuing until Saturday, June 6 at 5:00 p.m.",
					"description":"Robinson Street from Summerlin Avenue to Rosalind Avenue"
				},
				{
					"type":"closure",
					"schedule":"6 p.m. Friday, June 5 and continuing until Saturday, June 6 at 5:00 p.m.",
					"description":"Eola Drive from Robinson Street to Washington Street"
				},
				{
					"type":"closure",
					"schedule":"6 p.m. Friday, June 5 and continuing until Saturday, June 6 at 5:00 p.m.",
					"description":"Osceola Avenue cul de sac"
				},
			]
		}
	];
	db.collection('cityevents', function(err, collection) {
	collection.insert(cityevents, {safe:true}, function(err, result) {});
	});
};
