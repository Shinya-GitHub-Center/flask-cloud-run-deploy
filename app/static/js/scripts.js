// 秘密コマンド機能:
// - 上上下下左右左右BA で投稿ログイン画面へ遷移
// - 左右左右BA で削除画面へ遷移
(function() {
    // ページ表示時に初期状態にリセット（ブラウザの戻るボタン対応）
    window.addEventListener('pageshow', function() {
        document.body.style.opacity = '1';
    });

    // コマンド1: 上上下下左右左右BA → /post
    const konamiCode = [
        'ArrowUp', 'ArrowUp',
        'ArrowDown', 'ArrowDown',
        'ArrowLeft', 'ArrowRight',
        'ArrowLeft', 'ArrowRight',
        'b', 'a'
    ];

    // コマンド2: 左右左右BA → /delete
    const deleteCode = [
        'ArrowLeft', 'ArrowRight',
        'ArrowLeft', 'ArrowRight',
        'b', 'a'
    ];

    let konamiCodePosition = 0;
    let deleteCodePosition = 0;

    document.addEventListener('keydown', function(e) {
        // 入力されたキーを小文字に変換して比較
        const key = e.key.toLowerCase();

        // コマンド1（コナミコード）のチェック
        const requiredKonamiKey = konamiCode[konamiCodePosition];
        if (key === requiredKonamiKey || e.key === requiredKonamiKey) {
            konamiCodePosition++;

            // コナミコマンドが完成したら投稿ログイン画面へ遷移
            if (konamiCodePosition === konamiCode.length) {
                activateCommand('/post');
                konamiCodePosition = 0;
                deleteCodePosition = 0;
                return;
            }
        } else {
            konamiCodePosition = 0;
        }

        // コマンド2（削除コード）のチェック
        const requiredDeleteKey = deleteCode[deleteCodePosition];
        if (key === requiredDeleteKey || e.key === requiredDeleteKey) {
            deleteCodePosition++;

            // 削除コマンドが完成したら削除画面へ遷移
            if (deleteCodePosition === deleteCode.length) {
                activateCommand('/delete');
                konamiCodePosition = 0;
                deleteCodePosition = 0;
                return;
            }
        } else {
            deleteCodePosition = 0;
        }
    });

    // コマンド実行時の共通処理
    function activateCommand(url) {
        // ちょっとした演出
        document.body.style.transition = 'opacity 0.3s';
        document.body.style.opacity = '0.7';

        // 指定されたページへ遷移
        setTimeout(function() {
            window.location.href = url;
        }, 300);
    }
})();
