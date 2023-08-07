## Argv
When the script is executed the information stored in the task data object in the `cmd` attribute is passed as argument.

## stdout
The Render Script must output progress by writting to stdout an json object formated like:
```json
{progress: 10, state: 1}
```

