const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

const numLines = 200;
const minLength = 10;
const maxLength = 50;
const minSpeed = 1;
const maxSpeed = 5;

const lines = [];

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function distance(x1, y1, x2, y2) {
  const xDist = x2 - x1;
  const yDist = y2 - y1;
  return Math.sqrt(Math.pow(xDist, 2) + Math.pow(yDist, 2));
}

function Line(x, y, dx, dy, length, speed) {
  this.x = x;
  this.y = y;
  this.dx = dx;
  this.dy = dy;
  this.length = length;
  this.speed = speed;

  this.draw = function() {
    ctx.beginPath();
    ctx.moveTo(this.x, this.y);
    ctx.lineTo(this.x + this.dx * this.length, this.y + this.dy * this.length);
    ctx.strokeStyle = 'white';
    ctx.stroke();
  }

  this.update = function() {
    if (this.x >= canvas.width || this.x <= 0) {
      this.dx = -this.dx;
    }
    if (this.y >= canvas.height || this.y <= 0) {
      this.dy = -this.dy;
    }

    this.x += this.dx * this.speed;
    this.y += this.dy * this.speed;

    this.draw();
  }

  this.isConnected = function(otherLine) {
    const dist = distance(this.x, this.y, otherLine.x, otherLine.y);
    return dist <= (this.length + otherLine.length) / 2;
  }
}

function createLines() {
  for (let i = 0; i < numLines; i++) {
    const x = random(0, canvas.width);
    const y = random(0, canvas.height);
    const dx = random(-1, 1);
    const dy = random(-1, 1);
    const length = random(minLength, maxLength);
    const speed = random(minSpeed, maxSpeed);
    lines.push(new Line(x, y, dx, dy, length, speed));
  }
}

function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < lines.length; i++) {
    lines[i].update();

    for (let j = i + 1; j < lines.length; j++) {
      if (lines[i].isConnected(lines[j])) {
        ctx.beginPath();
        ctx.moveTo(lines[i].x, lines[i].y);
        ctx.lineTo(lines[j].x, lines[j].y);
        ctx.strokeStyle = 'white';
        ctx.stroke();
      }
    }
  }
}

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

createLines();
animate();

window.addEventListener('resize', function() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  createLines();
});
