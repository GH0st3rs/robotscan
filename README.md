# robotscan

Python addon for dirsearch
```bash
usage: robotscan.py [-h] [-u URL] [-w WORDLIST] [-e EXTENSIONS]
                    [-x EXCLUDESTATUS] [-a ...]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL target
  -w WORDLIST, --wordlist WORDLIST
                        Dictionary
  -e EXTENSIONS, --extensions EXTENSIONS
                        Extension list separated by comma (example: php,asp)
  -x EXCLUDESTATUS, --excludestatus EXCLUDESTATUS
                        Exclude status code, separated by comma (example:
                        301,500)
  -a ..., --args ...    Other args for dirsearch. Use quotes for parameters
                        (example: "--timeout=0 -t 20")
```
