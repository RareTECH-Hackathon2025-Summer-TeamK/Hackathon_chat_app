/*
チャンネルを登録するモーダルの制御
*/

// pagination.jsでチャンネル一覧の表示処理が終了してから読みこまれる
// (チャンネル一覧を表示する処理が終わるまでcreateChannelButtonは存在しないためundefinedになる)
export const initCreateChannelModal = () => {
  const createChannelModal = document.getElementById("create-channel-modal");
  const addPageButtonClose = document.getElementById("add-page-close-button");

  const createChannelButton = document.getElementById("create-channel-button");

  // モーダル表示ボタンが押された時にモーダルを表示する
  createChannelButton.addEventListener("click", () => {
    createChannelModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  addPageButtonClose.addEventListener("click", () => {
    createChannelModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == createChannelModal) {
      createChannelModal.style.display = "none";
    }
  });

  // create-channel-modalが表示されている時に Ctrl/Command + Enterで送信
  // Enterで自動送信を防ぐ
  document.addEventListener("keydown", keydownEvent);

  function keydownEvent(e) {
    const newChannelTitle = document.createChannelForm.channelTitle.value;

    const createChannelModal = document.getElementById("create-channel-modal");
    const createChannelModalStyle = getComputedStyle(
      createChannelModal,
      null
    ).getPropertyValue("display");

    if (e.code === "Enter") {
      e.preventDefault();
    }

    if (
      ((e.ctrlKey && !e.metaKey) || (!e.ctrlKey && e.metaKey)) &&
      e.keyCode == 13
    ) {
      if (e.code === "Enter") {
        if (createChannelModalStyle !== "none") {
          if (newChannelTitle !== "") {
            document.createChannelForm.submit();
          }
        }
      }
    }
  }
};