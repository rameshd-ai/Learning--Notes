exports.handler = (event, context, callback) => {
    var specialty = event.currentIntent.slots.Specialty;
    var insurance = event.currentIntent.slots.Insurance;
    var language = event.currentIntent.slots.Language;
    var city = event.currentIntent.slots.City;
    var message;

    message = "Dr. Awesome is a " + specialty + " who speaks " + language + ", accepts " + 
        insurance + " insurance and has an office in " + city;

        callback(null, {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    });
};