Choose your external editor.

On Linux, there are many choices, depending on your distribution and the installed editor. On Ubuntu, the default editor is *gedit*. On LinuxMint, the default editor is *xed*.  
Ubuntu config JSON:  
``{
    "editor": "gedit"
}``
LinuxMint config JSON:  
``{
    "editor": "xed"
}``

On Windows, you can choose *notepad* and the config JSON should look like this:  
``{
    "editor": "%windir%\system32\notepad.exe"
}``

On MacOS, you can choose *TextEdit* and the config JSON should look like this:  
``{
    "editor": "/Applications/TextEdit.app/Contents/MacOS/TextEdit"
}``  
Alternatively, the MacOS command *open* should do the trick (but don't give extra parameters, like in `"open -a TextEdit"`, because of space characters it may not work properly \[I haven't tested this on MacOS\]):  
``{
    "editor": "open"
}``
