document.getElementById('generate-btn').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input').value;

    if (!userInput) {
        alert('Please enter a description.');
        return;
    }

    const resultContainer = document.getElementById('result-container');
    resultContainer.innerHTML = "Generating YAML...";

    try {
        const response = await fetch('http://localhost:8000/generate_yaml', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: userInput })
        });

        const data = await response.json();

        if (response.ok) {
            resultContainer.innerHTML = `<pre>${data.yaml}</pre>`;
        } else {
            resultContainer.innerHTML = `Error: ${data.detail}`;
        }
    } catch (error) {
        resultContainer.innerHTML = `Error: ${error.message}`;
    }
});
