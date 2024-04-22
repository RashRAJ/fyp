let timer = null;
let elapsedSeconds = 0;

function updateTimerDisplay() {
    document.getElementById('timerDisplay').textContent = formatTime(elapsedSeconds);
}

function formatTime(seconds) {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
}

function startTimer() {
    if (timer === null) {
        timer = setInterval(() => {
            elapsedSeconds++;
            updateTimerDisplay();
        }, 1000);
    }
}

function pauseTimer() {
    if (timer !== null) {
        clearInterval(timer);
        timer = null;
    }
}

function stopTimer() {
    pauseTimer();
    elapsedSeconds = 0;
    updateTimerDisplay();
}

function controlCamera(command) {
    const videoFeed = document.getElementById('videoFeed');
    fetch('/control_camera', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: command })
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.state) {
                videoFeed.style.display = 'block';
                videoFeed.src = videoURL;
                startTimer();
            } else {
                videoFeed.style.display = 'none';
                videoFeed.src = ""; 
                stopTimer();
            }
        }
    });
}

function loadDrowsinessLevel() {
    setInterval(() => {
        fetch('/drowsiness_level')
        .then(response => response.json())
        .then(data => {
            document.getElementById('drowsinessLevel').textContent = data.level;
        })
        .catch(error => console.error('Error fetching drowsiness level:', error));
    }, 10000); // Update every second
}

document.addEventListener('DOMContentLoaded', function () {
    loadDrowsinessLevel();
});