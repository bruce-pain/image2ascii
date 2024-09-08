document.getElementById('uploadForm').addEventListener('submit', async function(e) {
	e.preventDefault();

	const statusBar = document.getElementById('status-bar');
	const asciiOutput = document.getElementById('asciiOutput');

	const fileInput = document.getElementById('fileInput');
	const formData = new FormData();

	const charSetSelect = document.getElementById('charSetSelect');
	const selectedCharSet = charSetSelect.value;
	const addColor = document.getElementById('addColor').checked;

	statusBar.innerHTML = "generating..."
	asciiOutput.innerHTML = ""

	if (fileInput.files[0] == null) {
		statusBar.innerHTML = "No file selected!"
	} else {
		formData.append('image_file', fileInput.files[0]);

		try {
			const response = await fetch(`/upload?character_set=${selectedCharSet}&is_colored=${addColor}`, {
				method: 'POST',
				body: formData
			});

			const data = await response.json();
			const result = data["result"];
			statusBar.innerHTML = "done!";

			if (addColor == true) {
				asciiOutput.innerHTML = result;
			} else {
				asciiOutput.textContent = result;
			}


		} catch (error) {
			statusBar.innerHTML = "Server Error!"
			console.error('Error:', error);
		}
	}
});
