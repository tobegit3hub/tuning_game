var width = 800;
var height = 600;
var game = new Phaser.Game(width, height, Phaser.AUTO, "game");

var spacefield;
var backgroundv;
var player;
var cursors;
var bullets;
var bulletTime = 0;
var enemies;
var score = 0;
var scoreText;
var winText;

// For TuningGame
var metrics = "none";
var metricsTextWidge;
var submitButton;
var inputParameterTextWidget;
var inputParameterValue;

var mainState = {

    preload: function () {
        game.stage.backgroundColor = '#000000';

        // Load images
        game.load.image("starfield",
            "/static/phaser_tutorial/images/starfield.png");
        game.load.image("player", "/static/phaser_tutorial/images/player.png");
        game.load.image("bullet", "/static/phaser_tutorial/images/bullet.png");
        game.load.image("enemy", "/static/phaser_tutorial/images/enemy.png");
        game.load.image("submitButton",
            "/static/phaser_tutorial/images/submit_button.png");

        // Load audio
        game.load.audio("bgm",
            "/static/games/audio/pokemon2.mp3");
    },

    create: function () {

        // Set game engine
        game.physics.startSystem(Phaser.Physics.ARCADE);

        //spacefield = game.add.tileSprite(0, 0, 800, 600, "starfield");
        spacefield = game.add.tileSprite(0, 0, width, height, "starfield");

        backgroundv = 5;

        player = game.add.sprite(game.world.centerX, game.world.centerY + 200,
            "player");
        game.physics.enable(player, Phaser.Physics.ARCADE);

        cursors = game.input.keyboard.createCursorKeys();

        bullets = game.add.group();
        bullets.enableBody = true;
        bullets.physicsBodyType = Phaser.Physics.ARCADE;
        bullets.createMultiple(30, "bullet");
        bullets.setAll("anchor.x", 0.5);
        bullets.setAll("anchor.y", 1);
        bullets.setAll("outOfBoundsKill", true);
        bullets.setAll("checkWorldBounds", true);

        fireButton = game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);

        enemies = game.add.group();
        enemies.enableBody = true;
        enemies.physicsBodyType = Phaser.Physics.ARCADE;

        createEnemies();

        scoreText = game.add.text(0, 550, "Score:",
            {font: "32px Arial", fill: "#fff"});
        winText = game.add.text(game.world.centerX, game.world.centerY,
            "You won!", {font: "32px Arial", fill: "#fff"});
        winText.visible = false;

        // For TuningGame
        metricsTextWidge = game.add.text(16, 16, "Metrics: none",
            {font: "32px Arial", fill: "#fff"});

        inputParameterTextWidget = game.add.text(16, 64, "x: none",
            {font: "32px Arial", fill: "#fff"});

        submitButton = game.add.button(game.world.centerX - 95, 400,
            "submitButton", submitButtonOnClick, this, 2, 1, 0);

        music = game.sound.play("bgm");

    },

    update: function () {

        game.physics.arcade.overlap(bullets, enemies, collisionHandler, null,
            this);

        spacefield.tilePosition.y += backgroundv;

        // Update while pressing keyboards
        player.body.velocity.x = 0;

        if (cursors.left.isDown) {
            player.body.velocity.x = -350;
        }

        if (cursors.right.isDown) {
            player.body.velocity.x = 350;
        }

        if (fireButton.isDown) {
            fireBullet();
        }

        scoreText.text = "Score: " + score;

        if (score == 4000) {
            scoreText.visible = false;
            winText.visible = true;
        }


        // For TuningGame
        inputParameterValue = $("input#parameter1").get(0).value;
        inputParameterTextWidget.text = "x: " + inputParameterValue;

    }

};

function fireBullet() {
    if (game.time.now > bulletTime) {
        bullet = bullets.getFirstExists(false);

        if (bullet) {
            bullet.reset(player.x, player.y)
            bullet.body.velocity.y = -400;
            bulletTime = game.time.now + 200;
        }
    }
}

function createEnemies() {
    for (var y = 0; y < 4; y++) {
        for (var x = 0; x < 10; x++) {
            var enemy = enemies.create(x * 48, y * 50, "enemy");
            enemy.anchor.setTo(0.5, 0.5);
        }

    }

    enemies.x = 100;
    enemies.y = 50;

    var tween = game.add.tween(enemies).to({x: 200}, 2000,
        Phaser.Easing.Linear.None, true, 0, 1000, true);

    tween.onLoop.add(descend, this);
}

function descend() {
    enemies.y ** 10;
}

function collisionHandler(bullet, enemy) {
    bullet.kill();
    enemy.kill();

    score += 100;
}

function updateMetricsTextWidget(metrics) {
    //console.log("Update the metrics text widget: " + metrics);
    metricsTextWidge.text = "Metrics: " + metrics;
}

// Click the submit button
function submitButtonOnClick() {
    console.log("Click submit button");

    parameterValue = parseFloat(inputParameterValue);
    request_data = {
        "participation_id": 69,
        "parameters_instance": {"x": parameterValue}
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

                metrics = data["data"]["metrics"];
                updateMetricsTextWidget(metrics);
            });

        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });

}

game.state.add("mainState", mainState);

game.state.start("mainState");

$(document).ready(function () {
    // Update with default parameters
    inputParameterValue = $("input#parameter1").text();

});