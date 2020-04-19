exports.handler = (event, context, callback) => {
    var specialty = event.currentIntent.slots.Specialty;
    var insurance = event.currentIntent.slots.Insurance;
    var language = event.currentIntent.slots.Language;
    var city = event.currentIntent.slots.City;
    var message;
    var contentTypeValue;   

    if(event.outputDialogMode === 'Text') {
        contentTypeValue = 'PlainText';

        if (language !== null) {
            message = "Dr. Awesome is a " + specialty + " who speaks " + language + ", accepts " + 
                insurance + " insurance and has an office in " + city;
        } else {
            message = "Dr. Awesome is a " + specialty + " who accepts " + insurance + 
                " insurance and has an office in " + city;
        }
    }
    else {
        contentTypeValue = 'SSML';

        if (language !== null) {
            message = "<speak>Dr. Awesome at <say-as interpret-as='telephone'>801-999-1234</say-as> is a " + 
                specialty + " who speaks " + language + ", accepts " + insurance + 
                " insurance and has an office in " + city + "</speak>";
        } else {
//            message = "<speak>Dr. Awesome at <say-as interpret-as='telephone'>8019991234</say-as> is a " + 
//                specialty + " who accepts " + insurance + 
//                " insurance and has an office in " + city + "</speak>";
            message = "<speak>Dr. Awesome at 8019991234 is a " + specialty + " who accepts " + insurance + 
                " insurance and has an office in " + city + "</speak>";
        }
    }

        callback(null, {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": contentTypeValue,
                "content": message
            }
        }
    });
};