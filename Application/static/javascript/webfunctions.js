function loadFormationPage() {
    // loads the formationspage
    fetch('/formationpage')
        .then(response => response.json())
        .then(competitions_json => loadChoicesMenu("keuzeCompetitie", competitions_json));
}

function getAllFormations(league) {
    //
    fetch('/getformationsoptions/' + league)
        .then(response => response.json())
        .then(formations_json => loadChoicesMenu("keuzeFormaties", formations_json))
}

function getFormationRecommendation() {
    //
    if (sessionStorage.getItem("chosenLeague") === null && sessionStorage.getItem("chosenFormation") == null) {
        alert("Selecteer een competitie en een formatie.")
    } else {
        let league = sessionStorage.getItem("chosenLeague");
        let formation = sessionStorage.getItem("chosenFormation");

        fetch('/recomformation/' + formation + '/' + league)
            .then(response => response.json())
            .then(formations_json => test_script(formations_json))
    }
}

function loadChoicesMenu(elementId, json_info) {
    //
    console.log(json_info)
    let elements = json_info['values']
    let x = document.getElementById(elementId);
    for (i = 0; i < elements.length; i++) {
        let option = document.createElement("option");
        option.text = elements[i];
        x.add(option);
    }
}

function set_cookie_league() {
    //
    let leagueChoice = this.options[this.selectedIndex].text;
    console.log(leagueChoice);
    sessionStorage.setItem('chosenLeague', leagueChoice);
    getAllFormations(leagueChoice)
}

function set_cookie_formation() {
    //
    let formationChoice = this.options[this.selectedIndex].text;
    console.log(formationChoice)
    sessionStorage.setItem('chosenFormation', formationChoice)
}

function test_script(asdf) {
    console.log(asdf)
    alert(asdf["recoms"])
}