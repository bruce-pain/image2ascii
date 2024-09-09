const characterPerLine = document.getElementById('rangeInput');
const characterPerLineValue = document.getElementById('rangeValue');

function updateRangeValue() {
	characterPerLineValue.textContent = characterPerLine.value;
}

characterPerLine.addEventListener("input", updateRangeValue);
updateRangeValue()

document.getElementById('uploadForm').addEventListener('submit', async function(e) {
	e.preventDefault();

	const statusBar = document.getElementById('status-bar');
	const asciiOutput = document.getElementById('asciiOutput');
	const displayArea = document.getElementById('display');

	const fileInput = document.getElementById('fileInput');
	const formData = new FormData();

	const charSetSelect = document.getElementById('charSetSelect');
	const selectedCharSet = charSetSelect.value;

	const addColor = document.getElementById('addColor').checked;

	const screenWidth = window.screen.width
	let dynamicFontSize = 44 / characterPerLine.value;

	statusBar.innerHTML = "generating..."
	displayArea.style.border = "0px";
	asciiOutput.innerHTML = ""

	if (fileInput.files[0] == null) {
		statusBar.innerHTML = "No file selected!"
	} else {
		formData.append('image_file', fileInput.files[0]);

		try {
			const response = await fetch(`/upload?width=${characterPerLine.value}&character_set=${selectedCharSet}&is_colored=${addColor}`, {
				method: 'POST',
				body: formData
			});

			const data = await response.json();
			const result = data["result"];
			statusBar.innerHTML = "done!";
			displayArea.style.border = "1px solid #FCFCFC";
			asciiOutput.style.fontSize = `${dynamicFontSize}rem`

			if (addColor == true) {
				asciiOutput.innerHTML = result;
			} else {
				asciiOutput.textContent = result;
			}

			if (response.status == 400) {
				statusBar.innerHTML = "Unsupported Image Format"
			}


		} catch (error) {
			statusBar.innerHTML = "Server Error!"
			console.error('Error:', error);
		}
	}
});
