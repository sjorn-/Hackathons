module.exports = {
// Returns an array of Objects with Card Data.
// Usage `getCards();`
    getCards: function(n) {
        // Do the stuff to get the data from the place
        var request = require('urllib-sync').request;
        // Make the data from the place random
        var x = Math.floor(Math.random() * (10001-n));

        var res = request('http://elastic.hackathon.cdlaws.co.uk/_search?source={"from":'+x+',"size":'+n+',"query":{"bool":{"must":{"match_all":{}},"filter":{"geo_distance_range":{"from":"0km","to":"20km","location":{"lat":53.46,"lon":-2.23}}}}}}', {dataType: 'json'});
    
        // Uncomment to view cards that are recieved.
        //console.log(res.data);
        console.log("Got response from database!");
        
        // Put the stuff from the place into a nice cosy place that we make and then
        // group up the cosy places.
        var entries = new Array();
        var i, r;
        for (i = 0; i < n; i++) {
            r = {
        	        description:            res.data.hits.hits[i]._source.accidentSeverity+' Accident on '+res.data.hits.hits[i]._source.dayOfWeek+', '+res.data.hits.hits[i]._source.year,
        	        "Accident severity":       res.data.hits.hits[i]._source.accidentSeverity,
        	        "Number of vehicles":       res.data.hits.hits[i]._source.numberofVehicles,
        	        "Number of casualties":     res.data.hits.hits[i]._source.numberofCasualties,
	                "Speed limit":             res.data.hits.hits[i]._source.speedlimit,
       		        "Light conditions":        res.data.hits.hits[i]._source.lightConditions,
        	        "Weather conditions":      res.data.hits.hits[i]._source.weatherConditions
	              }
            // Add the cosy place to the group of more cosy places
  	        entries.push(r);
        }
        // Share the cosiness!
        return entries;
    }
}

