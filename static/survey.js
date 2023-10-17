// const SURVEY_ID = 1;

const surveyJson = {
    elements: [{
        name: "FirstName",
        title: "Enter your first name:",
        type: "text"
    }, {
        name: "LastName",
        title: "Enter your last name:",
        type: "text"
    }]
};

const survey = new Survey.Model(surveyJson);

function alertResults (sender) {
    $.post("/open_api/submit_survey", JSON.stringify(sender.data),
        function(data, textStatus) {
            //Gets called when browser recieves response from server
            console.log("DATA: ");
            console.log(data);

        }, "json").fail(function(response){
            console.log("Error");
            console.log(response);
        });
}

survey.onComplete.add(alertResults);

$(function() {
    $("#surveyContainer").Survey({ model: survey });
});