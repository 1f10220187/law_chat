// Enterキーで送信（Shift+Enterなら改行）
document.getElementById("message").addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // 改行を防ぐ
        sendMessage(); // メッセージ送信
    }
});

// 入力欄の高さを最大3行まで広く
document.getElementById("message").addEventListener("input",function(){
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight,100)+ "px"
})