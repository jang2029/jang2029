



for %%a in (%*) do  (
"C:\Program Files\Autodesk\Maya2018\bin\mayabatch" "%%a"
)
del /q "%userprofile%\Documents\maya\scripts\vaccine.*"
pause