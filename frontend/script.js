async function sendImage() {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
    alert("Выберите файл!");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("result").innerText =
    "Результат: " + JSON.stringify(data);
}
