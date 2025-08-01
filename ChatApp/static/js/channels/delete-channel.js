/*
チャンネルを削除するモーダルの制御
*/

export const initDeleteChannelModal = () => {
  const deletePageButtonClose = document.getElementById(
    "delete-page-close-button"
  );

  const deleteChannelModal = document.getElementById("delete-channel-modal");

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  deletePageButtonClose.addEventListener("click", () => {
    deleteChannelModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == deleteChannelModal) {
      deleteChannelModal.style.display = "none";
    }
  });
};