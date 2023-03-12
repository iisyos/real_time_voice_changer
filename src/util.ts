import axios, { AxiosRequestConfig } from "axios";

export const speak = async(text:string)=>{
    const response = await axios.get("http://localhost:8080/",{params: {text}});
    if (response.data.ok) {
        const file = await uriToFile(response.data.url, 'temp')
        const fileReader = new FileReader()
        fileReader.onload = () => {
          const view = new DataView(fileReader.result)
          const audioBlob = new Blob([view], { type: 'audio/wav' })
          const myURL = window.URL || window.webkitURL
          const audio = new Audio();
          audio.src = myURL.createObjectURL(audioBlob)
          audio.play();
        }
        fileReader.readAsArrayBuffer(file)
      }
}

export const uriToFile:(uri:string, fileName:string)=>Promise<any> = (uri, fileName) =>{
  if (!uri) return Promise.resolve(null);
  return uri.startsWith("data:")
    ? convertDataUriToFile(uri, fileName)
    : loadUriToFile(uri, fileName);
}

function convertDataUriToFile(dataUri, fileName) {
  const byteString = atob(dataUri.split(",")[1]);
  const mimeType = dataUri.match(/(:)([a-z/]+)(;)/)[2];

  const length = byteString.length;
  const content = new Uint8Array(length);
  for (let i = 0; length > i; i++) {
    content[i] = byteString.charCodeAt(i);
  }

  
  return Promise.resolve(
    new File([content], fileName, {
      type: mimeType,
    })
  );
}

async function loadUriToFile(uri, fileName) {
  const response = await axios.get(uri, {
    responseType: "blob",
  });
  return new File([response.data], fileName, {
    type: response.data.type,
  });
}
