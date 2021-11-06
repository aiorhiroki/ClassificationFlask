function previewFile(file) {
  // プレビュー画像を追加する要素
  const preview = document.getElementById('preview');

  // FileReaderオブジェクトを作成
  const reader = new FileReader();

  // ファイルが読み込まれたときに実行する
  reader.onload = function (e) {
    const imageUrl = e.target.result; // 画像のURLはevent.target.resultで呼び出せる
    const img = document.createElement("img"); // img要素を作成
    img.src = imageUrl; // 画像のURLをimg要素にセット

    if(preview.getElementsByTagName('img').length > 0){
        preview.replaceChild(img, preview.lastChild);
    }else{
        preview.appendChild(img);
    }
  }

  // ファイルを読み込む
  reader.readAsDataURL(file);
}


// <input>でファイルが選択されたときの処理
const fileInput = document.getElementById('file');
const handleFileSelect = () => {
    const file = fileInput.files[0];
    previewFile(file);
    // フォームデータを作成
    const formData = new FormData();
    // avatarというフィールド名でファイルを追加
    formData.append("img_file", file);
    // アップロード
    fetch("http://localhost:5000/send", { method: "POST", body: formData })
    .then((res)=>{
    return( res.json() );
    })
    .then((json)=>{
        result_div = document.getElementById('result');

        const result_p = document.createElement("p");
        result_p.innerHTML = "<span style='font-size: 20px; font-weight: bold'> AI診断結果 ： " + json["pred_cls"] + "</span><br><br>";
        for (let i = 0; i < json["probs"].length; i++) {
            result_p.innerHTML += json["class_names"][i] + "の確率 ： " + json["probs"][i] + "%<br>";
        }

        if(result_div.getElementsByTagName('p').length > 0){
            result_div.replaceChild(result_p, result_div.lastChild);
        }else{
            result_div.appendChild(result_p);
        }
        console.log(json)
    });
}
fileInput.addEventListener('change', handleFileSelect);