# 3 Bash scripting techniques every Linux user should know

> **Source:** <https://www.howtogeek.com/beginner-friendly-ways-to-level-up-your-bash-scripts/>
> **Author:** Graeme Peacock

Have you been thinking about biting the bullet and learning Bash scripting? Or perhaps you're like me, and you're always looking for ways to improve. I have three tips that will improve every Bash script you write.

Passing arguments, writing a help menu, and debugging can be burdensome. However, the `getopts` command, Heredoc, and the `set -x` option are common solutions that not everybody knows about. Let's tackle that problem and learn how these things can improve your Bash scripts.

## Use a Heredoc to specify a help menu

When you execute a script months after you wrote it, the first thing you will need is a help menu. Without that, you need to dig into the source code to jog your memory, which is an unnecessary hassle.

When I started writing help menus in Bash, I used a function that ran dozens of `echo` statements:

```bash
_help() {
  echo -e "Usage foo [OPTION]\n"
  echo -e "OPTIONS"
  echo -e "  -h     display this help menu"
  echo -e "  -r     do NOT press this button\n"
  echo -e "  -a     echo something\n"
}
```

Even though I aligned the menu elements to make them more readable, a Heredoc is far superior:

```bash
_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

OPTIONS
  -h     display this help menu
  -r     do NOT press this button
  -a     echo something
EOF
}
```

The code is tidier, more readable, easier to write, and without special characters (e.g., `\n`) to format it. To make your life easier, you should prefer a Heredoc over separate echo statements.

Also, notice the use of `$(basename "$0")`, which extracts the filename from the script path so that our help menu displays the name of the script.

- `$0` is the script path.
- `basename` extracts the filename from a path.

## Parse command line arguments like a pro

Now that we have a menu, we need to process the arguments. The most common and easiest way is to access the positional parameters provided by Bash.

```bash
#!/usr/bin/env bash
echo "The first parameter: $1"
echo "The second parameter: $2"
```

However, that approach becomes complex when handling options (aka flags) and values. The `getopts` command is the go-to solution, and it's built into Bash. Below, I have expanded the earlier help menu example to allow us to process options:

```bash
#!/usr/bin/env bash
_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

OPTIONS
  -h     display this help menu
  -r     do NOT press this button
  -a     echo something
EOF
}

while getopts "ra:h" opt; do
  case "$opt" in
  r)
    curl 'https://ascii.live/rick'
    ;;
  a)
    echo "ECHO -$opt: $OPTARG" # For example, "ECHO -a: foo"
    ;;
  h)
    _help
    exit 0
    ;;
  esac
done
```

### Accepting basic options

The basic form of the `getopts` command is:

```bash
getopts OPTSTRING OPTVAR
```

The options string ("optstring") is how we specify available options. If we want to accept the `-a`, `-b`, and `-c` options, then we specify the option string as follows:

```bash
getopts "abc" OPTVAR
```

There are three facts we can use to our advantage:

1. The option variable ("optvar") stores the option name currently being processed (e.g., a, b, or c).
2. When complete, `getopts` returns a number greater than zero.
3. A while loop will continue until it receives a falsy value, like an exit code of 1.

Simply put, the following code will process each option:

```bash
# This code is incomplete and does not work.
while getopts "abc" opt; do
   ...
done
```

Because the `opt` variable stores the option name (e.g., a, b, c), we can use a case statement to help process them:

```bash
# This code is incomplete and does not work.
while getopts "abc" opt; do
  case "$opt" in
  a) ... ;;
  b) ... ;;
  c) ... ;;
  esac
done
```

The `case $opt in` statement uses the `opt` variable and then matches it against `a)`, `b)`, or `c)`—the first match wins. Case statements use pattern matching, and we could do a lot more with them if we wanted to.

### Accepting options with values

Getting an option _value_ is the last thing to learn—for example: `-a foo`. First, we must tell `getopts` that an option accepts a value—add a colon after it in the option string. For example, `a:` tells `getopts` that `-a` accepts a value. It then becomes accessible via the `$OPTARG` variable.

```bash
# This code is incomplete and does not work.
while getopts "a:b" opt; do
  case "$opt" in
  a) echo "$OPTARG" ;;
  b) ... ;;
  esac
done
```

## Set a flag for optional debugging

Bugs are inevitable. Fortunately, Bash has a simple way to debug your script by printing all statements when they execute. We can also enable it optionally. Let's change our script to make that happen, using a `set -x` statement.

```bash
#!/usr/bin/env bash
set -x  # <-- ENABLE DEBUG STATEMENTS.

_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

OPTIONS
  -h     display this help menu
  -r     do NOT press this button
  -a     echo something
EOF
}

while getopts "ra:h" opt; do
  case "$opt" in
  r)
    curl 'https://ascii.live/rick'
    ;;
  a)
    echo "ECHO -$opt: $OPTARG" # For example, "ECHO -a: foo"
    ;;
  h)
    _help
    exit 0
    ;;
  esac
done
```

Now let's run the script:

```bash
./script.sh -a foo
```

You can see that Bash prints each command it executes and most variables it evaluates.

You could enable it optionally via a flag:

```bash
# This code is incomplete and does not work.
while getopts "ra:hd" opt; do
  case $opt in
  d)
    set -x  # <-- ENABLE DEBUG STATEMENTS.
    ;;
  # ...
  esac
done
```

Or you can enable it via an environment variable at the top of the script:

```bash
#!/usr/bin/env bash
[[ -n "$DEBUG" ]] && set -x  # <-- ENABLE DEBUG STATEMENTS.
```

Then enable debug mode like this:

```bash
DEBUG=true ./script.sh -a foo
```

Doing it that way means it will print the option processing code too.

---

So that's it—a sensible help menu, CLI argument parsing, and debugging. Each of these will apply to nearly every script you write. In fact, they're so common, you could write a script to make other scripts, populating them with the concepts you've learned today. In programming, we call them snippets. I have a "create" and "edit" Bash script that does just that.

Bash is a much larger topic, but these three simple tips should set a solid foundation for you.
