# LLMCoderSync
Work with ClaudeSync and LLMCoder for easy Claude coding experience.

# Installation

```
pip install flask
```

# Build

```
pip install pyinstaller
pyinstaller LLMCoderSync.spec
pyinstaller LLMCoderServer.spec
```

Run with `./dist/LLMCoderSync` or `python LLMCoderSync.py`.

# Usage

Claude custom instruction sample:

```
使用繁體中文台灣用語回答。
程式內容請完全以英文撰寫，包括顯示訊息及註解。
請精簡扼要回答，除非要求詳細說明。
每次的回覆若有牽涉到修改現有程式碼，必須完全依 instruction.zh-tw.md 中的指示來進行。
所有程式碼請直接由 Project 上傳檔案取得，不要參考最近的修改結果。
```

Run `python LLMCoderServer.py` then open `http://localhost:5000/` in browser.

Run `LLMCoderSync` every time after codes are modified. You can add `claudesync project sync` after it, makes the command be `LLMCoderSync&claudesync project sync`.