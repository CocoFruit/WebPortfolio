// on load
window.onload = function(){
    // doTheThings();
}

function create_pedal(rot){
    var pedal = document.createElement("div");
    pedal.classList.add("flower__leaf");
    pedal.classList.add("flower__leaf--basic");
    // rotate the pedal
    pedal.style.transform = "rotate(" + rot + "deg)";
    return pedal
}

function create_flower(){
    var flower = document.createElement("div");
    flower.classList.add("flower");
    // create 5 pedals
    for (var i = 0; i < 11; i++){
        rot = i * 32;
        flower.appendChild(create_pedal(rot));
    }
    var stem = document.createElement("div");
    stem.classList.add("stem");
    flower.appendChild(stem);
    return flower;
}

function doTheThings(){
    // create a flower
    var flower = create_flower();
    // add it to the body
    document.body.appendChild(flower);
}
