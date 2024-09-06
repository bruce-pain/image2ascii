document.getElementById('uploadForm').addEventListener('submit', async function(e) {
	e.preventDefault();

	const statusBar = document.getElementById('status-bar');
	const asciiOutput = document.getElementById('asciiOutput');

	const fileInput = document.getElementById('fileInput');
	const formData = new FormData();

	statusBar.innerHTML = "generating..."
	asciiOutput.innerHTML = ""

	if (fileInput.files[0] == null) {
		statusBar.innerHTML = "No file selected!"
	} else {
		formData.append('image_file', fileInput.files[0]);

		try {
			const response = await fetch('/upload', {
				method: 'POST',
				body: formData
			});

			const data = await response.json();
			const result = data["result"];
			statusBar.innerHTML = "done!"
			asciiOutput.innerHTML = result;

		} catch (error) {
			statusBar.innerHTML = "Server Error!"
			console.error('Error:', error);
		}
	}
});
