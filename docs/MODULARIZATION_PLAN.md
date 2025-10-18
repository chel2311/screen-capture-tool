# モジュール化実装計画

## 📋 概要

screen-capture-tool の段階的モジュール化を実施します。
単一HTMLファイル運用を維持しながら、コード品質を向上させます。

## ✅ 完了したステップ

### ステップ1: バックアップとGit初期化 ✅
- **実施日**: 2025-10-18
- **成果物**:
  - バックアップファイル: `index.html.backup.20251018_132508`
  - Gitコミット: `f189e67` (ベースライン: モジュール化前の安定版)

- **確認コマンド**:
  ```bash
  git log --oneline
  ls -lh index.html.backup*
  ```

## 🔄 進行中のステップ

### ステップ2: AppStateオブジェクト作成 (進行中)

#### 目的
50個以上のグローバル変数を1つのAppStateオブジェクトに集約

#### 作業内容

##### ステップ2A: テンプレート作成 ✅
- `modularization_template.js` 作成完了
- AppStateオブジェクトの構造定義
- IIFE(即時実行関数式)パターンの適用

##### ステップ2B: 実装 (次回)
1. `<script>`タグ直後にIIFE開始を追加
2. 既存の全let変数をAppStateオブジェクトに移行
3. 全関数内の変数参照を`AppState.xxx`に置換
4. `</script>`直前にIIFE終了を追加

#### 置換対象の変数一覧

| 変数名 | 型 | 用途 |
|--------|-----|------|
| currentTool | string/null | 現在選択中のツール |
| currentColor | string | 現在の描画色 |
| isDrawing | boolean | 描画中フラグ |
| startX, startY | number | 描画開始座標 |
| shapes | array | 描画図形の配列 |
| redoStack | array | Redo用スタック |
| backgroundImage | Image/null | 背景画像 |
| snapEnabled | boolean | スナップ機能有効化 |
| snapToGrid | boolean | グリッドスナップ |
| snapToObjects | boolean | オブジェクトスナップ |
| gridSize | number | グリッドサイズ |
| snapTolerance | number | スナップ許容範囲 |
| guidelines | array | ガイドライン配列 |
| stylePresets | array | スタイルプリセット |
| currentPresetIndex | number | 現在のプリセットインデックス |
| zoom | number | ズーム倍率 |
| savedCount | number | 保存回数 |
| pendingTextPosition | object/null | テキスト入力待機位置 |
| selectedShape | object/null | 選択中の図形 |
| isDragging | boolean | ドラッグ中フラグ |
| isResizing | boolean | リサイズ中フラグ |
| isRotating | boolean | 回転中フラグ |
| resizeHandle | string/null | リサイズハンドル |
| dragOffsetX, dragOffsetY | number | ドラッグオフセット |
| saveDirectoryHandle | FileSystemDirectoryHandle/null | 保存先ディレクトリ |
| polylinePoints | array | ポリライン座標配列 |
| freehandPoints | array | フリーハンド座標配列 |
| isPolylineActive | boolean | ポリライン描画中フラグ |
| doubleClickTimer | number/null | ダブルクリックタイマー |
| lastClickTime | number | 最終クリック時刻 |
| trimMode | boolean | トリミングモード |
| trimRect | object | トリミング範囲 |
| isShiftPressed | boolean | Shiftキー押下状態 |
| dragStartX, dragStartY | number | ドラッグ開始座標 |
| mosaicSize | number | モザイクサイズ |
| blurStrength | number | ぼかし強度 |
| imageStamps | array | 画像スタンプ配列 |
| imageCache | Map | 画像キャッシュ |
| db | IDBDatabase/null | IndexedDBインスタンス |

**合計**: 47個の変数

#### 置換パターン

```javascript
// Before (現状)
let currentTool = null;
function selectTool(tool) {
    currentTool = tool;
}

// After (ステップ2B実施後)
const AppState = {
    currentTool: null,
    // ... 他の変数
};
function selectTool(tool) {
    AppState.currentTool = tool;
}
```

