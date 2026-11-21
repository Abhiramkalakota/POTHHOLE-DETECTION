const input=document.getElementById("imageInput"),drop=document.getElementById("dropzone"),preview=document.getElementById("preview"),img=document.getElementById("previewImg"),nameEl=document.getElementById("previewName"),remove=document.getElementById("remove"),form=document.getElementById("form");
function show(file){if(!file)return;if(!["image/jpeg","image/png","image/webp"].includes(file.type)){alert("Choose a JPG, PNG or WEBP image.");input.value="";return}if(file.size>12*1024*1024){alert("Maximum image size is 12 MB.");input.value="";return}img.src=URL.createObjectURL(file);nameEl.textContent=file.name;preview.hidden=false;drop.hidden=true}
input?.addEventListener("change",()=>show(input.files[0]));remove?.addEventListener("click",()=>{input.value="";img.src="";preview.hidden=true;drop.hidden=false});
["dragenter","dragover"].forEach(e=>drop?.addEventListener(e,x=>{x.preventDefault();drop.classList.add("drag")}));
["dragleave","drop"].forEach(e=>drop?.addEventListener(e,x=>{x.preventDefault();drop.classList.remove("drag")}));
drop?.addEventListener("drop",e=>{const f=e.dataTransfer.files[0];if(f){const dt=new DataTransfer();dt.items.add(f);input.files=dt.files;show(f)}});
form?.addEventListener("submit",()=>{const b=form.querySelector("button[type=submit]");if(b){b.disabled=true;b.firstChild.textContent="Analysing..."}});
