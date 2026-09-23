import webbrowser
from pathlib import Path


html = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<title>Taylor Expansion of e^x</title>

<style>

body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f7f7f7;
}

.container {
    max-width: 1000px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
}

h1 {
    text-align: center;
}

.controls {
    margin: 25px 0;
    text-align: center;
}

input[type="range"] {
    width: 70%;
}

#terms {
    font-size: 20px;
    font-weight: bold;
}

#polynomial {
    font-size: 20px;
    text-align: center;
    margin: 20px;
}

canvas {
    width: 100%;
    height: 500px;
    border: 1px solid #ccc;
}

</style>
</head>


<body>

<div class="container">

<h1>Taylor Expansion of \(e^x\)</h1>

<div class="controls">

<label>
Number of terms:
<strong id="terms">3</strong>
</label>

<br><br>

<input
    type="range"
    id="slider"
    min="1"
    max="20"
    value="3"
>

</div>


<div id="polynomial"></div>

<canvas id="graph"></canvas>

</div>


<script>

// ------------------------------------------------------------
// Canvas
// ------------------------------------------------------------

const canvas = document.getElementById("graph");
const ctx = canvas.getContext("2d");


// ------------------------------------------------------------
// Resize canvas
// ------------------------------------------------------------

function resizeCanvas() {

    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    draw();

}

window.addEventListener("resize", resizeCanvas);


// ------------------------------------------------------------
// Taylor approximation
// ------------------------------------------------------------

function factorial(n) {

    let result = 1;

    for (let i = 2; i <= n; i++) {
        result *= i;
    }

    return result;

}


function taylor(x, terms) {

    let sum = 0;

    for (let n = 0; n < terms; n++) {

        sum += Math.pow(x, n) / factorial(n);

    }

    return sum;

}


// ------------------------------------------------------------
// Coordinate transformation
// ------------------------------------------------------------

function xPixel(x, xmin, xmax) {

    return (x - xmin) /
           (xmax - xmin) *
           canvas.width;

}


function yPixel(y, ymin, ymax) {

    return canvas.height -
           (y - ymin) /
           (ymax - ymin) *
           canvas.height;

}


// ------------------------------------------------------------
// Draw graph
// ------------------------------------------------------------

function draw() {

    const terms =
        parseInt(document.getElementById("slider").value);

    const xmin = -4;
    const xmax = 4;

    const ymin = -5;
    const ymax = 60;


    // Clear
    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // --------------------------------------------------------
    // Grid
    // --------------------------------------------------------

    ctx.strokeStyle = "#dddddd";
    ctx.lineWidth = 1;

    for (let x = -4; x <= 4; x++) {

        const px = xPixel(
            x,
            xmin,
            xmax
        );

        ctx.beginPath();
        ctx.moveTo(px, 0);
        ctx.lineTo(px, canvas.height);
        ctx.stroke();

    }


    for (let y = 0; y <= 60; y += 10) {

        const py = yPixel(
            y,
            ymin,
            ymax
        );

        ctx.beginPath();
        ctx.moveTo(0, py);
        ctx.lineTo(canvas.width, py);
        ctx.stroke();

    }


    // --------------------------------------------------------
    // Axes
    // --------------------------------------------------------

    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 1.5;


    // x-axis

    const y0 = yPixel(
        0,
        ymin,
        ymax
    );

    ctx.beginPath();
    ctx.moveTo(0, y0);
    ctx.lineTo(canvas.width, y0);
    ctx.stroke();


    // y-axis

    const x0 = xPixel(
        0,
        xmin,
        xmax
    );

    ctx.beginPath();
    ctx.moveTo(x0, 0);
    ctx.lineTo(x0, canvas.height);
    ctx.stroke();


    // --------------------------------------------------------
    // Exact e^x
    // --------------------------------------------------------

    ctx.strokeStyle = "#0066cc";
    ctx.lineWidth = 3;

    ctx.beginPath();

    for (let i = 0; i <= 1000; i++) {

        const x =
            xmin +
            (xmax - xmin) * i / 1000;

        const y = Math.exp(x);

        const px = xPixel(
            x,
            xmin,
            xmax
        );

        const py = yPixel(
            y,
            ymin,
            ymax
        );

        if (i === 0)
            ctx.moveTo(px, py);
        else
            ctx.lineTo(px, py);

    }

    ctx.stroke();


    // --------------------------------------------------------
    // Taylor approximation
    // --------------------------------------------------------

    ctx.strokeStyle = "#cc3333";
    ctx.lineWidth = 3;

    ctx.beginPath();

    for (let i = 0; i <= 1000; i++) {

        const x =
            xmin +
            (xmax - xmin) * i / 1000;

        const y =
            taylor(x, terms);

        const px = xPixel(
            x,
            xmin,
            xmax
        );

        const py = yPixel(
            y,
            ymin,
            ymax
        );

        if (i === 0)
            ctx.moveTo(px, py);
        else
            ctx.lineTo(px, py);

    }

    ctx.stroke();


    // --------------------------------------------------------
    // Legend
    // --------------------------------------------------------

    ctx.font = "16px Arial";

    ctx.fillStyle = "#0066cc";
    ctx.fillText(
        "eˣ",
        30,
        30
    );

    ctx.fillStyle = "#cc3333";
    ctx.fillText(
        "Taylor approximation",
        30,
        55
    );

}


// ------------------------------------------------------------
// Polynomial display
// ------------------------------------------------------------

function updatePolynomial() {

    const terms =
        parseInt(document.getElementById("slider").value);

    document.getElementById("terms").textContent =
        terms;


    let expression = "P(x) = ";

    for (let n = 0; n < terms; n++) {

        if (n === 0) {

            expression += "1";

        } else {

            expression +=
                " + x" +
                (n === 1 ? "" : "^" + n) +
                "/" +
                factorial(n);

        }

    }

    document.getElementById("polynomial").textContent =
        expression;


    draw();

}


// ------------------------------------------------------------
// Slider
// ------------------------------------------------------------

document
    .getElementById("slider")
    .addEventListener(
        "input",
        updatePolynomial
    );


// Initial drawing

resizeCanvas();
updatePolynomial();

</script>

</body>
</html>
"""


# ------------------------------------------------------------
# Write HTML file
# ------------------------------------------------------------

file = Path("taylor_expansion.html")

file.write_text(
    html,
    encoding="utf-8"
)


# ------------------------------------------------------------
# Open in browser
# ------------------------------------------------------------

webbrowser.open(
    file.resolve().as_uri()
)

print("Interactive application opened in your browser.")