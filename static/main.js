document.getElementById('uploadForm').addEventListener('submit', async function(e) {
	e.preventDefault();

	const fileInput = document.getElementById('fileInput');
	const formData = new FormData();
	formData.append('image_file', fileInput.files[0]);

	try {
		const response = await fetch('/upload', {
			method: 'POST',
			body: formData
		});

		const data = await response.json();
		const asciiOutput = document.getElementById('asciiOutput');
		asciiOutput.textContent = data["result"];
	} catch (error) {
		console.error('Error:', error);
	}
});
