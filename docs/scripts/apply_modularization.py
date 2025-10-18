#!/usr/bin/env python3
"""
画面キャプチャ編集ツール - モジュール化自動適用スクリプト

このスクリプトは index-modularized.html に以下の変更を適用します:
1. IIFE (即時実行関数式) で全体を囲む
2. let変数をAppStateオブジェクトに集約
3. 全ての変数参照を AppState.xxx に置換
"""

import re
import sys
from pathlib import Path

# 置換対象の変数リスト (47個)
VARIABLES_TO_REPLACE = [
    'currentTool', 'currentColor', 'isDrawing', 'startX', 'startY',
    'shapes', 'redoStack', 'backgroundImage',
    'snapEnabled', 'snapToGrid', 'snapToObjects', 'gridSize', 'snapTolerance', 'guidelines',
    'stylePresets', 'currentPresetIndex',
    'zoom', 'savedCount', 'pendingTextPosition', 'selectedShape',
    'isDragging', 'isResizing', 'isRotating', 'resizeHandle',
    'dragOffsetX', 'dragOffsetY', 'saveDirectoryHandle',
    'polylinePoints', 'freehandPoints', 'isPolylineActive',
    'doubleClickTimer', 'lastClickTime', 'trimMode', 'trimRect',
    'isShiftPressed', 'dragStartX', 'dragStartY',
    'mosaicSize', 'blurStrength', 'imageStamps', 'imageCache', 'db'
]

def read_file(filepath):
    """ファイルを読み込み"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """ファイルに書き込み"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def add_iife_wrapper(content):
    """IIFE構造を追加"""
    # <script>タグの位置を検索
    script_start = content.find('<script>')
    if script_start == -1:
        print("❌ <script>タグが見つかりません")
        return content

    # </script>タグの位置を検索
    script_end = content.rfind('</script>')
    if script_end == -1:
        print("❌ </script>タグが見つかりません")
        return content

    # IIFEの開始部分を挿入
    iife_start = """<script>
    // ========================================
    // モジュール化: IIFE (即時実行関数式)
    // ========================================
    (function() {
        'use strict';

        """

    # IIFEの終了部分を挿入
    iife_end = """
    })(); // IIFE終了
    </script>"""

    # <script>と</script>の間のコンテンツを抽出
    script_content = content[script_start + 8:script_end]

    # 新しいコンテンツを構築
    new_content = (
        content[:script_start] +
        iife_start +
        script_content.lstrip() +
        iife_end +
        content[script_end + 9:]
    )

    return new_content

