var width = 800;
var height = 600;

var game = new Phaser.Game(width, height, Phaser.CANVAS, 'game', { preload: preload, create: create, update: update, render: render });



var player;
var facing = 'right';
var jumpTimer = 0;
var cursors;
var jumpButton;
var background;

var metricsValue = "none";
var metricsText;
var submitButton;
var parameterX1Text;
var parameterX1Value;
var parameterX2Text;
var parameterX2Value;



function preload() {

    game.load.spritesheet('player', '/static/high_jump/images/player.png', 32, 48);
    game.load.image('background', '/static/high_jump/images/background.png');
    game.load.image("submitButton", "/static/high_jump/images/submit_button.png");

    game.load.audio("bgm", "/static/games/audio/pokemon.mp3");

}



function create() {

    game.physics.startSystem(Phaser.Physics.ARCADE);

    game.time.desiredFps = 30;

    background = game.add.tileSprite(0, 0, 800, 600, 'background');

    game.physics.arcade.gravity.y = 250;

    player = game.add.sprite(32, 32, 'player');
    game.physics.enable(player, Phaser.Physics.ARCADE);

    player.body.bounce.y = 0.2;
    player.body.collideWorldBounds = true;
    player.body.setSize(20, 32, 5, 16);

    player.animations.add('left', [0, 1, 2, 3], 10, true);
    player.animations.add('turn', [4], 20, true);
    player.animations.add('right', [5, 6, 7, 8], 10, true);

    cursors = game.input.keyboard.createCursorKeys();
    jumpButton = game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);


    submitButton = game.add.button(game.world.right - 120, 550,
        "submitButton", submitButtonOnClick, this, 2, 1, 0);

    music = game.sound.play("bgm");


    metricsText = game.add.text(16, 16, "Metrics: none",
        {font: "32px Arial", fill: "#fff"});

    parameterX1Text = game.add.text(16, 64, "x1: none",
        {font: "32px Arial", fill: "#fff"});

    parameterX2Text = game.add.text(16, 112, "x2: none",
        {font: "32px Arial", fill: "#fff"});

}

function update() {

    // game.physics.arcade.collide(player, layer);

    parameterX1Value = $("input#x1").get(0).value;
    parameterX1Text.text = "x1: " + parameterX1Value;

    parameterX2Value = $("input#x2").get(0).value;
    parameterX2Text.text = "x2: " + parameterX2Value;


    player.body.velocity.x = 0;

    if (cursors.left.isDown)
    {
        player.body.velocity.x = -150;

        if (facing != 'left')
        {
            player.animations.play('left');
            facing = 'left';
        }
    }
    else if (cursors.right.isDown)
    {
        player.body.velocity.x = 150;

        if (facing != 'right')
        {
            player.animations.play('right');
            facing = 'right';
        }
    }
    else
    {
        if (facing != 'idle')
        {
            player.animations.stop();

            if (facing == 'left')
            {
                player.frame = 0;
            }
            else
            {
                player.frame = 5;
            }

            facing = 'idle';
        }
    }

    if (jumpButton.isDown && player.body.onFloor() && game.time.now > jumpTimer)
    {
        player.body.velocity.y = -150;
        //[-413, 100] -> [150, 500]

        if (metricsValue > 0) {
            console.log("Update velocity as: -1 * " + metricsValue)
            player.body.velocity.y = -3 * metricsValue - 100 ;
        } else {
            player.body.velocity.y = -100;
        }



        jumpTimer = game.time.now + 750;
    }

}

function render () {
    //game.debug.text(game.time.suggestedFps, 32, 32);
    // game.debug.text(game.time.physicsElapsed, 32, 32);
    // game.debug.body(player);
    // game.debug.bodyInfo(player, 16, 24);

}



// Click the submit button
function submitButtonOnClick() {
    console.log("Click submit button");

    parameterX1 = parseFloat(parameterX1Value);
    parameterX2 = parseFloat(parameterX2Value);

    request_data = {
        // TODO: Get participation id
        "participation_id": 75,
        "parameters_instance": {"x1": parameterX1, "x2": parameterX2}
    }

    // Request to create the trial
    $.ajax({
        url: 'http://127.0.0.1:8000/tuning/v1/trials',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(request_data),
        processData: false,
        success: function (data, textStatus, jQxhr) {
            console.log("Succeed to create the trial");

            trial_id = data["data"]["id"];

            // Request to execute the trial
            $.post("http://127.0.0.1:8000/tuning/v1/trials/" + trial_id
                + "/execute", function (data, status) {

                console.log("Succeed to execute the trial");

                metricsValue = data["data"]["metrics"];
                metricsText.text = "Metrics: " + metricsValue;
            });

        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });

}


$(document).ready(function () {
    // Update with default parameters
    parameterX1Value = $("input#x1").text();
    parameterX2Value = $("input#x2").text();

});