#### リスク管理

**リスク**: 一度に全ての置換を行うと、見落としによるバグのリスクが高い

**対策**:
1. バックアップ済み(復元可能)
2. Git管理(コミット単位で巻き戻し可能)
3. ブラウザで動作確認しながら進める

#### 実装手順(次回実行)

```bash
# 1. 作業ブランチ作成(推奨)
git checkout -b feature/app-state-object

# 2. index.htmlを編集
#    - <script>直後にIIFE開始を追加
#    - let変数宣言をAppStateオブジェクトに変換
#    - 全関数内の変数参照を置換(sed/正規表現使用)
#    - </script>直前にIIFE終了を追加

# 3. ブラウザで動作確認
#    - ファイル読み込み
#    - 描画ツール動作
#    - 保存機能
#    - クリップボード機能

# 4. 動作確認後、コミット
git add index.html
git commit -m "ステップ2B完了: AppStateオブジェクトへの変数集約"

# 5. メインブランチにマージ
git checkout master
git merge feature/app-state-object
```

## 📅 今後のステップ

### ステップ3: CanvasModule作成 (予定)
- Canvas操作をCanvasModuleオブジェクトにカプセル化
- redrawCanvas, drawSelectionHandles等を移動

### ステップ4: DrawingModule作成 (予定)
- 描画処理をDrawingModuleにカプセル化
- drawShape, drawRect, drawCircle等を移動

### ステップ5: EventHandlers作成 (予定)
- イベントハンドラをEventHandlersオブジェクトに整理
- mousedown, mousemove, mouseup等を移動

### ステップ6: 最終確認とドキュメント更新 (予定)
- 全機能の動作確認
- README.md更新
- コードレビュー

## 📊 進捗状況

- [x] ステップ1: バックアップとGit初期化
- [x] ステップ2A: AppStateテンプレート作成
- [x] ステップ2B: AppState実装
- [x] **ステップ2 完了！** (2025-10-18)
- [ ] ステップ3: CanvasModule (将来の拡張として保留)
- [ ] ステップ4: DrawingModule (将来の拡張として保留)
- [ ] ステップ5: EventHandlers (将来の拡張として保留)
- [ ] ステップ6: 最終確認 (不要 - ステップ2で完了)

**進捗率**: 100% (ステップ2まで完了、以降は将来の拡張として保留)

## 🔗 関連ファイル

- `index.html` - メインファイル
- `index.html.backup.20251018_132508` - バックアップ
- `modularization_template.js` - モジュール化テンプレート
- `MODULARIZATION_PLAN.md` - 本ドキュメント
- `README.md` - プロジェクトドキュメント

## 📝 メモ

- 単一HTMLファイル運用を維持
- プロトタイプとしての利便性を保つ
- 段階的改善により安全性を確保

---

## ✅ 完了報告 (2025-10-18)

### 実装完了した機能

1. **IIFE (即時実行関数式)によるスコープ分離**
   - グローバルスコープの汚染を防止
   - 変数の意図しない上書きを防止

2. **AppStateオブジェクトによる状態管理**
   - 47個のグローバル変数を1つのオブジェクトに集約
   - 状態の可視化と管理性向上

3. **グローバルAPI公開機構**
   - HTML onclick属性から必要な関数にアクセス可能
   - 40個の関数を明示的に公開

4. **バグ修正**
   - モザイク/ぼかしのマイナス方向ドラッグ時の座標ずれを修正

### Git コミット履歴

```
3ce2f23 本番適用: index.htmlをモジュール化版で置き換え
0c701d8 修正: モザイク/ぼかしのマイナス方向ドラッグ時の座標ずれを修正
d222a82 修正: HTML属性とJavaScriptのID参照を元に戻す
5e0e305 修正: Pythonスクリプトの誤置換を修正
4ea9737 修正: Lucide初期化タイミングとスクリプト構造の最適化
4792b53 修正: IIFE構造とグローバルAPI公開を追加
aadf18e 修正: 構文エラーを2箇所修正
9116c03 ステップ2B完了: AppStateオブジェクト実装(自動化)
```

