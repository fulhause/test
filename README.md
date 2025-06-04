# Pythonサンプル集

このリポジトリには、シンプルなシリンダーのモデル(`cylinder.py`)と、非常に簡易的なSLMPメッセージの実装(`slmp.py`)が含まれています。Pythonの基礎を学び始めたばかりの方でも扱いやすいコードになっています。

## 必要なもの

- Python 3.x
- [pytest](https://docs.pytest.org/)（テストを実行する場合）

## インストール

以下のコマンドでテスト実行に必要なパッケージをインストールします。

```bash
pip install pytest
```

## 使い方

### シリンダーモデル `cylinder.py`

2ポジションまたは3ポジションのシリンダーを模したクラスです。以下のように使います。

```python
from cylinder import Cylinder

cyl = Cylinder(mode="2-position")
print(cyl.position)  # 初期状態は"retracted"

cyl.extend()
print(cyl.position)  # "extended"に変化
```

3ポジションモードでは `intermediate()` メソッドも利用できます。

### SLMPメッセージ `slmp.py`

実際のSLMPプロトコルを簡略化したサンプルです。`encode()` と `decode()` でバイト列の変換を行います。

```python
from slmp import SLMPMessage

msg = SLMPMessage("CMD", 100, b"data")
encoded = msg.encode()
decoded = SLMPMessage.decode(encoded)
```

## テストの実行

依存パッケージをインストールした後、次のコマンドでテストを実行できます。

```bash
pytest
```

テストではシリンダークラスの状態遷移や、SLMPメッセージのエンコード/デコードを確認しています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
