const closeDBDialogBtn = document.getElementById("closeDBDialog");
const dbdialog = document.getElementById("DBDialog");

closeDBDialogBtn.addEventListener("click", () => {
  dbdialog.close();
});

const closeGitDialogBtn = document.getElementById("closeGitDialog");
const gitdialog = document.getElementById("GitDialog");

closeGitDialogBtn.addEventListener("click", () => {
  gitdialog.close();
});
