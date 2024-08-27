# LLMCoderSync

Work with [ClaudeSync](https://github.com/jahwag/ClaudeSync) and [LLMCoder](https://github.com/ChrisTorng/LLMCoder) for easy Claude project coding experience.

![](images/LLMCoderServer.png)
The WebUI shows all files, excludes `.gitignore` and `.claudesync`. You choose which files to be synced with or without line number. Then press `Sync All` button to sync to target Claude project, with the help from [ClaudeSync](https://github.com/jahwag/ClaudeSync).

You can modify your `SyncCommand` file for your sync tools, not limited to `LLMCoderSync` and `ClaudeSync`.

You can easily choose the currently working files to sync, save more tokens from Claude usage for longer conversations.

The line number options is used for [LLMCoder](https://github.com/ChrisTorng/LLMCoder), it uses code with line numbers and ask LLM to use specific Markdown diff output, then apply the Markdown diff to the source code. It helps you sync the output of LLM back to your source code with only one paste action, and save the output tokens for only diff part.

# Build & Usage

```
pip install flask pyinstaller
pyinstaller LLMCoderSync.spec
pyinstaller LLMCoderServer.spec
```

Run `/path/to/LLMCoderSync/dist/LLMCoderServer/LLMCoderServer` from your project dir `current`, open http://localhost:5000 for WebUI. Check all the codes that needs to be synced. If your are not using [LLMCoder](https://github.com/ChrisTorng/LLMCoder), you should uncheck all line numbers.

Run `/path/to/LLMCoderSync/dist/LLMCoderSync` to copy `current` dir into another `current.sync` dir, for all files synced, with specific line numberred files to sync to LLM (I'm using Claude).

While `claudesync project select`, select the project dir to `current.sync`.

Then you can click `Sync All` button to run `SyncCommand`, make sure the sync is working.

# Working with [LLMCoder](https://github.com/ChrisTorng/LLMCoder)

Copy `SyncCommand` or `SyncCommand.cmd` (Windows) into your project dir. Add `.claudeignore` file with content:
```
.*
LICENSE
SyncCommand*
```
Open WebUI, unckech anything that should not be synced or adding line numbers, then `Sync All`.

Set Claude's Project custom instructions with then content of `instructions\markdown.instruction.en.md` after your own specific instructions.

Ask Claude to modify code, it should follow the instructions, output Markdown diff.

On [LLMCoder online page](https://christorng.github.io/LLMCoder/), paste the source code, then paste the Markdown, it will apply the changes to the source and copy to clipboard automatically. You can paste back to overwrite to your source.

Click `Sync All` button on WebUI after each time the codes are modified, ready for the next prompt to reference the latest code with line numbers.

# Future plan


* **Integrate LLMCoder into LLMCoderSync WebUI**

  So you can select a code file, paste Markdown, then it writes the result directly into the source, saves you more time.
  
* **Apply multiple files at once**

  Ask LLM to add file names in Markdown diff, then it can modify them all at once.

* **Fix line number errors automatically**

  Sometimes the LLM output wrong first/last line number. It tries to look for correct line number and apply without manual fix.

* **Auto Sync**

  Detect file changes, then sync automatically.

* **Browser extension**

  Integrate with Claude.ai website, saves even more times copy&paste between IDE and LLMCoderSync.