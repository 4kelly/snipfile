A CLI for templating files into other files. No external dependencies required.

- [Usage](#usage)
    - [Example](#example)
    - [Template Syntax](#template-syntax)
- [Disclaimers](#disclaimers)
    - [TODOs](#todos)

**Motivation**

snipfile was designed to help you **stop** copy-&-pasting **un-tested** code snippets into your professional work.

Fix your:

- [x] Outdated examples
- [x] Broken demos
- [x] Busted blog posts
- [x] Stale documentation
- [x] Un-tested slide decks
- [ ] What other use-cases are there?

You can achieve testable code snippets by _separating_ your code from your content.

```bash
pip install snipfile
```

## Usage

```bash
snipfile --help
```

### Example

1. Embed the [template syntax]() within a file.

   - `posts/thing.md`

       ```markdown
       Checkout this code snippet!
    
           ```python
           --8<-- code/foo.py  
           ```
       ```
   - The filepath is relative where you run `snipfile` (usually the root of your project).


2. Make sure the file to-be-templated exists. This file can be unit-tested as normal.
   - `code/foo.py`

       ```python
       class Foo:
           def __init__(self, bar: int) -> None:
               self.bar = bar
       ```

3. Run `snipfile` anytime your code changes so that your documentation is always up-to-date.
    - A CLI tool `snipfile` is installed automatically.

      ```bash
      snipfile --input-dir=posts --output-dir=site --pattern=**/*.md
      ```

4. Profit

   - `site/posts/thing.md`

      ```markdown
      Checkout this code snippet!
        
          ```python
          class Foo:
              def __init__(self, bar: int) -> None:
                  self.bar = bar
          ```
      ```

### Template Syntax

The syntax is a space delimited set of arguments.

`--8<-- <filepath> <startline> <endline>`

- `--8<--` The template syntax, used to identify which line you want to replace.
- `<filepath>`: (str) a filepath relative to the call to `snipfile`. This is the file you want to inject into the document.
- `<startline> <endline>`: Optional (int) these integers mark the start and/or end line to read from the snipped file provided in the `<filepath>`.

Some examples:

- Inject lines 2-3 from filename.txt.

  - `--8<-- filename.txt 2 3`

- Inject all but the first line from filename.md
  - `--8<-- filename.md 1`

- Inject all by the last line from filename.csv
  - `--8<-- filename.csv -1`
  
Notes:

- Extra spaces between the arguments are ignored. 

## Disclaimers

- This repo was mostly created to help practice some software design patterns for enabling unit testing the file system without mocks. But I'm happy to respond to bug/feature requests.
- Template syntax (`--8<--`) taken from [pymdown-extensions](https://github.com/facelessuser/pymdown-extensions).

### TODOs

- Configurable base path.
- Finish support for templating certain line ranges.
- Preserve whitespace so that templating can preserve indented semantics (lists, etc.).
- Expose Python API as well as a CLI.
