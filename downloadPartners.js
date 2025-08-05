fetch("https://gyakorlat.vik.bme.hu/api/Public/GetRegularPartners?department=1")
  .then(res => {
    if (!res.ok) throw new Error(res.statusText);
    return res.blob();              // ① grab raw response as a Blob
  })
  .then(blob => {
    // ② create a temporary object URL for the blob
    const url = window.URL.createObjectURL(blob);

    // ③ create a hidden <a> element and force a download
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "partners.json";    // ← the default filename

    document.body.appendChild(a);
    a.click();                       // ④ trigger the download
    document.body.removeChild(a);

    // ⑤ cleanup the object URL
    window.URL.revokeObjectURL(url);
  })
  .catch(err => console.error("Download failed:", err));