def convert_variables_to_appstate(content):
    """let変数宣言をAppStateオブジェクトに変換"""

    # AppStateオブジェクトの定義を作成
    appstate_def = """
        // ========================================
        // アプリケーション状態管理オブジェクト
        // ========================================
        const AppState = {
            // 描画ツール関連
            currentTool: null,
            currentColor: '#FF0000',

            // 描画状態
            isDrawing: false,
            startX: 0,
            startY: 0,

            // 図形管理
            shapes: [],
            redoStack: [],
            backgroundImage: null,

            // スナップ機能
            snapEnabled: false,
            snapToGrid: false,
            snapToObjects: false,
            gridSize: 10,
            snapTolerance: 8,
            guidelines: [],

            // スタイルプリセット
            stylePresets: [
                { name: '赤・太線', color: '#FF0000', lineWidth: 5, opacity: 0 },
                { name: '青・細線', color: '#0000FF', lineWidth: 2, opacity: 0 },
                { name: '黄・半透明', color: '#FFFF00', lineWidth: 3, opacity: 50 }
            ],
            currentPresetIndex: -1,

            // UI状態
            zoom: 1.0,
            savedCount: 0,

            // 編集状態
            pendingTextPosition: null,
            selectedShape: null,
            isDragging: false,
            isResizing: false,
            isRotating: false,
            resizeHandle: null,
            dragOffsetX: 0,
            dragOffsetY: 0,

            // ファイル操作
            saveDirectoryHandle: null,

            // ポリライン・フリーハンド
            polylinePoints: [],
            freehandPoints: [],
            isPolylineActive: false,

            // その他
            doubleClickTimer: null,
            lastClickTime: 0,
            trimMode: false,
            trimRect: { x: 0, y: 0, w: 0, h: 0 },
            isShiftPressed: false,
            dragStartX: 0,
            dragStartY: 0,
            mosaicSize: 10,
            blurStrength: 10,
            imageStamps: [],
            imageCache: new Map(),

            // IndexedDB
            db: null
        };

        """

    # 既存のlet変数宣言を削除
    # パターン: let variableName = ... まで
    patterns_to_remove = []
    for var in VARIABLES_TO_REPLACE:
        # 単純な宣言 (例: let currentTool = null;)
        pattern1 = rf'\s*let\s+{var}\s*=\s*[^;]+;'
        patterns_to_remove.append(pattern1)

        # 複数行にわたる宣言 (例: let stylePresets = [...];)
        pattern2 = rf'\s*let\s+{var}\s*=\s*\[[\s\S]*?\];'
        patterns_to_remove.append(pattern2)

    modified_content = content
    for pattern in patterns_to_remove:
        modified_content = re.sub(pattern, '', modified_content, flags=re.MULTILINE)

    # AppStateオブジェクトを挿入 (const ctx = ... の後)
    insertion_point = modified_content.find("const ctx = canvas.getContext('2d'")
    if insertion_point != -1:
        # 次の行の終わりを見つける
        next_line_end = modified_content.find(';', insertion_point) + 1
        modified_content = (
            modified_content[:next_line_end] +
            appstate_def +
            modified_content[next_line_end:]
        )

    return modified_content

def replace_variable_references(content):
    """変数参照を AppState.xxx に置換"""

    # 各変数について置換
    for var in VARIABLES_TO_REPLACE:
        # パターン1: 代入 (例: currentTool = 'select')
        pattern1 = rf'\b{var}\s*='
        replacement1 = f'AppState.{var} ='
        content = re.sub(pattern1, replacement1, content)

        # パターン2: 参照 (例: if (currentTool === 'select'))
        # ただし、AppState.xxx は除外
        pattern2 = rf'(?<!AppState\.)\b{var}\b(?!\s*:)'
        replacement2 = f'AppState.{var}'
        content = re.sub(pattern2, replacement2, content)

    return content

def main():
    """メイン処理"""
    input_file = Path('index-modularized.html')
    output_file = Path('index-modularized.html')
    backup_file = Path('index-modularized.html.backup')

    if not input_file.exists():
        print(f"❌ エラー: {input_file} が見つかりません")
        return 1

    print(f"📖 読み込み: {input_file}")
    content = read_file(input_file)

    # バックアップ作成
    print(f"💾 バックアップ作成: {backup_file}")
    write_file(backup_file, content)

    # ステップ1: IIFE構造を追加
    print("🔧 ステップ1: IIFE構造を追加")
    content = add_iife_wrapper(content)

    # ステップ2: let変数をAppStateに変換
    print("🔧 ステップ2: let変数をAppStateオブジェクトに変換")
    content = convert_variables_to_appstate(content)

    # ステップ3: 変数参照を置換
    print("🔧 ステップ3: 変数参照を AppState.xxx に置換")
    content = replace_variable_references(content)

    # 出力
    print(f"💾 書き込み: {output_file}")
    write_file(output_file, content)

    print("\n✅ モジュール化適用完了!")
    print(f"\n📋 確認事項:")
    print(f"1. ブラウザで {output_file} を開いて動作確認")
    print(f"2. 問題があれば {backup_file} から復元可能")
    print(f"3. 動作確認後、index.html と置き換え")

    return 0

if __name__ == '__main__':
    sys.exit(main())
