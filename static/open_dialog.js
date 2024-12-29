const openDBDialogBtn = document.getElementById("openDBDialog");
const closeDBDialogBtn = document.getElementById("closeDBDialog");
const dbdialog = document.getElementById("DBDialog");

openDBDialogBtn.addEventListener("click", () => {
  dbdialog.showModal();
});

closeDBDialogBtn.addEventListener("click", () => {
  dbdialog.close();
});
const openGitDialogBtn = document.getElementById("openGitDialog");
const closeGitDialogBtn = document.getElementById("closeGitDialog");
const gitdialog = document.getElementById("GitDialog");

openGitDialogBtn.addEventListener("click", () => {
  gitdialog.showModal();
});

closeGitDialogBtn.addEventListener("click", () => {
  gitdialog.close();
});
