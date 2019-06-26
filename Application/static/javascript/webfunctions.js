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
            .then(formations_json => get_recoms(formations_json))
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

function get_recoms(recoms_dict) {
    //
    let recoms = recoms_dict["recoms"];
    console.log(recoms);

    let first_text = document.getElementById("first_formation");
    let second_text = document.getElementById("second_formation");

    if (recoms.length === 2) {
        let formation_1 = recoms[0];
        let formation_2 = recoms[1];

        first_text.textContent = formation_1;
        second_text.textContent = formation_2;

        draw_formations(formation_1, "first_canvas");
        draw_formations(formation_2, "second_canvas");
    } else {
        let formation_1 = recoms[0];

        first_text.textContent = formation_1;

        draw_formations(formation_1, "first_canvas");
    }
}

function fix_dpi(canvas, dpi) {
  let style = {
    height() {
      return +getComputedStyle(canvas).getPropertyValue('height').slice(0,-2);
    },
    width() {
      return +getComputedStyle(canvas).getPropertyValue('width').slice(0,-2);
    }
  };
  canvas.setAttribute('width', style.width() * dpi);
  canvas.setAttribute('height', style.height() * dpi);
}

function drawCircle(ctx, xPos, yPos, diam) {
    //
    ctx.beginPath();
    ctx.arc(xPos - (diam / 2), yPos, diam, 0, 2 * Math.PI, true);
    ctx.fillStyle = 'red';
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#000000';
    ctx.stroke();
}

function drawPlayingFieldSpecs(ctx, canvasWidth, canvasHeight) {
    // color the canvas
    ctx.fillStyle = "#68ba16";
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);

    // draw the penalty area
    ctx.strokeRect(canvasWidth / 4, 0, canvasWidth / 2, canvasHeight / 6);
    ctx.strokeRect(canvasWidth / 4, (canvasHeight / 6) * 5, canvasWidth / 2, canvasHeight / 6);

    // decorate the center line
    ctx.beginPath();
    ctx.moveTo(0, canvasHeight / 2);
    ctx.lineTo(canvasWidth, canvasHeight / 2);
    ctx.stroke();

    // draw the center circle
    ctx.beginPath();
    ctx.arc(canvasWidth / 2, canvasHeight / 2, canvasWidth / 4, 0, 2 * Math.PI, true);
    ctx.stroke();
}

function draw_formations(formation, id_target) {
    //
    let given_formation = formation;
    if (given_formation === "diamond") {
        given_formation = "4-1-2-1-2"
    }
    let positions = given_formation.split("-");
    // reversing the array and adding a keeper
    positions = positions.reverse();
    positions.push("1");

    let canvas = document.getElementById(id_target);
    let ctx = canvas.getContext("2d");
    let dpi = window.devicePixelRatio;
    fix_dpi(canvas, dpi);

    let canvasWidth = canvas.width;
    let canvasHeight = canvas.height;

    drawPlayingFieldSpecs(ctx, canvasWidth, canvasHeight);

    let playerDiam = 15;

    // calculate the delta between the lines
    let deltaYStep = canvasHeight / (positions.length + 2);
    // the variable holds the current position on the y-axis
    let currentYStep = deltaYStep;

    //
    for (let y = 0; y < positions.length + 1; y++) {
        //
        let playerCount = parseInt(positions[y - 1]);
        // calculate the space between two players
        let deltaXStep = canvasWidth / (playerCount + 1);
        //
        let currentXStep = deltaXStep;

        //
        for (let x = 0; x < playerCount; x++) {
            drawCircle(ctx, currentXStep, currentYStep, playerDiam);
            currentXStep += deltaXStep;
        }
        // increment the Ystep
        currentYStep += deltaYStep;
    }
}