### 成果物

- **index.html**: モジュール化完了版（本番適用済み）
- **index-modularized.html**: モジュール化版（検証用として残存）
- **apply_modularization.py**: 自動置換スクリプト
- **modularization_template.js**: 実装テンプレート
- **.gitignore**: Gitバージョン管理設定

### 動作確認

✅ 全機能正常動作
✅ コンソールエラーなし
✅ モザイク/ぼかし全方向対応
✅ 描画ツール全般動作確認済み
✅ 保存機能動作確認済み

### 今後の拡張案

ステップ3以降（CanvasModule、DrawingModule、EventHandlers）は将来の拡張として保留。
現時点では、AppStateオブジェクトによる状態管理のモジュール化で十分な改善効果を得られた。

---

## 📊 Gemini CLIによるコードレビュー結果 (2025-10-18)

Claude Codeとは異なる視点からの技術的評価を実施しました。

### 技術的評価サマリー

| 評価項目 | 現状の課題 | 推奨される改善 |
|---------|-----------|--------------|
| **設計パターン** | 4000行超で単一ファイル構成は限界 | MVC/MVVM導入が必須 |
| **テスタビリティ** | DOM密結合でテスト困難 | テスト可能な構造への変換 |
| **拡張性** | 機能追加のたびに複数箇所修正 | プラグイン機構の導入 |
| **状態管理** | 50個以上のグローバル変数（今回集約済み✅） | Redux/MobX等の本格導入検討 |
| **TypeScript化** | 動的なshapeオブジェクトの型不明 | 型定義で劇的改善が見込める |
| **Web Worker** | モザイク/ぼかしがメインスレッドをブロック | オフロードで応答性向上 |
| **モダン実装** | 古典的なDOM操作 | React/Vueへの移植を検討 |

### 段階的改善計画（Gemini推奨）

#### **フェーズ1: 基盤整備（短期・最優先）** ⭐

1. **コード分離**
   - `index.html`からCSS/JavaScriptを別ファイルに分離
   - `style.css`, `main.js` として独立

2. **Vite導入**
   - 開発サーバー、モジュールバンドル、TypeScript即時サポート
   - モダン開発環境の構築

3. **状態の集約** ✅ **完了**
   - 全グローバル変数を単一stateオブジェクトに集約
   - 状態変更を専用関数経由で実施

#### **フェーズ2: 品質と安定性向上（中期）**

1. **TypeScript導入**
   - `main.js` → `main.ts` にリネーム
   - `Shape`型と`state`型の定義から開始

2. **純粋関数の分離とテスト**
   - 副作用のない計算ロジックを切り出し
   - Vitestでユニットテスト作成

#### **フェーズ3: パフォーマンスと拡張性改善（長期）**

1. **Web Worker導入**
   - モザイク/ぼかし処理をオフロード
   - UIの応答性を改善

2. **ツールのクラス化（プラグイン化）**
   - 各描画ツールを共通インターフェースのクラスとして再設計
   - ツール追加・修正を容易に

### 最終的な選択肢: モダンフレームワークへの移行

長期的に大規模な機能追加が見込まれる場合、**React（またはVue）を用いた完全な再実装**が最も合理的。

**メリット**:
- 長期的なメンテナンス性の飛躍的向上
- 開発生産性の向上
- 安全性の向上

**進め方**:
- 既存コードを「動く仕様書」として参考にする
- コンポーネントベースで再設計
- Canvas描画ライブラリ（例: React-Konva）を活用

### Geminiの結論

**現状のコードは機能豊富だが、技術的負債が大きく、これ以上の拡張は困難。**

**推奨する最初のステップ**:
「**フェーズ1: 基盤整備**」に着手すること。
Viteを導入し、ファイルを分割するだけでも開発体験は大きく改善される。
その上で、TypeScript化を進めるか、再実装に踏み切るかの判断を下すのが良い。

---
