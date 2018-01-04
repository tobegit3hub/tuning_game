
// Phaser variables
var width = 800;
var height = 600;
var game = new Phaser.Game(width, height, Phaser.CANVAS, 'game', { preload: preload, create: create, update: update, render: render });

// Game variables
var player;
var facing = 'right';
var jumpTimer = 0;
var cursors;
var jumpButton;
var background;
var platforms;
var stars;
var starNumber = 0;
var starNumberText;
var winText;

// TuningGame variables
var participationId = 1;
var parameterX1Text;
var parameterX1Value;
var parameterX2Text;
var parameterX2Value;
var metricsValue = "none";
var metricsText;
var submitButton;


function preload() {
    // Load images
    game.load.spritesheet('player', '/static/high_jump/images/player.png', 32, 48);
    game.load.image('background', '/static/high_jump/images/background.png');
    game.load.image("submitButton", "/static/high_jump/images/submit_button.png");
    game.load.image('star', '/static/high_jump/images//star.png');
    game.load.image('platform', '/static/high_jump/images//platform.png');

    // Load audio
    game.load.audio("bgm", "/static/games/audio/pokemon.mp3");

}



function create() {

    // Game settings
    game.physics.startSystem(Phaser.Physics.ARCADE);
    game.time.desiredFps = 30;

    // Background, Music and control
    background = game.add.tileSprite(0, 0, 800, 600, 'background');
    music = game.sound.play("bgm");
    cursors = game.input.keyboard.createCursorKeys();
    jumpButton = game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);

    // Create player
    player = game.add.sprite(32, 32, 'player');
    game.physics.enable(player, Phaser.Physics.ARCADE);
    player.body.bounce.y = 0.2;
    player.body.collideWorldBounds = true;
    player.body.setSize(20, 32, 5, 16);
    player.body.gravity.y = 350;
    player.animations.add('left', [0, 1, 2, 3], 10, true);
    player.animations.add('turn', [4], 20, true);
    player.animations.add('right', [5, 6, 7, 8], 10, true);

    // Create platforms
    platforms = game.add.group();
    platforms.enableBody = true;

    // Platform image is 400 * 32
    var platform1 = platforms.create(400, 500, 'platform');
    platform1.body.immovable = true;

    var platform2 = platforms.create(-150, 450, 'platform');
    platform2.body.immovable = true;

    var platform3 = platforms.create(450, 300, 'platform');
    platform3.body.immovable = true;

    // Create stars
    stars = game.add.group();
    stars.enableBody = true;
    for (var i = 0; i < 3; i++) {
        var x = (3 - i) * 100 + Math.random() * 150;
        var y = i * 100 + Math.random() * 150;
        var star = stars.create(x, y, 'star');
        star.body.bounce.y = 0.7 + Math.random() * 10.2;
        star.body.bounce.x = 0.7 + Math.random() * 10.2;
    }

    starNumberText = game.add.text(16, 550, 'Star: 0', { font: '24px Arial', fill: '#fff' });

    // TuningGame texts
    submitButton = game.add.button(game.world.right - 170, 550,
        "submitButton", submitButtonOnClick, this, 2, 1, 0);
    metricsText = game.add.text(16, 16, "Metrics: none",
        {font: "24px Arial", fill: "#fff"});
    // Update with default parameters
    parameterX1Value = $("input#x1").text();
    parameterX2Value = $("input#x2").text();
    parameterX1Text = game.add.text(16, 64, "x1: " + parameterX1Value,
        {font: "24px Arial", fill: "#fff"});
    parameterX2Text = game.add.text(16, 112, "x2: " + parameterX2Text,
        {font: "24px Arial", fill: "#fff"});
    participationId = $("p#participation_id").text();
    console.log("participationId: " + participationId);


    // Win text
    winText = game.add.text(game.world.centerX - 50, game.world.centerY,
        "You win!", {font: "24px Arial", fill: "#fff"});
    winText.visible = false;

}

function update() {
    // Check collision
    game.physics.arcade.collide(player, platforms);
    game.physics.arcade.collide(stars, platforms);
    game.physics.arcade.overlap(player, stars, collectStar, null, this);

    // Update parameter values
    parameterX1Value = $("input#x1").get(0).value;
    parameterX1Text.text = "x1: " + parameterX1Value;

    parameterX2Value = $("input#x2").get(0).value;
    parameterX2Text.text = "x2: " + parameterX2Value;

    // Move the player
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


    if (jumpButton.isDown && player.body.onFloor() && game.time.now > jumpTimer || jumpButton.isDown && player.body.touching.down && game.time.now > jumpTimer) {
        player.body.velocity.y = -150;
        //[-413, 100] -> [150, 500]

        if (metricsValue > 0) {
            console.log("Update velocity as: -1 * " + metricsValue)
            // TODO: Control the height of jump with TuningGame metrics
            player.body.velocity.y = -3 * metricsValue - 100 ;
        } else {
            player.body.velocity.y = -100;
        }

        jumpTimer = game.time.now + 300;
    }

}

function render () {
    // game.debug.text(game.time.suggestedFps, 32, 32);
    // game.debug.text(game.time.physicsElapsed, 32, 32);
    // game.debug.body(player);
    // game.debug.bodyInfo(player, 16, 24);

}

// When player touches the start
function collectStar(player, star) {
    star.kill();

    starNumber += 1;
    starNumberText.text = 'Star: ' + starNumber;

    // Display win text
    if(starNumber == 3) {
        winText.visible = true;
    }

}


// When user clicks the submit button
function submitButtonOnClick() {
    console.log("Click submit button");

    parameterX1 = parseFloat(parameterX1Value);
    parameterX2 = parseFloat(parameterX2Value);

    request_data = {
        "participation_id": participationId,
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