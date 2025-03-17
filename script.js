let getCode = document.querySelector(".getCode");
let getApp = document.querySelector(".getApp");

const codeUrl = "python/AbdoDownloader.py"
const appUrl = "python/AbdoDownloader.exe"

getCode.addEventListener("click", () => {download(codeUrl)} );
getApp.addEventListener("click", () => {download(appUrl)} );

function download(url) {
  // رابط الملف EXE الذي تريد تنزيله
  let fileUrl = url;

  // إنشاء عنصر <a> خفي لتنزيل الملف
  let link = document.createElement("a");
  link.href = fileUrl;
  link.download = fileUrl.split("/").pop(); // اسم الملف الذي سيتم تنزيله
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
