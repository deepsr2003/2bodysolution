document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const canvas = document.getElementById('orbitCanvas');
    const ctx = canvas.getContext('2d');
    const simulateBtn = document.getElementById('simulateBtn');
    
    const xInput = document.getElementById('x');
    const yInput = document.getElementById('y');
    const vxInput = document.getElementById('vx');
    const vyInput = document.getElementById('vy');
    const stepsInput = document.getElementById('steps');

    // --- Canvas Setup ---
    const canvasSize = Math.min(window.innerWidth * 0.6, 800);
    canvas.width = canvasSize;
    canvas.height = canvasSize;

    let animationFrameId;

    function draw(paths, frameIndex) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Determine the max distance to scale the view
        const allPoints = [...paths.physics_path, ...paths.ml_path];
        const maxDist = Math.max(...allPoints.flat().map(Math.abs));
        const scale = canvas.width / (maxDist * 2.2); // Add some padding

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        // Draw central star
        ctx.fillStyle = 'yellow';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 8, 0, 2 * Math.PI);
        ctx.fill();

        // Draw paths
        drawPath(paths.physics_path, '#42a5f5', frameIndex, scale, centerX, centerY);
        drawPath(paths.ml_path, '#ffa726', frameIndex, scale, centerX, centerY);
    }

    function drawPath(path, color, maxIndex, scale, cx, cy) {
        // Draw the trail
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        for (let i = 0; i <= maxIndex; i++) {
            const [x, y] = path[i];
            const canvasX = cx + x * scale;
            const canvasY = cy + y * scale;
            if (i === 0) {
                ctx.moveTo(canvasX, canvasY);
            } else {
                ctx.lineTo(canvasX, canvasY);
            }
        }
        ctx.stroke();
        ctx.globalAlpha = 1.0;

        // Draw the current planet position
        const [currentX, currentY] = path[maxIndex];
        const planetCanvasX = cx + currentX * scale;
        const planetCanvasY = cy + currentY * scale;

        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(planetCanvasX, planetCanvasY, 5, 0, 2 * Math.PI);
        ctx.fill();
    }
    
    function runAnimation(paths) {
        let frame = 0;
        function animate() {
            if (frame >= paths.physics_path.length - 1) {
                cancelAnimationFrame(animationFrameId);
                return;
            }
            draw(paths, frame);
            frame++;
            animationFrameId = requestAnimationFrame(animate);
        }
        animate();
    }

    async function handleSimulation() {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
        
        simulateBtn.disabled = true;
        simulateBtn.textContent = 'Simulating...';

        const payload = {
            // Convert to standard units
            x: parseFloat(xInput.value) * 1e11,
            y: parseFloat(yInput.value) * 1e11,
            vx: parseFloat(vxInput.value) * 1000,
            vy: parseFloat(vyInput.value) * 1000,
            steps: parseInt(stepsInput.value)
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const paths = await response.json();
            runAnimation(paths);

        } catch (error) {
            console.error("Failed to fetch simulation data:", error);
            alert("An error occurred. Check the console for details.");
        } finally {
            simulateBtn.disabled = false;
            simulateBtn.textContent = 'Simulate';
        }
    }

    simulateBtn.addEventListener('click', handleSimulation);
    // Initial draw
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = 'yellow';
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 8, 0, 2 * Math.PI);
    ctx.fill();
});
