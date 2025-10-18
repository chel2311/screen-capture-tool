// ========================================
// 画面キャプチャ編集ツール - モジュール化テンプレート
// ステップ2A: AppStateオブジェクト定義
// ========================================

// このファイルは、index.htmlの<script>タグ内に適用する構造のテンプレートです

(function() {
    'use strict';

    // ========================================
    // 1. DOM要素参照(変更不要)
    // ========================================
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    // ========================================
    // 2. アプリケーション状態管理オブジェクト
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

    // ========================================
    // 3. 定数定義
    // ========================================
    const CONFIG = {
        DB_NAME: 'ScreenCaptureTool',
        DB_VERSION: 1,
        MIN_CANVAS_SIZE: 100,
        DEFAULT_GRID_SIZE: 10,
        DEFAULT_SNAP_TOLERANCE: 8
    };

    // ========================================
    // 4. IndexedDB初期化
    // ========================================
    const request = indexedDB.open(CONFIG.DB_NAME, CONFIG.DB_VERSION);

    request.onerror = () => console.error('IndexedDB初期化エラー');
    request.onsuccess = (event) => {
        AppState.db = event.target.result;
        loadSavedDirectory();
    };
    request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('settings')) {
            db.createObjectStore('settings');
        }
    };

    // ========================================
    // 5. 初期化関数
    // ========================================
    function initCanvas() {
        ctx.fillStyle = '#f8f9fa';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#adb5bd';
        ctx.font = '20px Meiryo';
        ctx.textAlign = 'center';
        ctx.fillText('Win+Shift+S でスクショ → 📋クリップボードボタン', canvas.width / 2, canvas.height / 2 - 10);
        ctx.fillText('または 📁ファイル選択', canvas.width / 2, canvas.height / 2 + 20);
    }

    // ========================================
    // 6. 既存の関数群(ここから下は既存コードをそのまま配置)
    // ========================================

    // 注: 実際の実装では、既存の全関数をここに配置し、
    // 変数参照を AppState.xxx に置換します

    // 例:
    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (AppState.backgroundImage) {  // backgroundImage → AppState.backgroundImage
            ctx.drawImage(AppState.backgroundImage, 0, 0);
        }

        AppState.shapes.forEach(shape => drawShape(shape));  // shapes → AppState.shapes

        if (AppState.selectedShape) {  // selectedShape → AppState.selectedShape
            drawSelectionHandles(AppState.selectedShape);
        }
    }

    // ========================================
    // 7. グローバルAPIの公開(必要な関数のみ)
    // ========================================
    window.AppAPI = {
        // デバッグ用
        getState: () => ({ ...AppState }),

        // 外部から呼び出される可能性がある関数
        selectSaveFolder: selectSaveFolder,
        pasteFromClipboard: pasteFromClipboard,
        copyToClipboard: copyToClipboard,
        quickSave: quickSave,
        // ... 他の公開関数
    };

    // ========================================
    // 8. 初期化実行
    // ========================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCanvas);
    } else {
        initCanvas();
    }

})(); // IIFE終了
