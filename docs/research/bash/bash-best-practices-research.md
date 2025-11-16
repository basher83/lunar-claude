# Research: bash scripting best practices production patterns tips tricks

## Metadata

- **Query:** bash scripting best practices production patterns tips tricks
- **Generated:** 2025-11-16 06:13:40
- **Script:** firecrawl_sdk_research.py
- **Categories:** github
- **Search Results:** 10
- **Scraped Pages:** 10

## Summary

Found 10 search results, successfully scraped 10 pages.

- **High Quality Sources:** 10/10

## Sources

1. [GitHub - ralish/bash-script-template: A best practices Bash script template with several useful functions](https://github.com/ralish/bash-script-template) ⭐
  - Domain: `github.com`
  - Quality Score: 20
2. [GitHub - pushkar100/notes-bash-shell-scripting: Shell Scripting Short Notes & Reference](https://github.com/pushkar100/notes-bash-shell-scripting) ⭐
  - Domain: `github.com`
  - Quality Score: 20
3. [GitHub - icy/bash-coding-style: A Bash coding style](https://github.com/icy/bash-coding-style) ⭐
  - Domain: `github.com`
  - Quality Score: 20
4. [Zsh - Opinionated Best Practices · GitHub](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd) ⭐
  - Domain: `gist.github.com`
  - Quality Score: 20
5. [GitHub - bahamas10/bash-style-guide: A style guide for writing safe, predictable, and portable bash scripts (not sh!)](https://github.com/bahamas10/bash-style-guide) ⭐
  - Domain: `github.com`
  - Quality Score: 20
6. [GitHub - PacktPublishing/Bash-Quick-Start-Guide: Bash Quick Start Guide, published by Packt](https://github.com/PacktPublishing/Bash-Quick-Start-Guide) ⭐
  - Domain: `github.com`
  - Quality Score: 20
7. [GitHub - djeada/Bash-Scripts: 100+ Bash scripts for automating routine tasks and streamlining your workflow.](https://github.com/djeada/Bash-Scripts) ⭐
  - Domain: `github.com`
  - Quality Score: 20
8. [Bash Pitfalls · GitHub](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c) ⭐
  - Domain: `gist.github.com`
  - Quality Score: 20
9. [GitHub - hegdepavankumar/shell-scripting-tutorial: Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced developer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting.](https://github.com/hegdepavankumar/shell-scripting-tutorial) ⭐
  - Domain: `github.com`
  - Quality Score: 18
10. [GitHub - dereknguyen269/programing-best-practices: Awesome Programming Best Practices for Beginners](https://github.com/dereknguyen269/programing-best-practices) ⭐
  - Domain: `github.com`
  - Quality Score: 18

## Content

### 1. GitHub - ralish/bash-script-template: A best practices Bash script template with several useful functions

**Source:** [https://github.com/ralish/bash-script-template](https://github.com/ralish/bash-script-template)
**Domain:** `github.com`
**Quality Score:** 20

_A best practices Bash script template with several useful functions - ralish/bash-script-template_

A best practices Bash script template with several useful functions

### License

[MIT license](https://github.com/ralish/bash-script-template/blob/main/LICENSE)

[![license](https://camo.githubusercontent.com/792005a2e8dbe879289d5d751e99cb400b4d7bf08d5e26f57d2a0d5ae0d21723/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f72616c6973682f626173682d7363726970742d74656d706c617465)](https://choosealicense.com/licenses/mit/)

A _Bash_ scripting template incorporating best practices & several useful functions.

- [Motivation](https://github.com/ralish/bash-script-template#motivation)
- [Files](https://github.com/ralish/bash-script-template#files)
- [Usage](https://github.com/ralish/bash-script-template#usage)
- [Controversies](https://github.com/ralish/bash-script-template#controversies)
- [License](https://github.com/ralish/bash-script-template#license)

## Motivation

I write Bash scripts frequently and realised that I often copied a recent script whenever I started writing a new one. This provided me with a basic scaffold to work on and several useful helper functions I'd otherwise likely end up duplicating.

Rather than continually copying old scripts and flensing the irrelevant code, I'm publishing a more formalised template to ease the process for my own usage and anyone else who may find it helpful. Suggestions for improvements are most welcome.

## Files

| File | Description |
| --- | --- |
| **template.sh** | A fully self-contained script which combines `source.sh` & `script.sh` |
| **source.sh** | Designed for sourcing into scripts; contains only those functions unlikely to need modification |
| **script.sh** | Sample script which sources in `source.sh` and contains those functions likely to be modified |
| **build.sh** | Generates `template.sh` by combining `source.sh` & `template.sh` (just a helper script) |

## Usage

Being a Bash script you're free to _slice-and-dice_ the source as you see fit.

The following steps outline what's typically involved to help you get started:

1. Choose between using either:
1. `template.sh` (fully self-contained)
1. `script.sh` with `source.sh` (source in most functions)
1. Depending on your choice open `template.sh` or `script.sh` for editing
1. Update the `script_usage()` function with additional usage guidance
1. Update the `parse_params()` function with additional script parameters
1. Add additional functions to implement the desired functionality
1. Update the `main()` function to call your additional functions

### Adding a `hostname` parameter

The following contrived example demonstrates how to add a parameter to display the system's hostname.

Update the `script_usage()` function by inserting the following before the `EOF`:

```text
    --hostname                  Display the system's hostname
```

Update the `parse_params()` function by inserting the following before the default case statement (`*)`):

```text
--hostname)
    hostname=true
    ;;
```

Update the `main()` function by inserting the following after the existing initialisation statements:

```text
if [[ -n ${hostname-} ]]; then
    pretty_print "Hostname is: $(hostname)"
fi
```

## Controversies

The Bash scripting community is an opinionated one. This is not a bad thing, but it does mean that some decisions made in this template aren't going to be agreed upon by everyone. A few of the most notable ones are highlighted here with an explanation of the rationale.

### errexit ( _set -e_)

Conventional wisdom has for a long time held that at the top of every Bash script should be `set -e` (or the equivalent `set -o errexit`). This modifies the behaviour of Bash to exit immediately when it encounters a non-zero exit code from an executed command if it meets certain criteria. This would seem like an obviously useful behaviour in many cases, however, controversy arises both from the complexity of the grammar which determines if a command is eligible for this behaviour and the fact that there are many circumstances where a non-zero exit code is expected and should not result in termination of the script. An excellent overview of the argument against this option can be found in [BashFAQ/105](https://mywiki.wooledge.org/BashFAQ/105).

My personal view is that the benefits of `errexit` outweigh its disadvantages. More importantly, a script which is compatible with this option will work just as well if it is disabled, however, the inverse is not true. By being compatible with `errexit` those who find it useful can use this template without modification while those opposed can simply disable it without issue.

### nounset ( _set -u_)

By enabling `set -u` (or the equivalent `set -o nounset`) the script will exit if an attempt is made to expand an unset variable. This can be useful both for detecting typos as well as potentially premature usage of variables which were expected to have been set earlier. The controvery here arises in that many Bash scripting coding idioms rely on referencing unset variables, which in the absence of this option are perfectly valid. Further discussion on this option can be found in [BashFAQ/112](https://mywiki.wooledge.org/BashFAQ/112).

This option is enabled for the same reasons as described above for `errexit`.

## License

All content is licensed under the terms of [The MIT License](https://github.com/ralish/bash-script-template/blob/main/LICENSE).

[Activity](https://github.com/ralish/bash-script-template/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fralish%2Fbash-script-template&report=ralish+%28user%29)

You can’t perform that action at this time.

---

### 2. GitHub - pushkar100/notes-bash-shell-scripting: Shell Scripting Short Notes & Reference

**Source:** [https://github.com/pushkar100/notes-bash-shell-scripting](https://github.com/pushkar100/notes-bash-shell-scripting)
**Domain:** `github.com`
**Quality Score:** 20

_Shell Scripting Short Notes & Reference. Contribute to pushkar100/notes-bash-shell-scripting development by creating an account on GitHub._

Shell Scripting Short Notes & Reference

[**1** Branch](https://github.com/pushkar100/notes-bash-shell-scripting/branches) [**0** Tags](https://github.com/pushkar100/notes-bash-shell-scripting/tags)

## Bash Shell Scripting Notes

Shell Scripting Short Notes & Reference

- [Bash Shell Scripting Notes](https://github.com/pushkar100/notes-bash-shell-scripting#bash-shell-scripting-notes)
  - [Introduction](https://github.com/pushkar100/notes-bash-shell-scripting#introduction)
    - [Executing a Shell Script:](https://github.com/pushkar100/notes-bash-shell-scripting#executing-a-shell-script-)
    - [First Line of a shell script:](https://github.com/pushkar100/notes-bash-shell-scripting#first-line-of-a-shell-script-)
    - [Printing/Displaying:](https://github.com/pushkar100/notes-bash-shell-scripting#printing-displaying-)
    - [Comments:](https://github.com/pushkar100/notes-bash-shell-scripting#comments-)
    - [Variables:](https://github.com/pushkar100/notes-bash-shell-scripting#variables-)
    - [Variable Names:](https://github.com/pushkar100/notes-bash-shell-scripting#variable-names-)
    - [Using Variables:](https://github.com/pushkar100/notes-bash-shell-scripting#using-variables-)
    - [Storing Commands in variables:](https://github.com/pushkar100/notes-bash-shell-scripting#storing-commands-in-variables-)
    - [Tests:](https://github.com/pushkar100/notes-bash-shell-scripting#tests-)
      - [File Operator Tests:](https://github.com/pushkar100/notes-bash-shell-scripting#file-operator-tests-)
      - [String Operator Tests:](https://github.com/pushkar100/notes-bash-shell-scripting#string-operator-tests-)
        - [General Test Syntax: `[ -flag STRING]`](https://github.com/pushkar100/notes-bash-shell-scripting#general-test-syntax------flag-string--)
      - [Arithmetic Operator Tests:](https://github.com/pushkar100/notes-bash-shell-scripting#arithmetic-operator-tests-)
    - [The `if` Condition: (Uses Tests in its conditional)](https://github.com/pushkar100/notes-bash-shell-scripting#the--if--condition---uses-tests-in-its-conditional-)
    - [The `if-else` Condition: (Uses Tests in its conditional)](https://github.com/pushkar100/notes-bash-shell-scripting#the--if-else--condition---uses-tests-in-its-conditional-)
    - [The `if-elif-else` Condition: (Uses Tests in its conditional)](https://github.com/pushkar100/notes-bash-shell-scripting#the--if-elif-else--condition---uses-tests-in-its-conditional-)
    - [The `for` loop:](https://github.com/pushkar100/notes-bash-shell-scripting#the--for--loop-)
    - [Positional Parameters:](https://github.com/pushkar100/notes-bash-shell-scripting#positional-parameters-)
      - [The `$@`:](https://github.com/pushkar100/notes-bash-shell-scripting#the------)
    - [Accepting User Input (STDIN):](https://github.com/pushkar100/notes-bash-shell-scripting#accepting-user-input--stdin--)
    - [Exit Status of Commands:](https://github.com/pushkar100/notes-bash-shell-scripting#exit-status-of-commands-)
      - [The `$?`: (Return code/exit status)](https://github.com/pushkar100/notes-bash-shell-scripting#the--------return-code-exit-status-)
      - [Storing return code/exit status in a variable:](https://github.com/pushkar100/notes-bash-shell-scripting#storing-return-code-exit-status-in-a-variable-)
    - [Chaining Commands:](https://github.com/pushkar100/notes-bash-shell-scripting#chaining-commands-)
    - [Exit Statuses of Shell scripts:](https://github.com/pushkar100/notes-bash-shell-scripting#exit-statuses-of-shell-scripts-)
    - [Functions:](https://github.com/pushkar100/notes-bash-shell-scripting#functions-)
      - [Calling a function:](https://github.com/pushkar100/notes-bash-shell-scripting#calling-a-function-)
      - [Parameters to functions:](https://github.com/pushkar100/notes-bash-shell-scripting#parameters-to-functions-)
      - [Variable Scope:](https://github.com/pushkar100/notes-bash-shell-scripting#variable-scope-)
      - [Local Variables:](https://github.com/pushkar100/notes-bash-shell-scripting#local-variables-)
      - [Exit Status/Return Code of functions:](https://github.com/pushkar100/notes-bash-shell-scripting#exit-status-return-code-of-functions-)
    - [Shell Script CheckList:](https://github.com/pushkar100/notes-bash-shell-scripting#shell-script-checklist-)
    - [WILDCARDS:](https://github.com/pushkar100/notes-bash-shell-scripting#wildcards-)
      - [Using Wildcards in Shell Scripts:](https://github.com/pushkar100/notes-bash-shell-scripting#using-wildcards-in-shell-scripts-)
    - [Switch-Case Statements:](https://github.com/pushkar100/notes-bash-shell-scripting#switch-case-statements-)
    - [Logging:](https://github.com/pushkar100/notes-bash-shell-scripting#logging-)
      - [Log files locations are CONFIGURABLE:](https://github.com/pushkar100/notes-bash-shell-scripting#log-files-locations-are-configurable-)
      - [Logging with `logger`:](https://github.com/pushkar100/notes-bash-shell-scripting#logging-with--logger--)
    - [`while` loops:](https://github.com/pushkar100/notes-bash-shell-scripting#-while--loops-)
      - [Infinite While loops:](https://github.com/pushkar100/notes-bash-shell-scripting#infinite-while-loops-)
      - [Reading a file LINE-BY-LINE:](https://github.com/pushkar100/notes-bash-shell-scripting#reading-a-file-line-by-line-)
      - [Exiting a loop before it's normal end:](https://github.com/pushkar100/notes-bash-shell-scripting#exiting-a-loop-before-it-s-normal-end-)
      - [Skipping iteration and executing next iteration on a loop:](https://github.com/pushkar100/notes-bash-shell-scripting#skipping-iteration-and-executing-next-iteration-on-a-loop-)
    - [Arithmetic Operations:](https://github.com/pushkar100/notes-bash-shell-scripting#arithmetic-operations-)
    - [Debugging Shell Scripts:](https://github.com/pushkar100/notes-bash-shell-scripting#debugging-shell-scripts-)
      - [`-x` option:](https://github.com/pushkar100/notes-bash-shell-scripting#--x--option-)
      - [Exit on Error:](https://github.com/pushkar100/notes-bash-shell-scripting#exit-on-error-)
      - [Print Shell Input Lines (As they are being read):](https://github.com/pushkar100/notes-bash-shell-scripting#print-shell-input-lines--as-they-are-being-read--)
    - [Manual Debugging:](https://github.com/pushkar100/notes-bash-shell-scripting#manual-debugging-)
    - [Syntax Highlighting:](https://github.com/pushkar100/notes-bash-shell-scripting#syntax-highlighting-)
      - [PS4:](https://github.com/pushkar100/notes-bash-shell-scripting#ps4-)
    - [File Types (DOS/WINDOWS vs UNIX/LINUX):](https://github.com/pushkar100/notes-bash-shell-scripting#file-types--dos-windows-vs-unix-linux--)
      - [Knowing what type of file: (To which shell does the script belong to?)](https://github.com/pushkar100/notes-bash-shell-scripting#knowing-what-type-of-file---to-which-shell-does-the-script-belong-to--)
      - [Converting DOS text scripts to UNIX scripts:](https://github.com/pushkar100/notes-bash-shell-scripting#converting-dos-text-scripts-to-unix-scripts-)
      - [Converting UNIX text scripts to DOS scripts:](https://github.com/pushkar100/notes-bash-shell-scripting#converting-unix-text-scripts-to-dos-scripts-)

## Introduction

Any series of terminal commands can be put into a script. The shell, which is an interpreter, reads the script and executes those commands. Shell Scripting is useful to automate tasks, performing complex execution, etc.

BASH script = **B** ourne **A** gain **SH** ell script

### Executing a Shell Script

Give execute permission to your script. Ex: `chmod +x /path/to/yourscript.sh`

And to run your script. Ex: `/path/to/yourscript.sh`

We can also use the relative path if it is known: Ex: `./yourscript.sh` (`./` is necessary if directory is not in $PATH!)

### First Line of a shell script

When we create a shell script and wish to run it, we need to make sure it has the execute permission.

Use `chmod` command to add it, if execute permission does not exist.

Every script STARTS with a line like this:

`#!/path/to/interpreter`

The #(sharp) and !(bang/exclamation) are collectively known as the 'SHEBANG'.

The first line tells us which interpreter(Shell) is supposed to execute this script!.
Examples:

- `#!/bin/csh` = c shell,
- `#!/bin/ksh` = k shell,
- `#!/bin/zsh` = z shell,
- `#!/bin/bash` = bash shell

Basically, when the script runs: It is the specified shell that is running as a process and the file that it executes is the script's path.

You don't have to use a shell as an interpreter: Ex: `#!/usr/bin/python` =\> Uses the python interpreter (Hence, a python script)

Note: If we don't specify the interpreter, the current shell executes the script but this is tricky.
If the script contains commands not understood by the current shell, it could cause errors (Don't do this!)

### Printing/Displaying

`echo` command = It prints the supplied argument/string. Every echo statement prints on a NEW LINE.

Ex: `echo "Hello World!"` =\> Output: `Hello World!`

### Comments

Every line other than the first line (#! /bin/..) that STARTS with a '#'(pound/sharp/hash) marks a comment, example:

```text
 #!/bin/bash

 # Let's print something	=> A comment

 echo "Hello There"

 # End of printing		=> A comment
```

- If '#' STARTS on the line, the WHOLE LINE is IGNORED.
- If '#' appears in the MIDDLE of a line, Anything to the RIGHT of a '#' is IGNORED.

### Variables

Storage locations that have a name. They are 'name-value' pairs.

Syntax: `VARIABLE_NAME="Value"`

**NOTE: NO SPACES before or after the '='**

- The variable names are CASE-SENSITIVE!.
- And, by "convention", they are usually in UPPERCASE.

### Variable Names

Variable names can contain:

- LETTERS (a-z, A-Z),
- DIGITS (0-9), &
- UNDERSCORES (\_) \[ONLY!\]

VARIABLE NAMES **CANNOT** START WITH A DIGIT!

### Using Variables

Precede the variable name with a '$' sign. Ex:

```text
MY_SHELL="bash"
echo "This script uses the $MY_SHELL shell"
```

Output: This script uses the bash shell.

**Alternatively: (Optional)**

Enclose the variable in curly brackets '{}' and preced it with a '$', Ex:

```text
MY_SHELL="bash"
echo "I am ${MY_SHELL}ing shell"
```

Output: I am bashing on my keyboard

Hint: It's a best practice to use the ${VARIABLE} syntax if there is text or characters that directly precede or follow the variable.

If a specified variable does NOT exist, Nothing is printed in its place in the echo statement.

### Storing Commands in variables

`VAR_NAME=$(command)`

(or)

```text
VAR_NAME=`command`
```

(Command enclosed with tilde sign: Older Scripts)

### Tests

Syntax: `[ condition-to-test-for ]`

Returns true if test passes, else false. Ex:

`[ -e /etc/passwd]` = tests if the '/etc/passwd' file exists.

#### File Operator Tests

General Test Syntax: `[ -flag fileOrDirPath]`
Flags:

- `-d` = True if file is a directory
- `-e` = True if file exists
- `-f` = True if file exists and is a regular file
- `-s` = True if file exists and is NOT empty
- `-r` = True if file is readable by you
- `-w` = True if file is writable by you
- `-x` = True if file is executable by you

#### String Operator Tests

##### General Test Syntax: `[ -flag STRING]`

Flags:

- `-z` = True if STRING is empty
- `-n` = True if STRING is NOT empty

Equality Tests:

- `STRING1 = STRING2` = True if strings are equal
- `STRING1 != STRING2` = True if strings are NOT equal

NOTE: For testing Variable string in the conditions, enclose it in quote(""). Ex:

`"$MY_SHELL" = "bash"`

#### Arithmetic Operator Tests

General Test Syntax: `[ arg1 -flag arg2]`

Flags:

- `-eq` = True if arg1 equals to arg2
- `-ne` = True if arg1 is NOT equal to arg2
- `-lt` = True if arg1 is LESS THAN arg2
- `-le` = True if arg1 is LESS THAN OR EQUAL TO arg2
- `-gt` = True if arg1 is GREATER THAN arg2
- `-ge` = True if arg1 GREATER THAN OR EQUAL TO arg2

(`man test` =\> Help on tests.)

### The `if` Condition: (Uses Tests in its conditional)

```text
if [ condition-is-true ]
then
	command 1
 	command 2
 	...
	command N
fi
```

### The `if-else` Condition: (Uses Tests in its conditional)

```text
if [ condition-is-true ]
then
	commands 1 ... N
else
	commands 1 ... N
fi
```

### The `if-elif-else` Condition: (Uses Tests in its conditional)

```text
if [ condition-is-true ]
then
	commands 1 ... N
elif [ condition-is-true ]
then
	commands 1 ... N
else
	commands 1 ... N
fi
```

### The `for` loop

```text
for VARIABLE_NAME in ITEM_1 ... ITEM_N
do
	command 1
	command 2
	...
	command N
done
```

First item in the block is assigned to variable and commands are executed, next item in in the block is assigned to variable and commands are executed again, and so on ...

VARIABLE\_NAME need NOT be declared earlier.

**Ex 1:**

```text
for COLOR in red green blue
do
    echo "COLOR: $COLOR"
done
```

Output:

```text
COLOR: red
COLOR: green
COLOR: blue
```

**We can also store the items in a variable, separated by spaces!**

**Ex 2:**

```text
COLORS="red green blue"
for COLOR in $COLORS
do
    echo "COLOR: $COLOR"
done
```

Output:

```text
COLOR: red
COLOR: green
COLOR: blue
```

Note:: Bash scripting also contains `while` loops.

### Positional Parameters

Syntax (On the CLI): `$ script.sh parameter1 parameter2 parameter3`

- `$0` = "script.sh" (The script itself)
- `$1` = "parameter1"
- `$2` = "parameter2"
- `$3` = "parameter3"

We can Assign Positional Parameters to Variables. Ex:

`USER=$1`

#### The `$@`

`$@` contains all the parameters starting from Parameter 1 to the last parameter. It can be used to loop over parameters. Ex:

```text
for USER in $@
do
	echo "Archiving user : $USER"
	...
	...
done
```

### Accepting User Input (STDIN)

`read` command.

Syntax: `read -p "PROMPT" VARIABLE`

Note: The input could also come from pipelined(\|) or redirected output/input(<, >) if STDIN is changed to those.

Ex:

```text
read -p "Enter a UserName: " USER
echo "ARCHIVING $USER"
```

### Exit Status of Commands

Every command returns an exit status. Range of the status is from `0 - 255`. It is used for Error checking.

- `0` = Success
- Other than `0` = Error condition

**Use `man` on the command to find out what exit status means what (for the command).**

#### The `$?`: (Return code/exit status)

`$?` contains the return code(exit status) of the 'previously executed' command.

Ex:

```text
ls /not/here
echo "$?"
```

Output: `2` is echoed, which is the return command.

Ex:

```text
HOST="google.com"
ping -c 1 $HOST		=> -c tells command to send only 1 packet to test connection
if [ "$?" -eq "0" ]
then
	echo "$HOST reachable."
else
	echo "$HOST unreachable."
fi
```

#### Storing return code/exit status in a variable

Ex:

```text
ping -c 1 "google.com"
RETURN_CODE=$?		=> Now, we can use the variable RETURN_CODE anywhere in the script.
```

### Chaining Commands

- `&&` =\> AND => Executes commands one after the other UNTIL one of them FAILS. (in that case -> short-circuiting)

(It executes commands as long as they are returning exit statuses `0`. STOPS as soons as a command does NOT return 0)

Syntax: `cmd1 && cmd2 && ...`

- `||` =\> OR => Executes commands one after the other UNTIL one of them SUCCEEDS. (in that case -> short-circuiting)

(It executes commands as long as they are returning exit statuses NOT `0`. STOPS as soons as a command returns 0)

Syntax: `cmd1 || cmd2 || ...`

- `;` =\> Semicolon => Executes commands ONE AFTER ANOTHER without checking the exit statuses/return codes.

(It it same as/equivalent to executing each of the commands on a separate line)

Syntax: `cmd1 ; cmd2 ; ...`

### Exit Statuses of Shell scripts

Shell scripts too can have exit statuses.

`exit` command needs to be used.

- `exit` =\> Exits the script with exit status equal to that of the previously executed command within the script.
- `exit X` =\> Exits with exit status X. X is a number between 0 & 255. (0 = Success, !0 = Error)

(No exit status => This also equals the exit status of the previously executed command within the script)

### Functions

Reduces script length, **"DRY"(Dont Repeat Yourself) - concept of functions**.

A function:

- Is a block of reusable code.
- Must be defined before use.
- Has parameter support.
- It can return an "exit status/return code".

**Method 1:**

```text
function function-name() {
	# code goes here
}
```

**Method 2:**

```text
function-name() {
	# code goes here
}
```

#### Calling a function

`function-name`

We do **NOT** use parentheses () in the function like in other programming languages. Functions need to be defined before they are used. (In Top Down order of parsing) (That is, Function Definition must have been scanned(Top->Down parsing) before the call to the function)

**Functions can call other functions**

#### Parameters to functions

`function-name parameter1 parameter2 ...`

- `$1`, `$2`, ... = Parameter1, Parameter2, ...
- `$@` = Array of all the parameters

NOTE: `$0` REFERS TO THE SHELL SCRIPT ITSELF (NOT THE FUNCTION!)

Ex:

```text
function hello() {
	echo "Hello, $1"
}
hello Jason
```

Output: `"Hello, Jason"`

#### Variable Scope

- ALL Variables are GLOBAL by Default!
- Variables have to be DEFINED before Use.

Therefore, All variables defined 'before' a 'function call' can be accessed within it. Those that are defined 'after' the 'function call' **cannot** be accessed.

- Accessing a variable that has NOT been defined before the function call : Nothing/null/No Value for Variable.
- Accessing a variable that has been defined before the function call : Correct value.

#### Local Variables

Variables that can be accessed only within the function that it is declared. Use the keyword `local`.

Syntax: `local LOCAL_VAR=someValue`

Only functions can have local variables! (Try to keep variables local inside a function)

#### Exit Status/Return Code of functions

- Explicity: `return <RETURN_CODE>`

Note: For the WHOLE SCRIPT, we used the `exit <RETURN-CODE>` command. For functions it is `return` keyword.

- Implicitly: The exit status of the last command executed within the function.

Exit status range: `0 to 255`

- `0` = Success,

- All other values = errors of some kind,

- `$?` = gets the exit status of last executed command(after execution of cmd)/function(after the call)/script(terminal))

Tip: write function to backup files, returning 0 exit status if successful.

NOTE:

- `basename fileOrDirPath` =\> returns just the filename/Directory name after stripping off the path to the file.
- `dirname fileOrDirPath` =\> Getting the directory of the file/directory.

### Shell Script CheckList

HOW to write your scripts (PATTERN!)

1. Does your script start with a shebang?
2. Does your script include a comment describing the purpose of the script?
3. Are the global variables declared at the top of your script, following the initial comment(s)?
4. Have you grouped all of your functions together following the global variables?
5. Do your functions use local variables?
6. Does the main body of your shell script follow the functions?
7. Does your script exit with an explicit exit status?
8. At the various exit points, are exit statuses explicitly used?

**EXAMPLE**

```text
#!/bin/bash
#
# <Replace with the description and/or purpose of this shell script.>

GLOBAL_VAR1="one"
GLOBAL_VAR2="two"

function function_one() {
	local LOCAL_VAR1="one"
	# <Replace with function code.>
}

# Main body of the shell script starts here.
#
# <Replace with the main commands of your shell script.>

# Exit with an explicit exit status. Ex: exit 0
```

### WILDCARDS

**(Read in detail in: 'Command Line Basics Course/pdf/cheatsheet')**

Wildcards are Character or Strings used for pattern matching. Also referred to as **'Globbing'**: Commonly used to match file or directory paths. Wilcards can be used with **MOST** commands.

- matches 0 or more characters (Ex: _.txt, a_, a\*.txt, _a_.txt)
- ? \- matches exactly 1 character (Ex: ?.txt, a?, a?.txt, ?a.txt, a???.txt)

- \[\] \- a character class(Mathces any of the characters inside bracket, exactly one match.) (Ex: \[aeiou\], ca\[nt\]\* => can cant candy ... etc)

- \[!\] \- matches any of the characters NOT included inside the bracket. Exactly one match. (Ex: \[!aeiou\]\* => First character should not be a vowel)

- \[x-y\] - creating a range of values to match. Exactly one match. (Ex: \[a-g\]\* => start with any letter between a and g, \[3-6\]\* => start with any number between 3 and 6)

- \[\[:alpha:\]\] => Matches upper and lower case letters. Exactly One match.

- \[\[:alnum:\]\] => Matches upper and lower case letters or any decimal digits (0-9). Exactly One match.

- \[\[:digit:\]\] => Matches decimal digits (0-9). Exactly One match.

- \[\[:lower:\]\] => Matches lower case letters. Exactly One match.

- \[\[:space:\]\] => Matches White Space. Exactly One match.

- \[\[:upper:\]\] => Matches upper case letters. Exactly One match.

- \ - Match a wildcard character (Escape) (Ex: \*? => matches anything followed by a question mark \[Ex: 'done?'\])

TIP:: good practice to **not** include wildcards as filenames/directory names.

Examples:

- `ls *.txt` =\> list all files ending with '.txt'
- `ls a*` =\> list all files starting with 'a'
- `ls *aA` =\> list all files containing 'aA'
- `ls ?` =\> list all files containing one character
- `ls ??` =\> list all files containing two characters
- `ls ?.txt` =\> list all files containing one character and ending with '.txt'
- `ls fil?` =\> list all files such as 'file', 'filk', 'fild' ... (starting with 'fil' followed by any one character)
- `ls [a-d]*` =\> list all files starting with any lowercase letter in between 'a' and 'd'
- `ls *mp[[:digit:]]` =\> lists all files ending with 'mp' and a digit(0-9). \[Ex: ending with 'mp3', 'mp4', ...\]

#### Using Wildcards in Shell Scripts

Wildcards are great for working with groups of files of directories.

We can use it just like in regualar commands. Ex1:

```text
#!/bin/bash
cd /var/www
cp *.html /var/www-just-html
```

Ex2:

```text
for FILE in /var/www/*.html
do
	echo "Copying $FILE"
	cp $FILE /var/www-just-html
done
```

(NOTE: In the above example, the wildcard matches in the for loop expand as a List/Array that can be Iterated.)

### Switch-Case Statements

(Similar to `Switch-Case`) =\> Testing for multiple values. Use in-place of many 'if-elif-elif-elif...' scenarios!

Syntax:

```text
case "$VAR" in
	pattern_1)
		#commands go here
		;;
	pattern_N)
		#commands go here
		;;
esac
```

Patterns are case-sensitive!. Once a pattern has been matched, the commands of a pattern are executed until `;;` is reached! `;;` is like a break statement.

Examples. Ex1:

```text
case "$1" in
	start)
		/usr/sbin/sshd			# Executes the script at the specified path!
		;;
	stop)
		kill $(cat /var/run/sshd.pid)
		;;
esac
```

Note: Wildcards can be used as patterns: Ex: `*)` matches anything.

The pipe(\|) maybe used as an 'OR' in the patterns. Ex2:

```text
case "$1" in
	start|START)
		/usr/sbin/sshd
		;;
	stop|STOP)
		kill $(cat /var/run/sshd.pid)
		;;
	*)
		echo "Usage: $0 start|stop" ; exit 1
		;;
esac
```

The above example matches either upper or lower case 'start', else either upper or lower case 'stop', else it
matches anything that did not match one of the first two cases.

We can use other wildcards in the patterns as well. Ex3:

```text
case "$1" in
	[yY]|[yY][eE][sS])
		echo "You answered yes."
		;;
	[nN]|[nN][oO])
		echo "You answered no."
		;;
	*)
		echo "Invalid Answer."
		;;
esac
```

Above matches y, yes (case-insensitive) or n, no(case-insensitive).

NOTE: All the rules of wildcards are valid for patterns of case statements.

Case Statements:

- In place of if statements,
- Wildcards maybe used for patterns.
- Multiple patterns can be matched with the help of a pipe(\|) which acts as an 'OR' in the pattern.

### Logging

`Syslog` =\> Uses standard facilities and severities to categorize messages.

- `Facilities`: `kern`, `user`, `mail`, `daemon`, `auth`, `local0`, `local7`, etc.
- `Severities`: `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`.

Ex: if your script is using mail, you could use the 'mail' facility for logging.

#### Log files locations are CONFIGURABLE

1. '/var/log/messages'

(or)

1. '/var/log/syslog'

(Location depends on system)

#### Logging with `logger`

`logger` is a command line utility - used for logging 'syslog' messages. By default, it creates `user.notice` messages.

1. Basic logging message: `logger "Message"`

Example output: 'Aug 2 01:02:44 linuxsvr: Message'.

1. Logging message with facility and severity: Syntax: `logger -p facility.severity "Message"`

Ex: `logger -p local0.info "Message"`

1. Tagging the log message: Use the `-t` option followed by tagName

Usually you want to use the script's name as tag in order to easily identify the source of the log message. `logger -t myscript -p local0.info "Message"`

Example output: 'Aug 2 01:02:44 linuxsvr myscript: Message'

1. Include PID(Process ID in the log message): use `-i` option: `logger -i -t myscript "Message"`

Ex output: 'Aug 2 01:02:44 linuxsvr myscript\[12986\]: Message'

1. Additionally display log message on screen (apart from already logging it to the log file): use `-s` option

Ex: `logger -s -p local0.info "Message"`

NOTE: Different facilities and severities could cause the system logger to route the log messages to a different locaton/log file.

**NOTE:**

`$RANDOM` generates a random number. Ex:

`echo "$RANDOM"` =\> 29133

Using `shift`: `shift` shifts the command line arguments to the left (The script name is deleted).

The original param1 becomes $0, original param2 becomes $1, and so on ...

### `while` loops

Loop control (Alternative to `for`)

Syntax:

```text
while [ CONDITION_IS_TRUE ]
do
	command 1
	command 2
	...
	command N
done
```

While the command in the command keeps returning 0(success) exit status, the while loop keeps looping/executing. Usually commands inside the while loop change the condition for the next iteration's check.

#### Infinite While loops

Condition is always true, keeps looping forever (Use `CTRL-C` to exit the script - when executed in the terminal). You may need to use the `kill` command to kill the process - when run as an application outside terminal.

You may want to run some background processes infinitely: Ex: Running a daemon process in the background:

```text
while true
do
	command 1 ... N
	sleep 1
done
```

The `sleep` command: Used to 'PAUSE' the execution of the code for a given number of seconds (as argument).

Examples of while loops: Ex1:

```text
INDEX=1
while [ $INDEX -lt 6 ]
do
	echo "Creating project-${INDEX}"
	mkdir /usr/local/project-${INDEX}
	((INDEX++))				# Arithmetic operations are enclosed within '((...))'
done
```

Ex2:

```text
while [ "$CORRECT" != "y" ]
do
	read -p "Enter your name: " NAME
	read -p "Is $NAME correct?: " CORRECT
done
```

Ex3:

```text
while ping -c 1 app1 > /dev/null	# ping must succeed & redirect o/p to /dev/null as we don't want to see msg
do
	echo "app1 still up ... "
	sleep 5				# Pause execution for 5 seconds
done
echo "app1 is down! ... "
```

#### Reading a file LINE-BY-LINE

- Not possible in `for` loop since it reads word by word.

While loop example:

```text
LINE_NUM=1
while read LINE
do
	echo "${LINE_NUM}: ${LINE}"
	((LINE_NUM++))
done < /etc/fstab
```

- The /etc/fstab is taken as input to the whole while loop.
- `read LINE` reads the current line of the file
- Since it is a condition of the while, while stops when lines of the files are over

Note: input to read command need not only be lines from a file, we can use pipelining to the while to read from commands, etc.

Note: read command supports splitting of data that it reads into multiple variables!

#### Exiting a loop before it's normal end

- Use `break` statement.

```text
while [ CONDITION_IS_TRUE ]
do
	...
	break
	...
done
```

#### Skipping iteration and executing next iteration on a loop

- Use `continue` statement.

```text
while [ CONDITION_IS_TRUE ]
do
	...
	continue
	...
done
```

### Arithmetic Operations

We can execute arithmetic operations within double parentheses'((...))'. Ex:

`((INDEX++))` = increments INDEX value by 1 (++ operator). Useful within loops.

### Debugging Shell Scripts

'bug' => Means error

- Examine inner workings of your script
- Get to the Source/Root of the problem
- Fix Bugs(errors)

#### `-x` option

Debug Whole script:

- `#!/bin/bash -x` = prints commands and their arguments as they execute. That is: Values of variables, values of wildcard matches.

Ex: `VAR1="HI"` (Call an x-trace)

- `PS4` controls what is shown before a line while using '-x' command (default is '+') (LATER..)

- Debug from command line:
  - `set -x` = Start Debugging
  - `set +x` = Stop Debugging

Ex:

```text
$ set -x
$ ./scriptName.sh
<output>
$set +x
```

- Debug only a portion of the code:

Ex:

```text
#!/bin/bash
...
set -x
echo $VAR_NAME
set +x
...
```

Note: For every command that is debugged, a '+' sign appears to it's left. The outputs of commands (Ex: output of echo command) DON'T have a '+' next to them.

Note: Using ONLY THE `-x` flag executes subsequent lines of code (commands) even if a previous command was erroneous!

#### Exit on Error

- `-e` flag. (Exit immediately if a command exists with a non-zero status.)

Syntax: `#!/bin/bash -e`

Ex: It can be combined with the trace (-x) option.

- `#!/bin/bash -e -x`
- `#!/bin/bash -ex`
- `#!/bin/bash -xe`
- `#!/bin/bash -x -e`

#### Print Shell Input Lines (As they are being read)

- `-v` flag. (Can also be combined with -x and -e.)

Prints input lines before (without) any substitutions and expansions are performed. Therefore, All the lines of the shell script are printed as they are, and the outputs of printing commands(like echo) are also displayed.

- `#!/bin/bash -vx` = Useful, because we can see trace (substituted input) lines as well as shell script lines!

More Info: `help set` or `help set | less`

### Manual Debugging

You can create your own debugging code. Ex: Use a sepcial variable like DEBUG. (DEBUG=true, DEBUG=false)

- Boolean `true` : exit status 0 (success)
- Boolean `false` : exit status non-zero (failure)

Ex 1:

```text
#!/bin/bash
DEBUG=true
$DEBUG && echo "debug mode on!"
```

```text
#!/bin/bash
DEBUG=false
$DEBUG || echo "debug mode off!"
```

Ex 2: (When you want to echo lines in debug mode)

```text
#!/bin/bash
DEBUG="echo"
$DEBUG ls
```

Prints ls output to screen since $DEBUG is nothing but 'echo'

Ex 3:

```text
#!/bin/bash
function debug() {
	echo "Executing $@"
	$@
}
debug ls
```

### Syntax Highlighting

Syntax errors are common. Use a text editor and enable syntax highlighting to identify syntax errors. (Ex: vim, emacs) Helps us catch syntax errors.

#### PS4

Controls what is displayed before a line while using the `-x` option (during debugging). Default value is '+'

Bash Variables:

- BASH\_SOURCE, (name of the script)
- LINENO, (line number of the script)
- FUNCNAME (function name)
- etc ...

We can explicitly set the PS4 variable.

Ex:

```text
#!/bin/bash -x
...
PS4='+ $BASH_SOURCE : $LINENO : ${FUNCNAME[0] : '
...
```

Example Output: '+ ./test.sh : 3 : debug() : TEST\_VAR=test'

### File Types (DOS/WINDOWS vs UNIX/LINUX)

Control character is used to represent end of line in both DOS and Unix text files.

Control Character:

1. Unix/Linux: Line Feed
2. DOS: Carriage return & a Line Feed (2 characters)

- `cat -v script.sh` = View the file along with the carriage returns (^M)

When opening Linux/Unix text files on a DOS/Windows system: We may see one long line without new lines.

And, in the opposite: We may see additional characters on Unix/Linux (`^M`). =\> Might run into errors while executing the files.

Therefore, need to remove the carriage returns in order to run the file. The shebang `#!` is very important.

#### Knowing what type of file: (To which shell does the script belong to?)

`file script.sh`

Example Output:

- `script.sh: Bourne-Again shell script, ASCII text executable` =\> UNIX script,
- `script.sh: Bourne-Again shell script, ASCII text executable, with CRLF line terminators` =\> DOS script,

#### Converting DOS text scripts to UNIX scripts

- `dos2unix script.sh` =\> Removes incompatible characters(ex: DOS carriage returns) in DOS to match with UNIX text scripts. (So that we can run it on UNIX/LINUX)

Confirm the removal of incompatible characters by running `file script.sh` again to see what type of shell the script runs in. (Should be one of the unix shells that you are using.)

#### Converting UNIX text scripts to DOS scripts

- `unix2dos script.sh` =\> Does the opposite of dos2unix. (So that we can run it on DOS/WINDOWS)

How does all this happen? => When editing file in one OS and operating and using it another, Copying from one OS and pasting in another (via net, etc), Copying from web browsers into the system ... many ways!\]

---- * *

- USE SHELL SCRIPTS TO AUTOMATE TASKS - REPETITIVE WORK
- SHELL SCRIPTS CAN BE SHORTCUTS - DON'T HAVE TO REMEMBER EVERYTHING (LIKE EVERY COMMAND)
- HAPPY SCRIPTING!

---- * *

**THE END**

## About

Shell Scripting Short Notes & Reference

### Resources

[Readme](https://github.com/pushkar100/notes-bash-shell-scripting#readme-ov-file)

[Activity](https://github.com/pushkar100/notes-bash-shell-scripting/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fpushkar100%2Fnotes-bash-shell-scripting&report=pushkar100+%28user%29)

## [Releases](https://github.com/pushkar100/notes-bash-shell-scripting/releases)

No releases published

## [Packages\  0](https://github.com/users/pushkar100/packages?repo_name=notes-bash-shell-scripting)

No packages published

You can’t perform that action at this time.

---

### 3. GitHub - icy/bash-coding-style: A Bash coding style

**Source:** [https://github.com/icy/bash-coding-style](https://github.com/icy/bash-coding-style)
**Domain:** `github.com`
**Quality Score:** 20

_A Bash coding style. Contribute to icy/bash-coding-style development by creating an account on GitHub._

A Bash coding style

[github.com/icy/bash-coding-style](https://github.com/icy/bash-coding-style "https://github.com/icy/bash-coding-style")

[**1** Branch](https://github.com/icy/bash-coding-style/branches) [**2** Tags](https://github.com/icy/bash-coding-style/tags)

## Some `Bash` coding conventions and good practices

Coding conventions are... just conventions.
They help to have a little fun with scripting,
not to create new war/bias conversations.

Feel free to break the rules any time you can; it's important
that you will always love what you would have written
because scripts can be too fragile, too hard to maintain,
or so many people hate them...
And it's also important to have a consistent way in your scripts.

- [Deprecated conventions](https://github.com/icy/bash-coding-style#deprecation)
  - [`variable name started with an underscore` (`_foo_bar`)](https://github.com/icy/bash-coding-style#variable-name-started-with-an-underscore-_foo_bar)
- [Naming and styles](https://github.com/icy/bash-coding-style#naming-and-styles)
  - [Tabs and Spaces](https://github.com/icy/bash-coding-style#tabs-and-spaces)
  - [Pipe](https://github.com/icy/bash-coding-style#pipe)
  - [Variable names](https://github.com/icy/bash-coding-style#variable-names)
  - [Function names](https://github.com/icy/bash-coding-style#function-names)
- [Error handling](https://github.com/icy/bash-coding-style#error-handling)
  - [Sending instructions](https://github.com/icy/bash-coding-style#sending-instructions)
  - [Pipe error handling](https://github.com/icy/bash-coding-style#pipe-error-handling)
  - [Catch up with $?](https://github.com/icy/bash-coding-style#catch-up-with-)
  - [Automatic error handling](https://github.com/icy/bash-coding-style#automatic-error-handling)
    - [Set -u](https://github.com/icy/bash-coding-style#set--u)
    - [Set -e](https://github.com/icy/bash-coding-style#set--e)
- [Techniques](https://github.com/icy/bash-coding-style#techniques)
  - [Keep that in mind](https://github.com/icy/bash-coding-style#keep-that-in-mind)
  - [A little tracing](https://github.com/icy/bash-coding-style#a-little-tracing)
  - [Making your script a library](https://github.com/icy/bash-coding-style#making-your-script-a-library)
  - [Quick self-doc](https://github.com/icy/bash-coding-style#quick-self-doc)
  - [No excuse](https://github.com/icy/bash-coding-style#no-excuse)
  - [Meta programming](https://github.com/icy/bash-coding-style#meta-programming)
  - [Removing with care](https://github.com/icy/bash-coding-style#removing-with-care)
  - [Shell or Python/Ruby/etc](https://github.com/icy/bash-coding-style#shell-or-pythonrubyetc)
- [Contributions](https://github.com/icy/bash-coding-style#contributions)
  - [Variable names for arrays](https://github.com/icy/bash-coding-style#variable-names-for-arrays)
- [Good lessons](https://github.com/icy/bash-coding-style#good-lessons)
- [Resources](https://github.com/icy/bash-coding-style#resources)
- [Author. License](https://github.com/icy/bash-coding-style#author-license)

## Naming and Styles

### Tabs and Spaces

Don't use `(smart-)`tabs. Replace a tab by two spaces.
Do not accept any trailing spaces.

Many editors can't and/or aren't configured to display the differences
between tabs and spaces. Another person's editor is just not your editor.
Having spaces does virtually help a strange reader of your script.

### Pipe

There are `inline` pipe and `display` pipe. Unless your pipe is
short, please use `display` pipe to make things clear. For example,

```text
 # This is an inline pipe: "$(ls -la /foo/ | grep /bar/)"

 # The following pipe is of display form: every command is on
 # its own line.

foobar="$( \
  ls -la /foo/ \
  | grep /bar/ \
  | awk '{print $NF}')"

_generate_long_lists \
| while IFS= read -r  line; do
    _do_something_fun
  done
```

When using `display` form, put pipe symbol (`|`) at the beginning of
of its statement. Don't put `|` at the end of a line, because it's the
job of the line end (`EOL`) character and line continuation (`\`).

Here is another example

```text
 # List all public images found in k8s manifest files
 # ignore some in-house image.
list_public_images() {
  find . -type f -iname "*.yaml" -exec grep 'image: ' {} \; \
  | grep -v ecr. \
  | grep -v '#' \
  | sed -e "s#['\"]##g" \
  | awk '{print $NF}' \
  | sort -u \
  | grep -Eve '^(coredns|bflux|kube-proxy|logstash)$' \
}
```

### Variable names

If you are going to have meanful variable name, please use them
for the right purpose. The variable name `country_name` should
not be used to indicate a city name or a person, should they?
So this is bad

```text
countries="australia germany berlin"
for city in $countries; do
  echo "city or country is: $city
done
```

That's very bad example but that is to emphasize the idea.
(FIXME: Add better examples)

A variable is named according to its scope.

- If a variable can be changed from its parent environment,
it should be in uppercase; e.g, `THIS_IS_A_USER_VARIABLE`.
- Other variables are in lowercase
- Any local variables inside a function definition should be
declared with a `local` statement.

Example

```text
 # The following variable can be provided by user at run time.
D_ROOT="${D_ROOT:-}"

 # All variables inside `my_def` are declared with `local` statement.
my_def() {
  local d_tmp="/tmp/"
  local f_a=
  local f_b=

  # This is good, but it's quite a mess
  local f_x= f_y=
}
```

Though `local` statement can declare multiple variables, that way
makes your code unreadable. Put each `local` statement on its own line.

`FIXME`: Add flexibility support.

### Function names

Name of internal functions should be started by an underscore (`_`).
Use underscore (`_`) to glue verbs and nouns. Don't use camel form
(`ThisIsNotMyStyle`; use `this_is_my_style` instead.)

Use two underscores (`__`) to indicate some very internal methods aka
the ones should be used by other internal functions.

## Error handling

### Sending instructions

All errors should be sent to `STDERR`. Never send any error/warning message
to a`STDOUT` device. Never use `echo` directly to print your message;
use a wrapper instead (`warn`, `err`, `die`,...). For example,

```text
_warn() {
  echo >&2 ":: $*"
}

_die() {
  echo >&2 ":: $*"
  exit 1
}
```

Do not handle error of another function. Each function should handle
error and/or error message by their own implementation, inside its own
definition.

```text
_my_def() {
  _foobar_call

  if [[ $? -ge 1 ]]; then
    echo >&2 "_foobar_call has some error"
    _error "_foobar_call has some error"
    return 1
  fi
}
```

In the above example, `_my_def` is trying to handle error for `_foobar_call`.
That's not a good idea. Use the following code instead

```text
_foobar_call() {
  # do something

  if [[ $? -ge 1 ]]; then
    _error "${FUNCNAME[0]} has some internal error"
  fi
}

_my_def() {
  _foobar_call || return 1
}
```

### Catch up with $?

`$?` is used to get the return code of the _last statement_.
To use it, please make sure you are not too late. The best way is to
save the last return code thanks to some local variable. For example,

```text
_do_something_critical
local _ret="$?"

 # from now on, $? is zero, because the latest statement (assignment)
 # (always) returns zero.

_do_something_terrible
echo "done"
if [[ $? -ge 1 ]]; then
  # Bash will never reach here. Because "echo" has returned zero.
fi
```

`$?` is very useful. But don't trust it.

Please don't use `$?` with `set -e` ;)

### Pipe error handling

Pipe stores its components' return codes in the `PIPESTATUS` array.
This variable can be used only _ONCE_ in the sub-`{shell,process}`
followed the pipe. Be sure you catch it up!

```text
  echo test | fail_command | something_else
  local _ret_pipe=( "${PIPESTATUS[@]}" )
  # from here, `PIPESTATUS` is not available anymore
```

When this `_ret_pipe` array contains something other than zero,
you should check if some pipe component has failed. For example,

```text
 # Note:
 #   This function only works when it is invoked
 #   immediately after a pipe statement.
_is_good_pipe() {
  echo "${PIPESTATUS[@]}" | grep -qE "^[0 ]+$"
}

_do_something | _do_something_else | _do_anything
_is_good_pipe \
|| {
  echo >&2 ":: Unable to do something"
}
```

### Automatic error handling

#### Set -u

Always use `set -u` to make sure you won't use any undeclared variable.
This saves you from a lot of headaches and critical bugs.

Because `set -u` can't help when a variable is declared and set to empty
value, don't trust it twice.

It's recommended to emphasize the needs of your variables before your
script actually starts. In the following example, the script just stops
when `SOME_VARIABLE` or `OTHER_VARIABLE` is not defined; these checks
are done just before any execution of the main routine(s).

```text
: a lot of method definitions

set -u

: "${SOME_VARIABLE}"
: "${OTHER_VARIABLE}"

: your main routine
```

#### Set -e

Use `set -e` if your script is being used for your own business.

Be **careful** when shipping `set -e` script to the world. It can simply
break a lot of games. And sometimes you will shoot yourself in the foot.
If possible please have an option for user choice.

Let's see

```text
set -e
_do_some_critical_check

if [[ $? -ge 1 ]]; then
  echo "Oh, you will never see this line."
fi
```

If `_do_some_critical_check` fails, the script just exits and the following
code is just skipped without any notice. Too bad, right? The code above
can be refactored as below

```text
set +e
if _do_some_critical_check; then
  echo "Something has gone very well."
fi
echo "You will see this line."
```

Now, if you expect to stop the script when `_do_some_critical_check` fails
(it's the purpose of `set -e`, right?), these lines don't help. Why?
Because `set -e` doesn't work when being used with `if`. Confused?
Okay, these lines are the correct one

```text
set +e
if _do_some_critical_check; then
  echo "All check passed."
else
  echo "Something wrong we have to stop here"
  exit 1 # or return 1
fi
```

`set -e` doesn't help to improve your code: it just forces you to work hard,
doesn't it?

Another example, in effect of `set -e`:

```text
(false && true); echo not here
```

prints nothing, while:

```text
    { false && true; }; echo here
```

prints `here`.

The result is varied with different shells or even different versions of the same shell.

In general, don't rely on `set -e` and do proper error handling instead.

For more details about `set -e`, please read

> The correct answer to every exercise is actually "because set -e is crap".

- [http://mywiki.wooledge.org/BashFAQ/105/Answers](http://mywiki.wooledge.org/BashFAQ/105/Answers)
- [When Bash scripts bite](https://news.ycombinator.com/item?id=14321213)

## Techniques

### Keep that in mind

There are lot of shell scripts that don't come with (unit)tests.
It's just not very easy to write tests. Please keep that in mind:
Writing shell scripts is more about dealing with runtime and side effects.

It's very hard to refactor shell scripts.
Be prepared, and don't hate bash/shell scripts too much ;)

### A little tracing

It would be very helpful if you can show in your script logs some tracing
information of the being-invoked function/method.

`Bash` has two jiffy variables `LINENO` and `FUNCNAME` that can help.
While it's easy to understand `LINENO`, `FUNCNAME` is a little complex.
It is an array of `chained` functions. Let's look at the following example

```text
funcA() {
  log "This is A"
}

funcB() {
  log "This is B"
  funcA
}

funcC() {
  log "This is C"
  funcB
}

: Now, we call funcC

funcC
```

In this example, we have a chain: `funcC -> funcB -> funcA`.
Inside `funcA`, the runtime expands `FUNCNAME` to

```text
FUNCNAME=(funcA funcB funcC)
```

The first item of the array is the method per-se (`funcA`),
and the next one is the one who instructs `funcA` (it is `funcB`).

So, how can this help? Let's define a powerful `log` function

```text
log() {
  echo "(LOGGING) ${FUNCNAME[1]:-unknown}: *"
}
```

You can use this little `log` method everywhere, for example, when `funcB`
is invoked, it will print

```text
LOGGING funcB: This is B
```

### Making your script a library

First thing first: Use `function` if possible. Instead of writting
some direct instructions in your script, you have a wrapper for them.
This is not good

```text
: do something cool
: do something great
```

Having them in a function is better

```text
_default_tasks() {
  : do something cool
  : do something great
}
```

Now in the very last lines of you script, you can execute them

```text
case "${@:-}" in
":")  echo "File included." ;;
"")   _default_tasks        ;;
esac
```

From other script you can include the script easily without executing
any code:

```text
 # from other script
source "/path/to_the_previous_script.sh" ":"
```

(When being invoked without any argument the `_default_tasks` is called.)

By advancing this simple technique, you have more options to debug
your script and/or change your script behavior.

### Quick self-doc

It's possible to generate beautiful self documentation by using `grep`,
as in the following example. You define a strict format and `grep` them:

```text
_func_1() { #public: Some quick introduction
  :
}

_func_2() { #public: Some other tasks
  :
}

_quick_help() {
  LANG=en_US.UTF_8
  grep -E '^_.+ #public' "$0" \
  | sed -e 's|() { #public: |☠|g' \
  | column -s"☠" -t \
  | sort
}
```

When you execute `_quick_help`, the output is as below

```text
_func_1    Some quick introduction
_func_2    Some other tasks
```

### No excuse

When someone tells you to do something, you may blindly do as said,
or you would think twice then raise your white flag.

Similarly, you should give your script a white flag. A backup script
can't be executed on any workstation. A clean up job can't silently
send `rm` commands in any directory. Critical mission script should

- exit immediately without doing anything if argument list is empty;
- exit if basic constraints are not established.

Keep this in mind. Always.

### Meta programming

`Bash` has a very powerful feature that you may have known:
It's very trivial to get definition of a defined method. For example,

```text
my_func() {
  echo "This is my function`"
}

echo "The definition of my_func"
declare -f my_func

 # <snip>
```

Why is this important? Your program manipulates them. It's up to your
imagination.

For example, send a local function to remote and excute them via `ssh`

```text
{
  declare -f my_func    # send function definition
  echo "my_func"        # execution instruction
} \
| ssh some_server
```

This will help your program and script readable especially when you
have to send a lot of instructions via `ssh`. Please note `ssh` session
will miss interactive input stream though.

### Removing with care

It's hard to remove files and directories **correctly**.
Please consider to use `rm` with `backup` options. If you use some
variables in your `rm` arguments, you may want to make them immutable.

```text
export temporary_file=/path/to/some/file/
readonly temporary_file
 # <snip>
rm -fv "$temporary_file"
```

### Shell or Python/Ruby/etc

In many situations you may have to answer to yourself whether you have
to use `Bash` and/or `Ruby/Python/Go/etc`.

One significant factor is that `Bash` doesn't have a good memory.
That means if you have a bunch of data (in any format) you probably
reload them every time you want to extract some portion from them.
This really makes your script slow and buggy. When your script
needs to interpret any kind of data, it's a good idea to move forward
and rewrite the script in another language, `Ruby/Python/Golang/...`.

Anyway, probably you can't deny to ignore `Bash`:
it's still very popular and many services are woken up by some shell things.
Keep learning some basic things and you will never have to say sorry.
Before thinking of switching to Python/Ruby/Golang, please consider
to write better Bash scripts first ;)

## Contributions

### Variable names for arrays

In #7, Cristofer Fuentes suggests to use special names for arrays.
Personally I don't follow this way, because I always try to avoid
to use Bash array (and/or associative arrays), and in Bash
per-se there are quite a lot of confusion (e.g, `LINENO` is a string,
`FUNCNAME` is array, `BASH_VERSION` is ... another array.)

However, if your script has to use some array, it's also possible to
have special name for them. E.g,

```text
declare -A DEPLOYMENTS
DEPLOYMENTS["the1st"]="foo"
DEPLOYMENTS["the2nd"]="bar"
```

As there are two types of arrays, you may need to enforce a better name

```text
declare -A MAP_DEPLOYMENTS
```

Well, it's just a reflection of some idea from another language;)

## Good lessons

See also in `LESSONS.md` ( [https://github.com/icy/bash-coding-style/blob/master/LESSONS.md](https://github.com/icy/bash-coding-style/blob/master/LESSONS.md)).

## Deprecation

### `variable name started with an underscore` (`_foo_bar`)

Deprecated on July 7th 2021 (cf.: [#10](https://github.com/icy/bash-coding-style/issues/10)).

To migrate existing code, you may need to list all variables that
followed the deprecated convention. Here is an simple `grep` command:

```text
$ grep -RhEoe '(\$_\w+)|(\$\{_[^}]+\})' . | sort -u

  # -R    find in all files in the current directory
  # -h    don't show file name in the command output
  # -E    enable regular expression
  # -o    only print variable name that matches our pattern
  # -e    to specify the pattern (as seen above)
```

## Resources

- [Anybody can write good bash with a little effort](https://blog.yossarian.net/2020/01/23/Anybody-can-write-good-bash-with-a-little-effort)
- [Google - Shell Style Guide](https://github.com/google/styleguide/blob/gh-pages/shellguide.md)
- [Defensive Bash programming](https://news.ycombinator.com/item?id=7815190)
- [Shellcheck](https://github.com/koalaman/shellcheck)
- [What exactly was the point of \[ “x$var” = “xval” \]?](https://www.vidarholen.net/contents/blog/?p=1035) TLDR; You needed the trick during the mid-to-late 1990s and some times before 2010. Now you can forget that trick.
- [Don't copy paste from a website to a terminal (thejh.net)](http://thejh.net/misc/website-terminal-copy-paste): [https://news.ycombinator.com/item?id=10554679](https://news.ycombinator.com/item?id=10554679)
- [Homebrew installation "isssue"](https://github.com/withfig/fig/discussions/300): [https://news.ycombinator.com/item?id=27901496](https://news.ycombinator.com/item?id=27901496)

## Authors. License

The original author is Anh K. Huynh and the original work was part of
[`TheSLinux`](http://theslinux.org/doc/bash/coding_style/).

A few contributors have been helped to fix errors and improve the style.
They are also the authors.

The work is released under a MIT license.

## About

A Bash coding style

[github.com/icy/bash-coding-style](https://github.com/icy/bash-coding-style "https://github.com/icy/bash-coding-style")

### Topics

[bash](https://github.com/topics/bash "Topic: bash") [styling](https://github.com/topics/styling "Topic: styling") [disaster](https://github.com/topics/disaster "Topic: disaster") [personality](https://github.com/topics/personality "Topic: personality")

### Resources

[Readme](https://github.com/icy/bash-coding-style#readme-ov-file)

[Activity](https://github.com/icy/bash-coding-style/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Ficy%2Fbash-coding-style&report=icy+%28user%29)

## [Releases\  2](https://github.com/icy/bash-coding-style/releases)

[v1.0.1: minor fixes\\
Latest\\
\\
on Feb 4, 2021Feb 4, 2021](https://github.com/icy/bash-coding-style/releases/tag/v1.0.1)

[\+ 1 release](https://github.com/icy/bash-coding-style/releases)

## [Packages\  0](https://github.com/users/icy/packages?repo_name=bash-coding-style)

No packages published

You can’t perform that action at this time.

---

### 4. Zsh - Opinionated Best Practices · GitHub

**Source:** [https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd)
**Domain:** `gist.github.com`
**Quality Score:** 20

_Zsh - Opinionated Best Practices. GitHub Gist: instantly share code, notes, and snippets._

[Gist Homepage](https://gist.github.com/)

Search Gists

Search Gists

[Gist Homepage](https://gist.github.com/)

[Sign in](https://gist.github.com/auth/github?return_to=https%3A%2F%2Fgist.github.com%2FChristopherA%2F562c2e62d01cf60458c5fa87df046fbd) [Sign up](https://gist.github.com/join?return_to=https%3A%2F%2Fgist.github.com%2FChristopherA%2F562c2e62d01cf60458c5fa87df046fbd&source=header-gist)

Instantly share code, notes, and snippets.

[![@ChristopherA](https://avatars.githubusercontent.com/u/69103?s=64&v=4)](https://gist.github.com/ChristopherA)

## [ChristopherA](https://gist.github.com/ChristopherA)/ **[zsh\_opinionated\_best\_practices.md](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd)**

Last active
3 months agoAugust 15, 2025 09:22

Show Gist options

- [Download ZIP](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd/archive/c4e6f3b37118634b018510d0e6faf289a030be86.zip)

- [Star15(15)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2FChristopherA%2F562c2e62d01cf60458c5fa87df046fbd) You must be signed in to star a gist
- [Fork2(2)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2FChristopherA%2F562c2e62d01cf60458c5fa87df046fbd) You must be signed in to fork a gist

- Embed

## Select an option

- Embed

Embed this gist in your website.

- Share

Copy sharable link for this gist.

- Clone via HTTPS

Clone using the web URL.

## No results found

[Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

Clone this repository at &lt;script src=&quot;<https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd.js&quot;&gt;&lt;/script&gt>;

- Save ChristopherA/562c2e62d01cf60458c5fa87df046fbd to your computer and use it in GitHub Desktop.

Embed

## Select an option

- Embed

Embed this gist in your website.

- Share

Copy sharable link for this gist.

- Clone via HTTPS

Clone using the web URL.

## No results found

[Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

Clone this repository at &lt;script src=&quot;<https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd.js&quot;&gt;&lt;/script&gt>;

Save ChristopherA/562c2e62d01cf60458c5fa87df046fbd to your computer and use it in GitHub Desktop.

[Download ZIP](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd/archive/c4e6f3b37118634b018510d0e6faf289a030be86.zip)

Zsh - Opinionated Best Practices

[Raw](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd/raw/c4e6f3b37118634b018510d0e6faf289a030be86/zsh_opinionated_best_practices.md)

[**zsh\_opinionated\_best\_practices.md**](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#file-zsh_opinionated_best_practices-md)

## Zsh Opinionated - A Guide to Best Practices

- **Abstract:** This guide provides best practices for writing clear, maintainable, and robust Zsh scripts. Aimed at helping developers transition from Bash to Zsh, particularly on macOS, this guide offers practical advice and examples for creating standardized and efficient scripts.

- **Copyright** This text of this guide is Copyright ©️2024 by Christopher Allen, and is shared under [spdx:CC-BY-SA-4.0](https://spdx.org/licenses/CC-BY-SA-4.0.html) open-source license. All the example code is relenquished to the public domain under [spx:CC0-1.0](https://spdx.org/licenses/CC0-1.0).

- **Tags:** [#zsh](https://gist.github.com/search?q=user%3AChristopherA+%23zsh) [#scripting](https://gist.github.com/search?q=user%3AChristopherA+%23scripting) [#cli](https://gist.github.com/search?q=user%3AChristopherA+%23cli) [#opinionated](https://gist.github.com/search?q=user%3AChristopherA+%23opinionated) [#guide](https://gist.github.com/search?q=user%3AChristopherA+%23guide) [#bestpractices](https://gist.github.com/search?q=user%3AChristopherA+%23bestpractices) [#tips](https://gist.github.com/search?q=user%3AChristopherA+%23tips)

- **Version:** 0.1.2 (2024-05-05) - Minor Update (for information on this versioning scheme, see [Status & Versioning](https://github.com/ChristopherA/Lists-of-High-Signal-Low-Noise-Links#status--versioning))

## Support My Open Source & Digital Civil Rights Advocacy Efforts

If you like these tools, my writing, my advocacy, my point-of-view, I invite you to sponsor me.

It's a way to plug into an advocacy network that's not focused on the "big guys". I work to represent smaller developers in a vendor-neutral, platform-neutral way, helping us all to work together.

You can become a monthly patron on my [GitHub Sponsor Page](https://github.com/sponsors/ChristopherA) for as little as $5 a month.

But please don’t think of this as a transaction. It’s an opportunity to advance the open web, digital civil liberties, and human rights together. You get to plug into my various projects, and hopefully will find a way to actively contribute to the digital commons yourself. Let’s collaborate!

\-\- Christopher Allen < [ChristopherA@LifeWithAlacrity.com](mailto:ChristopherA@LifeWithAlacrity.com) >
Github: [@ChristopherA](https://github.com/ChristopherA)
X/Twitter: [@ChristopherA](https://twitter.com/ChristopherA)

## Table of Contents

- [Introduction](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#introduction)
- [Organizing a Zsh-based Project Repository](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#organizing-a-zsh-based-project-repository)
  - [Directory Structure Explanation](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#directory-structure-explanation)
- [Strategic Use of Case in Names](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#strategic-use-of-case-in-names)
  - [Additional Strategic Examples](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#additional-strategic-examples)
- [Best Practices for Zsh Script File Names](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#best-practices-for-zsh-script-file-names)
- [Best Practices for Zsh Variable and Function Names](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#best-practices-for-zsh-variable-and-function-names)
  - [Using `typeset` for Variable Scoping](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#using-typeset-for-variable-scoping)
  - [Combining `typeset` Options](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#combining-typeset-options)
  - [Parsing an Array of Parameters Passed to a Function](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#parsing-an-array-of-parameters-passed-to-a-function)
  - [Parsing an Associative Array of Configuration Parameters](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#parsing-an-associative-array-of-configuration-parameters)
  - [Setting Useful Options with `setopt`](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#setting-useful-options-with-setopt)
- [Avoiding Overuse of Global Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#avoiding-overuse-of-global-variables)
- [Some Useful Environment Variables and Conventions](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#some-useful-environment-variables-and-conventions)
  - [Operating System Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#operating-system-environment-variables)
  - [System and Shell Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#system-and-shell-environment-variables)
  - [macOS Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#macos-environment-variables)
  - [User Environment Information](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#user-environment-information)
  - [Shell Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#shell-environment-variables)
  - [Zsh Specific Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#zsh-specific-environment-variables)
  - [Working Directory Information](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#working-directory-information)
  - [Script Environment](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#script-environment)
  - [Caller Script Information](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#caller-script-information)
  - [Process Information](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#process-information)
  - [Script Arguments](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#script-arguments)
  - [Git Environment Variables (local and global)](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#git-environment-variables-local-and-global)
  - [Other Common Environment Variables](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#other-common-environment-variables)
- [Snippets of Code with Naming Conventions Applied](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#snippets-of-code-with-naming-conventions-applied)
  - [Logging Messages](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#logging-messages)
  - [Creating and Using a Temporary Directory](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#creating-and-using-a-temporary-directory)
  - [Checking and Modifying Script Arguments](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#checking-and-modifying-script-arguments)
- [macOS and Zsh](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#macos-and-zsh)
  - [Misc.](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#misc)
- [To Be Continued](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#to-be-continued)

## Introduction

This is my opinionated guide to Zsh best practices.

To be clear, I've never produced a complicated Zsh script in a major production environment, so I can't quite call myself an expert, but here is what I've learned through my experience and research.

One of the major reasons that I've had to create this guide is that macOS transitioned away from `bash` to default to `zsh` with the release of macOS Catalina 10.15 in 2019, and their choice to not keep up with newer versions of `bash` in their default environment. This broke some of my favorite scripts, utilities, tools, and I decided it was time to just fully switch.

My goal in all of these recommendations is to help create clear, maintainable, and robust Zsh scripts.

My approach initially focuses on naming conventions, file organization, and coding standards to enhance readability and maintainability. This guide is meant to provide a consistent framework for Zsh scripting, but it's not set in stone. I welcome feedback and am open to learning from others. If you disagree with any of these practices, I'd love to understand your reasoning and am open to changing my mind.

I've drawn inspiration from other opinionated guides across various programming languages and frameworks which emphasize consistency and clarity in coding practices. By adopting similar principles, we can create a more standardized approach to Zsh scripting that benefits everyone in the long run.

Let's dive in and explore these best practices together, keeping in mind that the ultimate goal is to write better, more maintainable code.

## Organizing a Zsh-based Project Repository

For a project involving multiple scripts, consider the following structure:

_(Note: details of the inside organization of `./repo/` folder is a work-in-progress)_

```text
my-project/
├── README.md
├── .gitignore
├── Makefile
├── bin/
│   ├── build-project.sh
│   ├── deploy-project.sh
│   └── test-project.sh
├── config/
│   ├── setup-environment.zsh
│   └── configure-database.zsh
├── lib/
│   ├── utility-functions.zsh
│   └── string-manipulations.zsh
├── repo/
│   ├── config/
│   │   ├── allowed_commit_signers.txt
│   │   ├── allowed_tag_signers.txt
│   │   └── trust-manifest.envelope
│   ├── hooks/
│   │   ├── pre-commit.sh
│   │   ├── pre-push.sh
│   │   ├── commit-msg.sh
│   │   ├── post-merge.sh
│   │   └── (etc.)
│   ├── scripts/
│   │   ├── verify_commit_signers.sh
│   │   ├── verify_tag_signers.sh
│   │   ├── verify_release_signers.sh
│   │   ├── deploy_helpers.sh
│   │   ├── setup_environment.sh
│   │   └── security_checks.sh
│   ├── pipeline/
│   │   ├── github_actions.yml
│   │   ├── gitlab_ci.yml
│   │   └── bitbucket_pipelines.yml
├── tests/
│   ├── test-build-project.sh
│   ├── test-deploy-project.sh
│   └── function_deploy-TEST.sh
├── docs/
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   └── LICENSE
```

### Directory Structure Explanation

- **README.md**: Provides an overview and key information about the project. It should be located in the root directory to be recognized by GitHub.
- **.gitignore**: Specifies intentionally untracked files to ignore.
- **Makefile**: Automates the build process with `make` commands.
- **bin/**: Contains executable scripts for building, deploying, and testing the project.
- **config/**: Contains configuration scripts and settings.
- **lib/**: Contains library scripts with reusable functions.
- **repo/**:

  - **config/**: Contains configuration files for signing and trust management.
  - **hooks/**: Contains Git hook scripts for various Git lifecycle events.
  - \*\*scripts

/\*\*: Contains utility scripts for verification and setup tasks.

- **pipeline/**: Contains CI/CD pipeline configuration files for different platforms (GitHub Actions, GitLab CI, Bitbucket Pipelines).
- **tests/**: Contains test scripts for various project components and functions.
- **docs/**: Documentation files.

  - **CONTRIBUTING.md**: Guidelines for contributing to the project.
  - **CHANGELOG.md**: A log of changes for each version of the project.
  - **LICENSE**: The project's license file.

## Strategic Use of Case in Names

Specific choices of case in names can significantly enhance efficiency and readability when writing and using Zsh code using the command line interface. Here’s my approach:

- **Lower Case Preference**: One reason for choosing to use lower case filenames for scripts is that most command names in Unix-like systems are also in lower case (e.g., `ls`, `cd`, `grep`), and if scripts are going to be called like these commands, they too should be lower case. Another reason is that using `MixedCamelCase` in directory and file names can slow down tab completion in the shell. Thus, I strongly prefer using `lowercase` filenames for that efficiency. Lower case is also somewhat advantageous for auto-completion in many code editors, however, most tend to be more tolerant of different case, so I can make different choices for variables and functions.

- **Use Upper Case Strategically**: Slowing down tab completion can be useful to avoid mistakes. For example, using `connectAlice.sh` and `connectBob.sh` requires intentional effort to execute the correct file (capital-A vs capital-B respectively), thus I am less likely to accidentally execute the wrong script.

- **Use `lower_snake_case` for Readability**: Being able to quickly scan a significant amount of code requires some structure to enhance readability. Since `CamelCase` isn't an option for me (in particular for filenames), I largely prefer `lower_snake_case` for readability. This format ensures that filenames are clear and easy to understand.

- **Avoid `lower-kebab-case` for Variables and Functions**: Zsh variable and function names can't contain dashes or periods as they aren't valid identifiers. Use underscores in `small_snake_case` or `CamelCase` instead. `lower-kebab-case` can still be used for filenames as it helps in distinguishing parts of the name, but not for code.

- **Combine Separators Strategically**: Mixing name separators (`_` or `-`) can be useful for complex names. For instance, `project_charles-build_production-part_one` allows selective double-clicking to highlight specific parts of the name (for copy or to paste over), i.e. `project_charles`, `build_production`, and `part_one`.

- **Consistency Over Style**: The exact naming style (whether `CamelCase`, `snake_case`, or another convention) is less important than being consistent throughout your codebase. This consistency helps in maintaining readability and understanding, especially in collaborative environments.

### Additional Strategic Examples

- **Versioned Scripts**: `process_data-v1.sh` and `process_data-v2.sh`
- **Test Scripts**: `get_database-TEST.sh`
- **Configurations**: `config_server-main.sh` and `config_server-backup.sh`

## Best Practices for Zsh Script File Names

When naming Zsh scripts, consider the following:

1. **Use Lower Case**: For consistency with other shell commands, use lower case names, but sometimes it can be [strategically useful](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#strategic-use-of-case-in-names) to use mixed case.

2. **Use the Appropriate Extension**:

   - Use `.sh` for command-line executable scripts. This relies on the `#!/usr/bin/env zsh` shebang to specify the Zsh interpreter shell.
   - Use `.zsh` for libraries, function tests, and other scripts that are intended to be sourced or included in other scripts.

**Example**:

- `deploy_project.sh` for an executable script.
- `string_manipulations_functions.zsh` for a library of functions.
1. **Use Descriptive Names**: The script's name should clearly describe its purpose or functionality. This helps users understand what the script does without having to open it.

**Example**:

- `setup_database.sh` for a script that sets up the database.
- `backup_database.sh` for a script that handles database backups.
1. **Prefix with Action Words**: Try to start the script name with a verb that indicates the action performed by the script, followed by an object. This makes it clear what the script is supposed to do.

**Example**:

- `install_packages.sh` clearly indicates that the script installs packages.
- `remove_temp_files.sh` clearly indicates that the script removes temporary files.
1. **Keep It Short but Clear**: While the name should be descriptive, it should also be concise. Aim for a balance between clarity and brevity.

**Example**:

- `sync-backup.sh` instead of `synchronize-backup-directory.sh`.
1. **Avoid Overuse of Acronyms & Short Terms**: While acronyms can shorten names, overusing them can make script names cryptic. Use them judiciously and ensure they are commonly understood.

**Example**:

- `setup-command-line-envelope.sh` is clearer than `setup-cl-env.sh` _(especially as -env often refers to the environment)_.
1. **Avoid Spaces and Special Characters**: Use only alphanumeric characters, underlines, and hyphens. Avoid spaces and non-ASCII characters (in particular those found in macOS), as they can cause issues in some environments and platforms, and in general make the script harder to use.

**Example**:

- `generate_report.sh` instead of `generate report.sh`.
1. **Test Script Naming**:

- Use `<script_name>-TEST.sh` for functional tests of the script `<script_name>.sh`.
- Use `<function_name>-FTEST.sh` for tests of a specific function() in a script.

**Example**:

- `deploy_project-TEST.sh` for testing the `deploy_project.sh` script.
- `parse_table-FTEST.sh` for testing the `parse_table()` function.
1. **Prefix for Related Scripts**:

- If there are a series of related scripts as part of a project or system, use a prefix to identify and connect them together.

**Example**:
\- `zutil_script_template.sh` for the Zsh Utilities script template.
\- `zutil_git_tool.sh` for the Zsh Utilities git tool.
\- `zutil_script_template-TEST.sh` for the functional tests of the `zutil_script_template.sh`.
\- `zutil_parse_params-FTEST.sh` for the script that tests the `zutil_parse_params()` function.

1. **Prefix for Special Uses**:

   - Prefix a file with an underscore (`_`) if it is intended not to be executed directly but instead called or sourced by other scripts.

**Example**:
\- `_config.zsh` for configuration settings sourced by other scripts.
\- `_zutil_common_utilities.zsh` for the common utility functions used by `zutil_` project scripts.

1. **Versioning**: If you have multiple versions of a script, include the version number in the file name for any alternative versions. I prefix these with a hyphen `-` for [strategic](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#strategic-use-of-case-in-names) double-click selection.

**Example**:
\- `deploy_website.sh` for the working release.
\- `deploy_website-legacy` for the legacy deploy script.
\- `deploy_website-v1.2.sh` for version 1.2 of the deploy script.

## Best Practices for Zsh Variable and Function Names

These are requirements of Zsh:

1. **Avoid Hyphens and Periods in Variable and Function Names**: In Zsh, variable and function names cannot contain dashes or periods as they are not valid identifiers. Use underscores or CamelCase instead.

2. **Avoid Special Characters in Variable and Function Names**: Avoid characters like `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `+`, `=`, `{`, `}`, `[`, `]`, `|`, `\`, `:`, `;`, `"`, `'`, `<`, `>`, `?`, `/` as they have special meanings in Zsh and other Unix-like shells. Using them in variable or function names can cause unpredictable behavior or errors.

These remaining formatting choices are my personal preferences, developed with a primary focus on general readability to ensure the code is easy to understand at a glance. Additionally, these conventions aim to reduce errors by allowing quick differentiation between functions and the various types of variables. Finally, these guidelines emphasize consistency throughout the codebase, making it easier to maintain and collaborate on projects.

1. **Global Variables**: Use all uppercase with underscores (UPPER\_SNAKE\_CASE), e.g. `$VERBOSE_MODE`. These are often exported for use by other processes or scripts.

2. **Scoped Variables**: Use Mixed\_Snake\_Case for variables that will persist in the current execution environment, such as sourced scripts and called functions, e.g. `$Scoped_Variable`. Ensure that scoped variable names are at least two words for clarity.

3. **Local Variables**: Use CamelCase for local variables defined within specific functions or small blocks of code, e.g. `$LocalScopedVariable`. For short, single-word local variables, using lowercase is acceptable, especially if the variable type is clear from context, such as `typeset -i count`.

4. **Function Names**: Use `lowerfirst_Snake_Case` for function names to align with script names and make them distinct from variables, e.g. `log_Message`.

5. **Private/Internal Variables & Functions**: Prefix with an underscore (`_`) to indicate the variable or function is private to a series of interrelated scripts (e.g. the global `$_ZUTIL_DBUG`, or internal `$_debug` inside a local function is different than locally scoped `$Debug`).

```text
# Public function example
log_Message() {
       local message=$1
       echo "$(date): $message" >> "$LOG_FILE_FULL_PATH"

       # Private function example
       _log_Internal() {
           local _internalMessage=$1
           echo "Internal: $_internalMessage"
       }

       # Calling the private function
       _log_Internal "This is a test internal message"
}
```

### Using `typeset` for Variable Scoping

In Zsh, `typeset`, in combination with appropriate `setopt` options, is a versatile command for declaring and managing variables. It provides better control over variable scoping as compared to `global` and `local`. It can also be combined with various options to achieve different functionalities to ensure that variables have the desired properties, such as being local, read-only, global, integers, arrays, or associative arrays.

#### `typeset` Examples

1. **Declare a Variable Scoped to the Current Script Context**:

Using `typeset` explicitly defines a variable within the current script or function context, making its scope clear and avoiding ambiguity.

These are equivalent, but don't be vague, use `typeset`:

```text
# bad example
my_Function() {
       ScriptVar="value"
       echo "Script variable: $ScriptVar"
}
```

Do be explicit:

```text
# good example
my_Function() {
       typeset ScriptScopedVar="value"
       echo "Script scoped variable: $ScriptScopedVar"
}
```

1. **Declare Global Variable**:

The `-g` option with `typeset` makes the variable global, allowing it to be accessed and modified from anywhere in the script, including within functions.

```text
typeset -g GLOBAL_VAR="global_value"
echo "Global variable: $GLOBAL_VAR"
```

If the Zsh-specific `setopt warn_create_global` is set, Zsh will issue a warning. See details in [Setting Useful Options with `setopt`](https://gist.github.com/ChristopherA/562c2e62d01cf60458c5fa87df046fbd#setting-useful-options-with-setopt).

1. **Declare Local Variable**:

Declaring a variable as local within a function ensures it is only accessible within that function, preventing unintended interactions with variables outside the function.

```text
my_Function() {
       local localVar="value"
       echo "Local variable: $localVar"
}
```

1. **Declare Read-Only Variable**:

Using the `-r` option with `typeset` makes the variable read-only, meaning its value cannot be changed after it is set. This is useful for constants, ensuring that their values remain consistent throughout the script. Additionally, declaring variables as read-only reduces errors by preventing accidental modifications and enhances safety by protecting critical values from being altered. If you try to modify a read-only variable, Zsh will report an error indicating that the variable is read-only, and this error message will be sent to standard error (stderr).

```text
typeset -r ReadOnlyVar="constant"
echo "Read-only variable: $ReadOnlyVar"

# Attempt to modify the read-only variable
ReadOnlyVar="new_value"  # This will cause an error
```

Example error message when attempting to modify a read-only variable:

```text
ReadOnlyVar: read-only variable: ReadOnlyVar
```

1. **Declare Integer Variable**:

Using the `-i` option with `typeset` declares an integer variable, ensuring that only integer values can be assigned to it. This helps maintain the integrity of numerical data and prevents unexpected behavior due to invalid assignments. If you try to assign a non-integer value to an integer variable, Zsh will automatically convert it to an integer, typically resulting in `0`. Note that this conversion does not generate an error message and is sent to standard output (stdout).

```text
typeset -i IntCounter=42
echo "Integer counter: $IntCounter"

# Attempt to assign a non-integer value
IntCounter="text"  # This will convert "text" to 0
echo "Updated integer counter: $IntCounter"
```

Example behavior when assigning a non-integer value to an integer variable:

```text
Updated integer counter: 0
```

1. **Declare Array Variable**:

The `-a` option with `typeset` declares an array variable, allowing multiple values to be stored and accessed using index positions. Ensure proper initialization syntax to avoid issues. Note that accessing an out-of-bounds index will not generate an error but will return an empty value.

```text
typeset -a ArrayVar=("element1" "element2")
echo "Array variable: ${ArrayVar[@]}"

# This will return an empty value, not an error
echo "Accessing out-of-bounds index: ${ArrayVar[10]}"
```

1. **Declare Associative Array Variable**:

Using the `-A` option with `typeset` declares an associative array variable, allowing key-value pairs to be stored and accessed. Ensure unique keys and proper quotation to avoid syntax errors and unintended behavior. Accessing a non-existent key will not generate an error but will return an empty value. If there is a syntax error, it will be sent to standard error (stderr).

```text
typeset -A AssocArray
AssocArray[key1]="value1"
AssocArray[key2]="value2"
echo "Associative array: ${AssocArray[key1]}, ${AssocArray[key2]}"

# Accessing a non-existent key
echo "Non-existent key: ${AssocArray[nonExistentKey]}"
```

Example behavior when accessing a non-existent key:

```text
Non-existent key:
```

#### Combining `typeset` Options

You can combine multiple `typeset` options to achieve various effects. For example:

- **Declare a Read-Only Global Variable**:

```text
typeset -gr GLOBAL_READ_ONLY_CONSTANT="constant_value"
echo "Global constant: $GLOBAL_READ_ONLY_CONSTANT"
```

- **Declare a Local Integer Variable**:

```text
my_Function() {
      typeset -i localInt=100
      echo "Local integer: $localInt"
}
```

#### Parsing an Array of Parameters Passed to a Function

You can use `typeset` to handle and parse an array of parameters passed to a function efficiently. Here's an example of how to parse parameters in a function:

Suppose you have a function that processes user information, where each user is represented by a set of attributes:

```text
process_Users() {
    typeset -a Users_Array=("$@") # Initialize an array with all passed parameters
    typeset -i idx=1

    while (( idx <= $#Users_Array )); do
        typeset Name="${Users_Array[idx]}"
        typeset Age="${Users_Array[idx+1]}"
        typeset Email="${Users_Array[idx+2]}"

        echo "Processing user:"
        echo "Name: $Name"
        echo "Age: $Age"
        echo "Email: $Email"

        (( idx += 3 ))  # Move to the next set of user attributes
    done
}

# Call the function with user data
process_Users "Alice" 30 "alice@example.com" "Bob" 25 "bob@example.com"
```

#### Parsing an Associative Array of Configuration Parameters

Associative arrays are very useful for handling key-value pairs, such as configuration parameters or settings. Here is an example of how to use an associative array to manage and parse configuration parameters in a function.

Suppose you have a function that processes configuration settings for an application:

```text
process_Config() {
    # Initializes an associative array `Config` with the parameters passed to the function.
    typeset -A Config_Associative_Array=("$@")
    local key

    echo "Processing configuration settings:"
    # Iterate over the keys of the associative array and prints each key-value pair.
    for key in "${(@k)Config_Associative_Array}"; do
        echo "$key: ${Config_Associative_Array[$key]}"
    done
}

# Call the function with configuration settings and pass configuration parameters as key-value pairs
process_Config "database_host" "localhost" "database_port" "5432" "username" "admin" "password" "secret"
```

### Setting Useful Options with `setopt`

To take full advantage of `typeset`, you can set several useful options in Zsh:

1. **`setopt typeset_silent`**: Prevents `typeset` from printing variables in a global context.

2. **`setopt local_traps`**: Ensures traps set within a function are local to that function.

3. **`setopt warn_create_global`**: A warning is sent to standard error (stderr) if a global variable is created implicitly without the `typeset -g` option, helping to prevent accidental global variable creation and enhancing safety.

```text
setopt warn_create_global  # Enable warning for implicit global variable creation

# Example of implicit global variable creation that triggers a warning
my_Function() {
       GLOBAL_VAR="global_value"  # This will
```

trigger a warning
echo "Global variable: $GLOBAL\_VAR"
}

````text
my_Function
```

Example warning message sent to standard error (stderr) when implicitly creating a global variable:
```stderr
GLOBAL_VAR: created global parameter in function
```
````

1. **`setopt local_options`**: Ensures that `nounset`, `errexit` and other options set within a function, such as `noglob`, `noclobber`, etc., are automatically restored to their previous values when the function exits, preventing unintended side effects on the global environment.
   Example:
   \`\`\`sh
   \# Enable strict mode for the script
   set -o errexit -o nounset -o pipefail


   ````text
    strict_Function() {
        setopt local_options
        setopt errexit nounset

        echo "Inside function: strict mode enabled"
        # Uncommenting the next line will cause an error due to nounset
        # echo "Undefined variable: $undefined_var"
    }

   echo "Before function: strict mode enabled"
   strict_Function
   echo "After function: strict mode restored"
   ```
   ````

### Avoiding Overuse of Global Variables

Global variables in shell scripting, including both Bash and Zsh, can become a crutch and lead to significant headaches. They often create unintended side effects and make the code harder to understand and maintain.

Here are some strategies and best practices to avoid the pitfalls of overuse of global variables to create more robust, maintainable scripts:

1. **Use Local Variables**: Whenever possible, declare variables within the `local` scope of functions. This confines their accessibility and modifications to the function itself and its child functions, thereby reducing the risk of unintended interactions with other parts of the script.

2. **Dynamic Scoping in Zsh**: Zsh uses dynamic scoping, meaning that variables are visible within the function and any functions it calls. Use `local` or `typeset` to ensure variables are not inadvertently modified in other scopes. For example:

   ```text
   my_Function() {
       local LocalVar="value"
       echo "Local variable: $LocalVar"
   }
   ```

3. **Unique Naming Conventions**: If you must use global variables, work hard to make them unique to avoid collisions. Use very specific names, such as `GIT_UTILITY_SCRIPT_DIR`, or add a private prefix, e.g., `_ZUTIL_DEBUG`, or both `_ZUTIL_TOP_SCRIPT_DIR`.

4. **Set `warn_create_global` Option**: Enable the `warn_create_global` option in Zsh to spot variables that are implicitly made global. This can help catch unintentional global variables:

   ```text
   setopt warn_create_global
   ```

5. **Limit Scope with Functions**: Encapsulate your code in functions and minimize the use of variables outside these functions. This practice not only reduces the need for global variables but also enhances readability and reusability.

6. **Use Environment Variables for Truly Global Needs**: Only when a variable needs to be truly global across multiple scripts, should use use a global environment variable. However, do this sparingly and with clear documentation, as it can affect the global state of the user's environment:

   ```text
   export MY_GLOBAL_VAR="some_value"
   ```

7. **Read-Only Variables**: If a global variable is necessary and should not be modified, declare it as read-only to prevent accidental changes:

   ```text
   typeset -r READ_ONLY_GLOBAL="constant_value"
   ```

8. **Documentation and Comments**: Always document the purpose and scope of any global variables. If a function uses a global variable, make sure to document it in the function comments. This helps other developers (and future you) understand why the global variable exists and how it should be used.

## Some Useful Environment Variables and Conventions

### Operating System Environment Variables

These variables provide information about the operating system on which the Zsh shell is running. These variables are useful to help adjust the OS environment and provide information about the operating system's state and configuration. They are especially useful for scripts that need to perform operations based on the specific OS details.

- **`$(uname -s)`**: Contains the operating system type (e.g., `Linux`, `Darwin`).
- **`$(uname -r)`**: Provides the kernel version of the operating system (e.g. `23.5.0`)
- **`$(uname -m)`**: Specifies the hardware architecture of the machine (e.g., `x86_64`, `arm64`).
- **`$(uname -v)`**: Contains the release name of the operating system version. On my mac `Darwin Kernel Version 23.5.0: Wed May 1 20:12:58 PDT 2024; root:xnu-10063.121.3~5/RELEASE_ARM64_T6000`

```text
# Read-only operating system type
typeset -r OsType=$(uname -s)

# Read-only kernel version
typeset -r OsKernelVersion=$(uname -r)

# Read-only machine hardware name
typeset -r OsMachineHardware=$(uname -m)

# Read-only operating system release name
typeset -r OsReleaseName=$(uname -v)
```

### System and Shell Environment Variables

There are a number of environment variables about the specific computer system that are established before the script is executed. I prefix most of these with `SYS_`, `Sys_`, or `sys_` for clarity.

- **`$(uname -n)`**: Provides the network node hostname of the machine, as returned by `uname` command. NOTE: I don't use `$(hostname)` as returned by the dedicated `hostname` command. Both should be the same, but `uname` should be more consistent across different Unix-like systems.
- **`$PATH`**: is a system-level environment variable as it is available to all users and processes, however, it is also a user environment variable that likely is different for each user.
- **`$fpath`**: is a Zsh-specific shell environment variable, used by Zsh to locate function files.

Though ideally, these should not change during the execution of a script, for safety I copy them into a read-only variable scoped to the script context, thus I use Mixed\_Snake\_Case for their names.

I sometimes use the suffix `_Init` when I initialize them if I believe that they might change (or my script might change) these values during runtime.

```text
# Read-only network node hostname
typeset -r SysNodeHostname=$(uname -n)

# Initial read-only system PATH variable
typeset -r SysPathInit=$PATH

# Initial read-only Zsh function search path variable
typeset -r SysFpathInit=$fpath
```

### macOS Environment Variables

If `OsIsOsx` then I find setting these environment variables useful. I prefix these with `Osx`.

```text
# Read-only flag indicating if the operating system is macOS
typeset -r OsIsOsx=$( [[ $(uname -s) == "Darwin" ]] && echo true || echo false )

# Mac Device Hardware Model if the system is macOS
[[ $OsIsOsx == true ]] && typeset -r OsxHardwareModel=$(sysctl -n hw.model)

# Get Device Model Name if the system is macOS
[[ $OsIsOsx == true ]] && typeset -r OsxDeviceModelName=$(system_profiler SPHardwareDataType | awk -F ': ' '/Model Name/ { print $2 }')

# Get Device CPU if the system is macOS
[[ $OsIsOsx == true ]] && typeset -r OsxDeviceCPU=$(/usr/sbin/sysctl -n machdep.cpu.brand_string | sed s/"Apple "//)

# Set read-only environment variables for macOS version information if the system is macOS
[[ $OsIsOsx == true ]] && read OsxProductVersion OsxVersMajor OsxVersMinor OsxVersPatch <<<$(sw_vers -productVersion | awk -F. '{print $0 " " $1 " " $2 " " $3}') && typeset -r OsxProductVersion OsxVersMajor OsxVersMinor OsxVersPatch
[[ $OsIsOsx == true ]] && typeset -r OsxBuildVersion="$(sw_vers -buildVersion)"
```

### User Environment Information

These variables contain information about the current system user, thus are not prefixed with `sys_`, so I use the prefix `User_`.

- `$USER`: is the current user's name.
- `$LOGNAME`: is the login name of the user.
  **Note:** The `$USER` and `$LOGNAME` variables typically contain the same value, but there can be differences. `$USER` is often set by the shell and can change within a session, reflecting the effective user ID. `$LOGNAME`, on the other hand, is usually set by the login process and reflects the original login name, remaining consistent even if the user switches to another account using commands like `su`.
- `$HOME`: is the current user's home directory.
- `$SHELL`: is the user's default shell, ensuring any shell-specific operations within the script use the correct shell.
- `$TERM`: is the current terminal type, which is useful for scripts that handle terminal-specific functionality or output formatting. In non-interactive sessions, `$TERM` might be unset or set to `dumb`, indicating no interactive terminal is available. (If `$TERM` is blank, for safety, I set it to `dumb`.)
- `$LANG`: is the user's language and locale settings, ensuring scripts that handle localization or internationalization are consistent with the user's environment. On macOS, it usually defaults to `en_US.UTF-8`.
- `$(id -u)`: is the user's unique identifier, useful for scripts that need to verify or log user actions.
- `$(id -g)`: is the user's group identifier, important for scripts managing file permissions or group-specific actions.
- `$(id -gn)`: is the user's primary group name.
- `$(id -Gn | tr ' ' ',')`: captures all the group names the user belongs to, which can be useful for managing permissions or checking group memberships.
- `$MAIL`: is the user's mail directory, included for completeness, which may be relevant for scripts that handle or check legacy Unix-style user email.

When I use any of these environment variables, for safety, I copy them into read-only variables first.

```text
# Read-only current user's name
typeset -r UserName=$USER

# Read-only login name of the user
typeset -r UserLogname=$LOGNAME

# Read-only current user's home directory, normalized using realpath
typeset -r UserHome=$(realpath "$HOME")

# Read-only user's default shell
typeset -r UserShell=$SHELL

# Read-only user's terminal type (set to default `dumb` if non-interactive or nil)
typeset -r UserTerm=${TERM:-dumb}

# Read-only user's language/locale setting (set it to a default if $LANG if nil)
typeset -r UserLang=${LANG:-en_US.UTF-8}

# Read-only user's unique identifier
typeset -r UserUid=$(id -u)

# Read-only user's group identifier
typeset -r UserGid=$(id -g)

# Read-only user's primary group name
typeset -r UserGroup=$(id -gn)

# Read-only user's primary group names (comma-separated)
typeset -r UserGroups=$(id -Gn | tr ' ' ',')

# Read-only user's mail directory
typeset -r UserMail=$MAIL
```

### Shell Environment Variables

These variables are common to most Unix-like shells, including Zsh. They help manage the shell environment and provide information about the shell session's state and configuration. These variables are useful for scripts that need to adapt their behavior based on the shell environment.

- **`interactive`**: Indicates whether the shell is interactive (`true` or `false`).
- **`login`**: Indicates whether the shell is a login shell (`true` or `false`).
- **`monitor`**: Indicates whether the shell is running with job control enabled (`true` or `false`).
- **`restricted`**: Indicates whether the shell is running in restricted mode

(`true` or `false`).

```text
# Current working directory path, and works with paths with spaces (macOS)
typeset -r ShellCurDir=$(realpath "$PWD")

# Indicates whether the shell is interactive
typeset -r ShellInteractive=$([[ -o interactive ]] && echo 'true' || echo 'false')

# Indicates whether the shell is a login shell
typeset -r ShellLoginShell=$([[ -o login ]] && echo 'true' || echo 'false')

# Indicates whether the shell is running with job control enabled
typeset -r ShellJobControl=$([[ -o monitor ]] && echo 'true' || echo 'false')

# Indicates whether the shell is running with restricted mode enabled
typeset -r ShellRestricted=$([[ -o restricted ]] && echo 'true' || echo 'false')
```

### Zsh Specific Environment Variables

These variables are related specifically to the Zsh shell environment. They provide metadata and configuration details about the current Zsh shell session.

- **`$ZSH_VERSION`**: Contains the version number of the Zsh shell.
- **`$HISTFILE`**: Specifies the file where the command history is saved.
- **`$HISTSIZE`**: Defines the number of commands to remember in the command history.
- **`$SESSION_ID`**: Provides a unique identifier for the current Zsh session.
- **`$options`**: An array containing all the current options set in the shell.
- **`$module_path`**: Specifies the directories to search for Zsh modules.
- **`$fpath`**: Specifies the directories to search for Zsh function files.

```text
# Zsh version
typeset -r ZshVersion=$ZSH_VERSION

# Path to the history file
typeset -r ZshHistfile=$(realpath $HISTFILE)

# Size of the history file
typeset -r ZshHistsize=$HISTSIZE

# The current session ID
typeset -r ZshSessionId=$SESSION_ID

# Array of shell options
typeset -r ZshOptions=($options)

# Module search path
typeset -r ZshModulePath=$(realpath $module_path)

# Function search path
typeset -r ZshFpath=($fpath)
```

### Working Directory Information

These environment variables relate to the current working directory when the script is executed. The user's working directory may differ from the script's directory. Also, by default, when a non-interactive shell session starts, it inherits the working directory from the parent process that started it.

These variables technically could just be another prefixed by `User_` or `Shell_`, however, I use them a lot, so use the prefix `Workdir_`. As the working directory may change during script execution, I copy the working directory details to read-only variables, which allows the script to change directories and restore the initial working directory if needed.

Paths are normalized using `realpath` to resolve symbolic links and remove redundant slashes, ensuring consistency. If `realpath` is not available on your system, you may need to install it or use an alternative method to achieve similar functionality. On macOS, `realpath` is typically available.

- **`$PWD`**: Holds the current working directory.

```text
# Initial read-only absolute path of the current working directory
typeset -r WorkdirPathInit=$(realpath "$PWD")

# Initial read-only name of the current working directory
typeset -r WorkdirNameInit=$(basename "${(Q)$(realpath "$PWD")}")

# Working directory variables are is not read-only they can be changed during script execution
WorkDirPath=$WorkdirPathInit
WorkDirName=$WorkdirNameInit

# Read-only absolute path of the parent directory of the current working directory
typeset -r WorkdirParentDirInit=$(realpath "${(Q)${PWD:h}}")

# Read-only absolute path of a specific subdirectory in the current working directory
typeset -r WorkdirSubdir=$(realpath "$(pwd)/subdir")

# Read-only name of a specific subdirectory in the current working directory
typeset -r WorkdirSubdirName=subdir
```

### Script Environment

These variables provide metadata about the execution environment of the script itself. These they can't change during script execution,

These can't not change during script execution, there is no need for the `_Init` suffix. For safety I also initialize them as read-only to prevent further modification. I also use `realpath` to normalize these in case of symbolic links.

```text
# Read-only absolute path of the current script's directory
typeset -r ScriptDir=$(realpath ${0:A:h})

# Read-only name of the current script without the path
typeset -r ScriptName=${${0##*/}}

# Read-only absolute path of the current script
typeset -r ScriptPath=$(realpath ${0:A})

# Read-only absolute path of the parent directory of the current script's directory
typeset -r ScriptParentDir=$(realpath "${(Q)${0:A:h:h}}")

# Read-only name of the current script without path and extension
typeset -r ScriptBasename=${${0:A:t}%.*}

# Read-only name of the directory containing the current script
typeset -r ScriptDirname=$(basename "$(realpath "${0:A:h}")")

# Read-only extension of the current script
typeset -r ScriptExt=${0##*.}
```

### Caller Script Information

These variables capture information about the script that called the current script, if passed as arguments. They are read-only to preserve the original calling context.

```text
# Read-only name of the caller script (if passed as an argument)
typeset -r CallerName=$1

# Read-only directory of the caller script (if passed as an argument)
typeset -r CallerDir=$(realpath "${(Q)${1:h}}")

# Read-only absolute path of the caller script (if passed as an argument)
typeset -r CallerPath=$(realpath "$1")
```

### Process Information

These variables provide information about the current and parent processes. Since process IDs and names do not change during script execution, there is no need for the `_Init` suffix, but I do set them read-only for safety.

```text
# Read-only name of the current process
typeset -r ProcName=$(ps -o comm= -p "$$")

# Read-only name of the parent process
typeset -r ProcParentName=$(ps -o comm= -p "$PPID")

# Read-only parent process ID
typeset -r ProcParentId=$PPID

# Read-only name of the parent process
typeset -r ProcParentName=$(ps -o comm= -p $PPID)
```

### Script Arguments

_(This section needs to be rewritten for zparams and various ways to leverage parameters in a zsh array)_

These variables store the script's initial arguments as read-only, allowing derived or modified arguments to be read/write.

```text
# Initial read-only all arguments passed to the script as an array. I use the suffix _Init to keep the original arguements, as sometimes it is useful to edit the array.
typeset -r AllArgsArrayInit=("$@")
AllArgsArray=AllArgsArrayInit

# Initial read-only first argument passed to the script
typeset -r Arg1=$1

# Initial read-only second argument passed to the script
typeset -r Arg2=$2

# Initial read-only third argument passed to the script
typeset -r Arg3=$3
```

### Git Environment Variables (local and global)

These variables are related to the Git environment and can be both local and global. Local variables are specific to the current repository, while global variables are part of the user's global Git configuration.

**Local Variables (set for the current repository):**

```text
# Git directory for the current repository
typeset -r GitDirLocal=$(git rev-parse --git-dir)

# Working tree of the current repository
typeset -r GitWorkTreeLocal=$(git rev-parse --show-toplevel)

# Current HEAD commit hash
typeset -r GitHeadLocal=$(git rev-parse HEAD)
```

**Global Variables (global Git configuration):**

```text
# Path to the global Git configuration file
typeset -r GIT_CONFIG_GLOBAL=$HOME/.gitconfig

# Global Git user name
typeset -r GIT_USER_NAME_GLOBAL=$(git config --global user.name)

# Global Git user email
typeset -r GIT_USER_EMAIL_GLOBAL=$(git config --global user.email)
```

### Other Common Environment Variables

```text
# LOG_FILE_FULL_PATH: Ensures the log file path is absolute, normalizing it with realpath and handling spaces correctly.
LOG_FILE_FULL_PATH=$(realpath "${(Q)${ScriptDir}/${ScriptName}.log}")

# Temporary directory: Ensures the temporary directory path is absolute and correctly handles symbolic links and spaces.
TmpDir=$(realpath "${(Q)$(mktemp -d)}")

# Counters for loops
typeset Counter=0 # when a function is called with the Counter as a parameter
local counter=0 # when all the uses of the counter are in this function's context
local _inner_counter=0 # when the counter is inside a local function.

# Status flag
typeset Success=true

# Variable to store user input
local userInput=""
```

## Snippets of Code with Naming Conventions Applied

```text
# Function to log messages
log_Message() {
    local message=$1
    if [[ ! -f "$LOG_FILE_FULL_PATH" ]]; then
        touch "$LOG_FILE_FULL_PATH" || { echo "

Error: Cannot create log file"; exit 1; }
    fi
    echo "$(date): $message" >> "$LOG_FILE_FULL_PATH" || { echo "Error: Cannot write to log file"; exit 1; }
}

# Main script logic
log_Message "Script started in directory: $WorkDirPath"

# Example loop with counter
for file in "$WorkDirPath"/*; do
    Counter=$((Counter + 1))
    log_Message "Processing file $Counter: $file"
    # Example operation that might change the working directory
    if [[ -d $file ]]; then
        WorkDirPath=$file
        log_Message "Changed working directory to: $WorkDirPath"
    fi
done

log_Message "Script finished with $Counter files processed."
log_Message "Temporary files are stored in: $TmpDir"

# Clean up
rm -rf "$TmpDir"
log_Message "Temporary directory cleaned up."
```

```text
# Change to a specific directory and list its contents
cd $WorkDirPath
echo "Listing contents of $WorkDirPath:"
ls
```

### Logging Messages

```text
# Log a message to the log file
log_Message "This is a log entry"
```

#### Creating and Using a Temporary Directory

```text
# Capture existing EXIT traps
existing_trap=$(trap -p EXIT)
trap 'rm -rf "$TmpDir"; eval "$existing_trap"' EXIT
# Create a temporary directory and use it for temporary files
TmpDir=$(mktemp -d)
tmp_file=$(mktemp -p "$TmpDir")
echo "Temporary file created: $tmp_file"
```

#### Checking and Modifying Script Arguments

```text
# Check if the first argument is provided and modify it
if [[ -n $Arg1 ]]; then
    ModifiedArg1="${Arg1}_modified"
    echo "Modified argument: $ModifiedArg1"
else
    echo "No first argument provided."
fi
```

#### Caller Script Information Example

```text
# Assume this script is called with the caller script path as the first argument

typeset -r CallerName=$(basename "$1")
typeset -r CallerDir=$(dirname "$1")
typeset -r CallerPath=$(realpath "$1")

echo "Caller Script Name: $CallerName"
echo "Caller Script Directory: $CallerDir"
echo "Caller Script Full Path: $CallerPath"
```

#### Checking if Required Commands are Available:\*\*

```text
# Check if required commands are available
required_commands=("git" "realpath" "awk")
for cmd in "${required_commands[@]}"; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: Required command '$cmd' is not installed."
        exit 1
    fi
done
```

#### Handling Unexpected Input

```text
# Function to handle unexpected input
validate_Input() {
    local input=$1
    if [[ -z "$input" ]]; then
        echo "Error: Input cannot be empty."
        return 1
    fi
    if ! [[ "$input" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Error: Input contains invalid characters. Only alphanumeric, underscores, and hyphens are allowed."
        return 1
    fi
    return 0
}

# Example usage
validate_Input "$1" || exit 1
```

#### Ensuring Proper Cleanup

```text
# Ensure temporary files and directories are cleaned up properly
cleanup() {
    [[ -d "$TmpDir" ]] && rm -rf "$TmpDir"
    echo "Cleanup completed."
}

trap cleanup EXIT

# Main script logic here
```

## macOS and Zsh

### Misc

- It can be useful to configure Finder to default to open .sh scripts with the terminal, but of course they will be executed without any parameters.

- Some older versions of macOS don't have `realpath`. Here is a solution if you need to work on both legacy and current macOS.

```text
if ! command -v realpath &> /dev/null; then
    realpath() {
        [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
    }
fi
```

## To Be Continued

- \*\*Using Zsh `$fpath` for Function Libraries
  - Advice and demo
- **Zsh Script Template**:
  - Comprehensive Template for Zsh Command-Line Scripts
  - Uses Zsh Common Utiilities Libraries via `$fpath`
  - Includes functional test scripts
  - Demonstrates best practices
- **More on Avoiding Globals**
  - Some common overuse of global variables, and how to fix
  - How to use `setop warn_create_global` effectively
- **Error Handling and Debugging**:
  - Techniques for error handling in Zsh scripts.
  - Using `trap` for handling signals and cleaning up resources.
  - Debugging tools and practices (`set -x`, `print -v`).
- **Advanced Parameter Expansion**:
  - Techniques for advanced parameter expansion and manipulation.
  - Examples of using `${parameter//pattern/replacement}` and other parameter expansion features.
- **Working with Strings**:
  - Best practices for string manipulation in Zsh.
  - Examples of string operations (concatenation, substitution, slicing).
- **Working with Files and Directories**:
  - Techniques for handling files and directories (checking existence, permissions).
  - Examples of file and directory operations (copying, moving, deleting).
- **Function Libraries and Modularity**:
  - Best practices for organizing and reusing functions across scripts.
  - Techniques for creating and using function libraries.
- **Testing and Continuous Integration**:
  - Approaches to writing tests for Zsh scripts.
  - Integrating Zsh script testing into CI/CD pipelines.
- **Documentation and Comments**:
  - Guidelines for documenting Zsh scripts and functions.
  - Best practices for writing meaningful comments.
- **Performance Optimization**:
  - Tips for improving the performance of Zsh scripts.
  - Avoiding common pitfalls that can degrade performance.

## Early Drafts & Misc. To Integrate or Research

### Zsh Debugging Techniques

Zsh offers several powerful but lesser-known features for debugging scripts. Here are some useful techniques:

_**`TRAPDEBUG` Function**_

The `TRAPDEBUG` function in Zsh can be used to execute code before every command. This can be very useful for tracing execution and debugging:

```text
TRAPDEBUG() {
    echo "Executing: $ZSH_DEBUG_CMD"
}
```

A more sophisticated version:

```text
# Improved TRAPDEBUG function to trace function calls
TRAPDEBUG() {
    # Disable the trap to prevent recursion
    local trap_state=$TRAPDEBUG
    TRAPDEBUG=''

    # Log the current function and its caller if available
    if [[ -n "${funcstack[2]}" ]]; then
        echo "In function: ${funcstack[1]}, called from: ${funcstack[2]}"
    else
        echo "In function: ${funcstack[1]}"
    fi

    # Restore the trap
    TRAPDEBUG=$trap_state
}
```

_**`zsh -x` for Execution Trace**_

Running a script with `zsh -x` will print each command before it is executed, providing a detailed execution trace:

```text
zsh -x your_script.zsh
```

\* _**`set -x` and `set +x`**_

You can enable and disable execution tracing within a script using `set -x` and `set +x`:

```text
set -x  # Enable tracing
# Your code here
set +x  # Disable tracing
```

\* _**`$funcstack`**_

The `$funcstack` array provides a call stack of functions. You can use it to see the sequence of function calls leading to a particular point:

```text
echo "Function call stack:"
for ((i = 1; i <= ${#funcstack[@]}; i++)); do
    echo "Caller $i: ${funcstack[$i]}"
done
```

_**Verbose Debugging**_

Use a `verbose` flag to conditionally print debug information:

```text
verbose=1  # Set to 1 to enable verbose mode

if [[ -n $verbose ]]; then
    echo "Debugging info: variable = $variable"
fi
```

_**`autoload -U zsh/zprof`**_

Use `zprof` for profiling Zsh scripts to identify performance bottlenecks:

```text
# Enable profiling
zmodload zsh/zprof

# Your script here

# Print profiling results
zprof
```

_**`DEBUG` and `RETURN` Traps**_

You can set traps for `DEBUG` and `RETURN` to execute commands before and after each function:

```text
trap 'echo "Before command: $ZSH_DEBUG_CMD"' DEBUG
trap 'echo "Function $funcstack[1] returned with status $?."' RETURN
```

_**Conditional Breakpoints with `zshdb`**_

Use `zshdb`, a debugger for Zsh scripts, to set breakpoints and step through code:

```text
zshdb your_script.zsh
```

_**Using `typeset -p`**_

_**Inspect Variables with `typeset -p <var>`**_

Use `typeset` to inspect variables, especially associative arrays:

```text
typeset -p my_assoc_array
```

_**Inspect all variables with `typeset -p`**_

When you run `typeset -p` by itself in Zsh, it prints out the definitions of all variables, functions, and their attributes in the current shell environment. This includes simple variables, arrays, associative arrays, and functions. It's a comprehensive way to see the current state of the shell's environment.

_**Example Usage**_

Here’s how you might use `typeset -p` by itself and what you can expect:

```text
#!/bin/zsh

# Define some variables
my_var="Hello, World!"
my_array=("one" "two" "three")
typeset -A my_assoc_array
my_assoc_array[key1]="value1"
my_assoc_array[key2]="value2"

# Define a simple function
my_function() {
    echo "This is my function."
}

# Print the definitions of all variables and functions
typeset -p
```

_**Output**_

Running `typeset -p` by itself will produce output similar to the following:

```text
typeset my_var='Hello, World!'
typeset -a my_array=( 'one' 'two' 'three' )
typeset -A my_assoc_array=( [key1]="value1" [key2]="value2" )
typeset -f my_function
```

_**Explanation**_

- **Variables**: The output includes the definitions of all the variables in the current shell environment, showing their names, types, and values.
- **Arrays**: Both indexed arrays and associative arrays are displayed with their elements.
- **Functions**: Function definitions are also included, showing their names and indicating that they are functions with `typeset -f`.

### Using `typeset -p` in Scripts

Using `typeset -p` can be particularly useful for debugging and inspecting the state of your environment at various points in a script. For example, you might add `typeset -p` at critical points in your script to see how variables are changing over time.

```text
#!/bin/zsh

# Define some variables
my_var="Hello, World!"
my_array=("one" "two" "three")
typeset -A my_assoc_array
my_assoc_array[key1]="value1"
my_assoc_array[key2]="value2"

# Define a simple function
my_function() {
    echo "This is my function."
}

# Initial state
echo "Initial state of the environment:"
typeset -p

# Change a variable
my_var="Goodbye, World!"

# After changing a variable
echo "State of the environment after changing a variable:"
typeset -p
```

The output will show the initial state of all variables and functions, followed by the state after modifying a variable:

```text
Initial state of the environment:
typeset my_var='Hello, World!'
typeset -a my_array=( 'one' 'two' 'three' )
typeset -A my_assoc_array=( [key1]="value1" [key2]="value2" )
typeset -f my_function
State of the environment after changing a variable:
typeset my_var='Goodbye, World!'
typeset -a my_array=( 'one' 'two' 'three' )
typeset -A my_assoc_array=( [key1]="value1" [key2]="value2" )
typeset -f my_function
```

_**Conditional Command Logging**_

You can log commands conditionally based on certain conditions:

```text
function log_command {
    if [[ -n $verbose ]]; then
        echo "Running: $@"
    fi
    "$@"
}

log_command ls -l
```

_**Use `PS4` for Custom Debugging Prompts**_

Customize the debug prompt with `PS4` to include more information:

```text
export PS4='+${FUNCNAME[0]:-}:$LINENO: ${SECONDS}s: '
set -x
# Your script here
set +x
```

_**`xtrace` for Specific Commands**_

Use `xtrace` for specific commands rather than the entire script:

```text
xtrace() {
    set -x
    "$@"
    set +x
}

xtrace ls -l
```

_**Combining Techniques for Advanced Debugging**_

You can combine these techniques for more advanced debugging:

```text
verbose=1

TRAPDEBUG() {
    echo "Executing: $ZSH_DEBUG_CMD"
}

trap 'echo "Function $funcstack[1] returned with status $?."' RETURN

if [[ -n $verbose ]]; then
    set -x
fi

function example_function {
    local var="Hello, World!"
    echo $var
}

example_function

if [[ -n $verbose ]]; then
    set +x
fi
```

### Misc

```text
    # Log the process hierarchy
    echo "Process hierarchy:"
    ps -o ppid,pid,command | grep -E "^ *$(ps -o ppid= -p $$) *"
```

```text
    # Print the definitions of all functions
    echo "Function definitions:"
    typeset -f
```

```text
    # Log the current environment variables
    echo "Environment variables:"
    env
```

```text
# Scoped Flags for verbose and debug output
typeset -i verbose=0
typeset -i debug=0

# Initialize an scoped associative array to store trap commands
typeset -A TrapCommands

#---------------------------------------------------------------
# Function:    script_Cleanup
# Description: Cleans up temporary files and resources.
# Arguments:   None
# Globals:
#   - TEST_FILE_PATH: Path to the temporary test key file.
#---------------------------------------------------------------
script_Cleanup() {
    if [[ $debug -eq 1 ]]; then
        # Print the call stack
        echo "Function call stack:"
        # Loop through the funcstack array from 1 to the length of funcstack
        for ((i = 1; i <= ${#funcstack[@]}; i++)); do
            echo "Caller $i: ${funcstack[$i]}"
        done
    fi

    if [[ -f "$TEST_FILE_PATH" ]]; then
        rm "$TEST_FILE_PATH"
        if [[ $verbose -eq 1 ]]; then
            echo "Test file removed."
        fi
        echo "Test file removed."
    fi
    # Reset flags
    unset debug verbose
}

#---------------------------------------------------------------
# Function:    add_Trap
# Description: Adds a new command to an existing trap or creates a new trap
# Arguments:
#   - new_cmd: The new command to add to the trap.
#   - signal: The signal for which the trap should be set.
# Globals:     None
# Usage:
#   add_Trap "command_to_add" "SIGNAL"
# Examples:
#   add_Trap test_Script_Cleanup "EXIT"
#   add_Trap test_Script_Cleanup "ERR"
#---------------------------------------------------------------
add_Trap() {
    local new_Cmd=$1
    local signal=$2

    # Initialize the command list for the signal if it doesn't exist
    if [[ -z ${TrapCommands[$signal]} ]]; then
        TrapCommands[$signal]=$new_Cmd
    else
        TrapCommands[$signal]="${TrapCommands[$signal]}; $new_Cmd"
    fi

    # Set the combined trap command
    trap "${TrapCommands[$signal]}" "$signal"

    # Print debugging output if verbose mode is enabled
    if [[ $debug -eq 1 ]]; then
        echo "Adding trap for signal: $signal"
        echo "New command: $new_Cmd"
        echo "Combined command: ${trap_commands[$signal]}"
        # Print the definition of the associative array
        typeset -p trap_commands
    fi
}

# Set the trap to call script_Cleanup function on EXIT and ERR for the main script
if [[ "${0##*/}" == "$_SCRIPT_TEMPLATE_TEST_SCRIPT_NAME" ]]; then
    add_Trap "script_Cleanup" EXIT
fi
```

[Sign up for free](https://gist.github.com/join?source=comment-gist) **to join this conversation on GitHub**.
Already have an account?
[Sign in to comment](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2FChristopherA%2F562c2e62d01cf60458c5fa87df046fbd)

You can’t perform that action at this time.

---

### 5. GitHub - bahamas10/bash-style-guide: A style guide for writing safe, predictable, and portable bash scripts (not sh!)

**Source:** [https://github.com/bahamas10/bash-style-guide](https://github.com/bahamas10/bash-style-guide)
**Domain:** `github.com`
**Quality Score:** 20

_A style guide for writing safe, predictable, and portable bash scripts (not sh!) - bahamas10/bash-style-guide_

A style guide for writing safe, predictable, and portable bash scripts (not sh!)

[style.ysap.sh](https://style.ysap.sh/ "https://style.ysap.sh")

[**1** Branch](https://github.com/bahamas10/bash-style-guide/branches) [**0** Tags](https://github.com/bahamas10/bash-style-guide/tags)

## Bash Style Guide

This guide outlines how to write bash scripts with a style that makes them safe
and predictable. This guide is written by [Dave Eddy](https://daveeddy.com/) as
part of the YSAP (You Suck at Programming) series [ysap.sh](https://ysap.sh/) and
is the working document for how I approach bash scripting when it comes to
style, design, and best-practices.

## Preface

This guide will try to be as objective as possible, providing reasoning for why
certain decisions were made. For choices that are purely aesthetic (and may
not be universally agreeable) they will exist in the `Aesthetics` section
below.

Though good style alone won't ensure that your scripts are free from error, it
can certainly help narrow the scope for bugs to exist. This guide attempts to
explicitly state my style choices instead of implicitly relying on a sense or a
"vibe" of how code should be written.

## Aesthetics

### Tabs / Spaces

Tabs.

### Columns

Not to exceed 80.

### Semicolons

Avoid using semicolons in scripts unless required in control statements (e.g.,
if, while).

```text
# wrong
name='dave';
echo "hello $name";

# right
name='dave'
echo "hello $name"
```

The exception to this rule is outlined in the `Block Statements` section below.
Namely, semicolons should be used for control statements like `if` or `while`.

### Functions

Don't use the `function` keyword. All variables created in a function should
be made local.

```text
# wrong
function foo {
    i=foo # this is now global, wrong depending on intent
}

# right
foo() {
    local i=foo # this is local, preferred
}
```

### Block Statements

`then` should be on the same line as `if`, and `do` should be on the same line
as `while`.

```text
# wrong
if true
then
    ...
fi

# also wrong, though admittedly looks kinda cool
true && {
    ...
}

# right
if true; then
    ...
fi
```

### Spacing

No more than 2 consecutive newline characters (ie. no more than 1 blank line in
a row).

### Comments

No explicit style guide for comments. Don't change someones comments for
aesthetic reasons unless you are rewriting or updating them.

---- * *

## Bashisms

This style guide is for bash. This means when given the choice, always prefer
bash builtins or keywords instead of external commands or `sh(1)` syntax.

### `test(1)`

Use `[[ ... ]]` for conditional testing, not `[ .. ]` or `test ...`

```text
# wrong
test -d /etc

# also wrong
[ -d /etc ]

# correct
[[ -d /etc ]]
```

See [BashFAQ031](http://mywiki.wooledge.org/BashFAQ/031) for more information
about these.

### Sequences

Use bash builtins for generating sequences

```text
n=10

# wrong
for f in $(seq 1 5); do
    ...
done

# wrong
for f in $(seq 1 "$n"); do
    ...
done

# right
for f in {1..5}; do
    ...
done

# right
for ((i = 0; i < n; i++)); do
    ...
done
```

- [YSAP052](https://ysap.sh/v/52/)
- [YSAP053](https://ysap.sh/v/53/)

### Command Substitution

Use `$(...)` for command substitution.

```text
foo=`date`  # wrong
foo=$(date) # right
```

- [YSAP022](https://ysap.sh/v/22/)

### Math / Integer Manipulation

Use `((...))` and `$((...))`.

```text
a=5
b=4

# wrong
if [[ $a -gt $b ]]; then
    ...
fi

# right
if ((a > b)); then
    ...
fi
```

Do **not** use the `let` command.

### Parameter Expansion

Always prefer parameter expansion over external commands like `echo`, `sed`,
`awk`, etc.

```text
name='bahamas10'

# wrong
prog=$(basename "$0")
nonumbers=$(echo "$name" | sed -e 's/[0-9]//g')

# right
prog=${0##*/}
nonumbers=${name//[0-9]/}
```

- [YSAP026](https://ysap.sh/v/26/)
- [YSAP056](https://ysap.sh/v/56/)

### Listing Files

Do not [parse ls(1)](http://mywiki.wooledge.org/ParsingLs), instead use
bash builtin functions to loop files

```text
# very wrong, potentially unsafe
for f in $(ls); do
    ...
done

# right
for f in *; do
    ...
done
```

- [YSAP001](https://ysap.sh/v/1/)

### Determining path of the executable (`__dirname`)

Simply stated, you can't know this for sure. If you are trying to find out the
full path of the executing program, you should rethink your software design.

See [BashFAQ028](http://mywiki.wooledge.org/BashFAQ/028) for more information

For a case study on `__dirname` in multiple languages see my blog post

[Dirname Case\\
Study](http://daveeddy.com/2015/04/13/dirname-case-study-for-bash-and-node/)

### Arrays and lists

Use bash arrays instead of a string separated by spaces (or newlines, tabs,
etc.) whenever possible

```text
# wrong
modules='json httpserver jshint'
for module in $modules; do
    npm install -g "$module"
done

# right
modules=(json httpserver jshint)
for module in "${modules[@]}"; do
    npm install -g "$module"
done
```

Of course, in this example it may be better expressed as:

```text
npm install -g "${modules[@]}"
```

... only if the command supports multiple arguments and you are not interested
in catching individual failures.

- [YSAP020](https://ysap.sh/v/20)
- [Arrays explained in 7 minutes](https://www.youtube.com/watch?v=asHJ-xfuyno)

### read builtin

Use the bash `read` builtin whenever possible to avoid forking external
commands

Example

```text
fqdn='computer1.daveeddy.com'

IFS=. read -r hostname domain tld <<< "$fqdn"
echo "$hostname is in $domain.$tld"
# => "computer1 is in daveeddy.com"
```

---- * *

## External Commands

### GNU userland tools

The whole world doesn't run on GNU or on Linux; avoid GNU specific options
when forking external commands like `awk`, `sed`, `grep`, etc. to be as
portable as possible.

When writing bash and using all the powerful tools and builtins bash gives you,
you'll find it rare that you need to fork external commands to do simple string
manipulation.

- [YSAP029](https://ysap.sh/v/29/)

### Useless Use of Cat Award

Don't use `cat(1)` when you don't need it. If programs support reading from
stdin, pass the data in using bash redirection.

```text
# wrong
cat file | grep foo

# right
grep foo < file

# also right
grep foo file
```

Prefer using a command line tools builtin method of reading a file instead of
passing in stdin. This is where we make the inference that, if a program says
it can read a file passed by name, it's probably more performant to do that.

- [UUOC](http://www.smallo.ruhr.de/award.html)

---- * *

## Style

### Quoting

Use double quotes for strings that require variable expansion or command
substitution interpolation, and single quotes for all others.

```text
# right
foo='Hello World'
bar="You are $USER"

# wrong
foo="hello world"

# possibly wrong, depending on intent
bar='You are $USER'
```

All variables that will undergo word-splitting _must_ be quoted (1). If no
splitting will happen, the variable may remain unquoted.

```text
foo='hello world'

if [[ -n $foo ]]; then   # no quotes needed:
                         # [[ ... ]] won't word-split variable expansions

    echo "$foo"          # quotes needed
fi

bar=$foo  # no quotes needed - variable assignment doesn't word-split
```

1. The only exception to this rule is if the code or bash controls the variable
   for the duration of its lifetime. For example code like this:

```text
printf_date_supported=false
if printf '%()T' &>/dev/null; then
    printf_date_supported=true
fi

if $printf_date_supported; then
    ...
fi
```

Even though `$printf_date_supported` undergoes word-splitting in the `if`
statement in that example, quotes are not used because the contents of that
variable are controlled explicitly by the programmer and not taken from a user
or command.

Also, variables like `$$`, `$?`, `$#`, etc. don't required quotes because they
will never contain spaces, tabs, or newlines.

When in doubt; [quote all expansions](http://mywiki.wooledge.org/Quotes).

- [YSAP021](https://ysap.sh/v/21/)

### Variable Declaration

Avoid uppercase variable names unless there's a good reason to use them.
Don't use `let` or `readonly` to create variables. `declare` should _only_
be used for associative arrays. `local` should _always_ be used in functions.

```text
# wrong
declare -i foo=5
let foo++
readonly bar='something'
FOOBAR=baz

# right
i=5
((i++))
bar='something'
foobar=baz
```

### shebang

Bash is not always located at `/bin/bash`, so use this line:

```text
#!/usr/bin/env bash
```

Unless you’re intentionally targeting a specific environment (e.g. `/bin/bash`
on Linux servers with restricted PATHs).

### Error Checking

`cd`, for example, doesn't always work. Make sure to check for any possible
errors for `cd` (or commands like it) and exit or break if they are present.

```text
# wrong
cd /some/path # this could fail
rm file       # if cd fails where am I? what am I deleting?

# right
cd /some/path || exit
rm file
```

### Using `set -e`

Don't set `errexit`. Like in C, sometimes you want an error, or you expect
something to fail, and that doesn't necessarily mean you want the program
to exit.

This is a controversial opinion that I have on the surface, but the link below
will show situations where `set -e` can do more harm than good because of its
implications.

- [BashFAQ105](http://mywiki.wooledge.org/BashFAQ/105)

### Using `eval`

Never.

It opens your code to code injection and makes static analysis impossible.
Almost every use-case can be solved more safely with arrays, indirect expansion,
or proper quoting.

---- * *

## Common Mistakes

### Using {} instead of quotes

Using `${f}` is potentially different than `"$f"` because of how word-splitting
is performed. For example.

```text
for f in '1 space' '2  spaces' '3   spaces'; do
    echo ${f}
done
```

yields:

```text
1 space
2 spaces
3 spaces
```

Notice that it loses the amount of spaces. This is due to the fact that the
variable is expanded and undergoes word-splitting because it is unquoted. This
loop results in the 3 following commands being executed:

```text
echo 1 space
echo 2  spaces
echo 3   spaces
```

The extra spaces are effectively ignored here and only 2 arguments are passed
to the `echo` command in all 3 invocations.

If the variable was quoted instead:

```text
for f in '1 space' '2  spaces' '3   spaces'; do
    echo "$f"
done
```

yields:

```text
1 space
2  spaces
3   spaces
```

The variable `$f` is expanded but doesn't get split at all by bash, so it is
passed as a single string (with spaces) to the `echo` command in all 3
invocations.

Note that, for the most part `$f` is the same as `${f}` and `"$f"` is the same
as `"${f}"`. The curly braces should only be used to ensure the variable name
is expanded properly. For example:

```text
$ echo "$HOME is $USERs home directory"
/home/dave is  home directory
$ echo "$HOME is ${USER}s home directory"
/home/dave is daves home directory
```

The braces in this example were the difference of `$USER` vs `$USERs` being
expanded.

### Abusing for-loops when while would work better

`for` loops are great for iteration over arguments, or arrays. Newline
separated data is best left to a `while read -r ...` loop.

```text
users=$(awk -F: '{print $1}' /etc/passwd)
for user in $users; do
    echo "user is $user"
done
```

This example reads the entire `/etc/passwd` file to extract the usernames into
a variable separated by newlines. The `for` loop is then used to iterate over
each entry.

This approach has a lot of issues if used on other files with data that may
contain spaces or tabs.

1. This reads _all_ usernames into memory, instead of processing them in a
   streaming fashion.
2. If the first field of that file contained spaces or tabs, the for loop would
   break on that as well as newlines.
3. This only works _because_`$users` is unquoted in the `for` loop - if
   variable expansion only works for your purposes while unquoted this is a good
   sign that something isn't implemented correctly.

To rewrite this:

```text
while IFS=: read -r user _; do
    echo "$user is user"
done < /etc/passwd
```

This will read the file in a streaming fashion, not pulling it all into memory,
and will break on colons extracting the first field and discarding (storing as
the variable `_`) the rest - using nothing but bash builtin commands.

- [YSAP038](https://ysap.sh/v/38/)

---- * *

## References

- [YSAP](https://ysap.sh/)
- [BashGuide](https://mywiki.wooledge.org/BashGuide)
- [BashPitFalls](http://mywiki.wooledge.org/BashPitfalls)
- [Bash Practices](http://mywiki.wooledge.org/BashGuide/Practices)

## Get This Guide

- `curl style.ysap.sh` \- View this guide in your terminal.
- `curl style.ysap.sh/plain` \- View this guide without color in your terminal.
- `curl style.ysap.sh/md` \- Get the raw markdown.
- [Website](https://style.ysap.sh/) \- Dedicated website for this guide.
- [GitHub](https://github.com/bahamas10/bash-style-guide) \- View the source.

## License

MIT License

## About

A style guide for writing safe, predictable, and portable bash scripts (not sh!)

[style.ysap.sh](https://style.ysap.sh/ "https://style.ysap.sh")

### Topics

[style-guide](https://github.com/topics/style-guide "Topic: style-guide") [bash-scripting](https://github.com/topics/bash-scripting "Topic: bash-scripting") [ysap](https://github.com/topics/ysap "Topic: ysap")

### Resources

[Readme](https://github.com/bahamas10/bash-style-guide#readme-ov-file)

[Activity](https://github.com/bahamas10/bash-style-guide/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fbahamas10%2Fbash-style-guide&report=bahamas10+%28user%29)

## Languages

- [CSS72.5%](https://github.com/bahamas10/bash-style-guide/search?l=css)
- [Shell25.5%](https://github.com/bahamas10/bash-style-guide/search?l=shell)
- [Makefile2.0%](https://github.com/bahamas10/bash-style-guide/search?l=makefile)

You can’t perform that action at this time.

---

### 6. GitHub - PacktPublishing/Bash-Quick-Start-Guide: Bash Quick Start Guide, published by Packt

**Source:** [https://github.com/PacktPublishing/Bash-Quick-Start-Guide](https://github.com/PacktPublishing/Bash-Quick-Start-Guide)
**Domain:** `github.com`
**Quality Score:** 20

_Bash Quick Start Guide, published by Packt. Contribute to PacktPublishing/Bash-Quick-Start-Guide development by creating an account on GitHub._

Bash Quick Start Guide, published by Packt

### License

[MIT license](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/blob/master/LICENSE)

[**1** Branch](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/branches) [**0** Tags](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/tags)

## Bash Quick Start Guide

[![Bash Quick Start Guide](https://camo.githubusercontent.com/b02184d0e149c2bf14e6ef03e280f5b93e8562ca14cfd023aea6d6df0893aced/68747470733a2f2f7777772e7061636b747075622e636f6d2f73697465732f64656661756c742f66696c65732f393738313738393533383833302e706e67)](https://www.packtpub.com/virtualization-and-cloud/bash-quick-start-guide?utm_source=github&utm_medium=repository&utm_campaign=9781789538830)

This is the code repository for [Bash Quick Start Guide](https://www.packtpub.com/virtualization-and-cloud/bash-quick-start-guide?utm_source=github&utm_medium=repository&utm_campaign=9781789538830), published by Packt.

**Get up and running with shell scripting with Bash**

## What is this book about?

Bash and shell script programming is central to using Linux, but it has many peculiar properties that are hard to understand and unfamiliar to many programmers, with a lot of misleading and even risky information online. Bash Quick Start Guide tackles these problems head on, and shows you the best practices of shell script programming.

This book covers the following exciting features:

- Understand where the Bash shell fits in the system administration and programming worlds
- Use the interactive Bash command line effectively
- Get to grips with the structure of a Bash command line
- Master pattern-matching and transforming text with Bash
- Filter and redirect program input and output

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1789538831) today!

[![https://www.packtpub.com/](https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png)](https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner)

## Instructions and Navigations

All of the code is organized into folders. For example, Chapter02.

The code will look like the following:

```text
#!/bin/bash
printf 'Starting script\n' >> log
printf 'Creating test directory\n' >> log
mkdir test || exit
printf 'Changing into test directory\n' >> log
cd test || exit
printf 'Writing current date\n' >> log
date > date || exit
```

**Following is what you need for this book:**
People who use the command line on Unix and Linux servers already, but don't write primarily in Bash. This book is ideal for people who've been using a scripting language such as Python, JavaScript or PHP, and would like to understand and use Bash more effectively.

With the following software and hardware list you can run all code files present in the book (Chapter 1-8).

### Software and Hardware List

| Chapter | Software required | OS required |
| --- | --- | --- |
| 1-8 | Bash 4.0 or newer | GNU/Linux (recommended), Mac OS X, or BSD |

We also provide a PDF file that has color images of the screenshots/diagrams used in this book. [Click here to download it](http://www.packtpub.com/sites/default/files/downloads/9781789538830_ColorImages.pdf).

### Related products

- Penetration Testing with the Bash shell [\[Packt\]](https://www.packtpub.com/networking-and-servers/penetration-testing-bash-shell?utm_source=github&utm_medium=repository&utm_campaign=9781849695107) [\[Amazon\]](https://www.amazon.com/dp/1849695105)

- Bash Cookbook [\[Packt\]](https://www.packtpub.com/application-development/bash-cookbook?utm_source=github&utm_medium=repository&utm_campaign=9781788629362) [\[Amazon\]](https://www.amazon.com/dp/1788629361)

## Get to Know the Author

**Tom Ryder**
is a systems administrator living in New Zealand who works for an internet services provider. He loves terminals, text editors, network monitoring and security, Unix and GNU/Linux, shell script, and programming in general. He is also the author of the Nagios Core Administration Cookbook.

## Other books by the authors

- [Nagios Core Administration Cookbook](https://www.packtpub.com/networking-and-servers/nagios-core-administration-cookbook?utm_source=github&utm_medium=repository&utm_campaign=9781849515566)
- [Nagios Core Administration Cookbook - Second Edition](https://www.packtpub.com/networking-and-servers/nagios-core-administration-cookbook-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781785889332)

### Suggestions and Feedback

[Click here](https://docs.google.com/forms/d/e/1FAIpQLSdy7dATC6QmEL81FIUuymZ0Wy9vH1jHkvpY57OiMeKGqib_Ow/viewform) if you have any feedback or suggestions.

### Download a free PDF

_If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost._

_Simply click on the link to claim your free PDF._

[https://packt.link/free-ebook/9781789538830](https://packt.link/free-ebook/9781789538830)

## About

Bash Quick Start Guide, published by Packt

### Resources

[Readme](https://github.com/PacktPublishing/Bash-Quick-Start-Guide#readme-ov-file)

### License

[MIT license](https://github.com/PacktPublishing/Bash-Quick-Start-Guide#MIT-1-ov-file)

[Activity](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/activity)

[Custom properties](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/custom-properties)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FPacktPublishing%2FBash-Quick-Start-Guide&report=PacktPublishing+%28user%29)

## [Releases](https://github.com/PacktPublishing/Bash-Quick-Start-Guide/releases)

No releases published

## [Packages\  0](https://github.com/orgs/PacktPublishing/packages?repo_name=Bash-Quick-Start-Guide)

No packages published

You can’t perform that action at this time.

---

### 7. GitHub - djeada/Bash-Scripts: 100+ Bash scripts for automating routine tasks and streamlining your workflow

**Source:** [https://github.com/djeada/Bash-Scripts](https://github.com/djeada/Bash-Scripts)
**Domain:** `github.com`
**Quality Score:** 20

_100+ Bash scripts for automating routine tasks and streamlining your workflow. - djeada/Bash-Scripts_

100+ Bash scripts for automating routine tasks and streamlining your workflow.

[adamdjellouli.com/articles/linux\_notes](https://adamdjellouli.com/articles/linux_notes "https://adamdjellouli.com/articles/linux_notes")

### License

[MIT license](https://github.com/djeada/Bash-Scripts/blob/master/LICENSE)

[![GitHub stars](https://camo.githubusercontent.com/b323926bc2758ea65726ce3a88c7d714b77a9b1321074efe7514ba148c5f00b6/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f646a656164612f426173682d73637269707473)](https://github.com/djeada/Bash-scripts/stargazers)[![GitHub forks](https://camo.githubusercontent.com/0bff15b8d8734523fb2fb73ba87af565be7a01bc317de8ce1b95ab532cbaf9cd/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f666f726b732f646a656164612f426173682d73637269707473)](https://github.com/djeada/Bash-scripts/network)[![GitHub license](https://camo.githubusercontent.com/4f32f2232b7f4b5c479898b2b9666ed69ee9edc0ba799b8f16d03e64c7523cf2/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f646a656164612f426173682d73637269707473)](https://github.com/djeada/Bash-scripts/blob/master/LICENSE)[![contributions welcome](https://camo.githubusercontent.com/9e93e892d0685e1bf7a1d0bd7c8410d6ecf2086a0a7b48dd58a6b96fa556ea2a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f6e747269627574696f6e732d77656c636f6d652d627269676874677265656e2e7376673f7374796c653d666c6174)](https://github.com/djeada/Bash-Scripts/blob/master)

## Bash-scripts

A collection of Bash scripts for automating routine tasks and streamlining your workflow. From simple file renaming to more complex deployments, these Bash scripts have you covered.

[![Screenshot](https://user-images.githubusercontent.com/37275728/186024435-7edf1be2-ca64-4841-98bf-d07cbb362715.png)](https://user-images.githubusercontent.com/37275728/186024435-7edf1be2-ca64-4841-98bf-d07cbb362715.png)

## About Bash

Bash (Bourne Again SHell) is an essential component of Unix-like operating systems. It's a powerful scripting language and command interpreter that has evolved from its predecessors in the Unix world. Here's an overview:

### Historical Background

The origin of scripting languages can be traced back to their initial role as enhancements to command interpreters within operating systems. These early scripting tools were designed to automate repetitive tasks, streamline workflows, and improve the efficiency of system administration.

One of the first significant developments in this area was the creation of the **Bourne Shell (sh)** in the 1970s. Developed by Stephen Bourne at AT&T’s Bell Labs, it became the standard command interpreter for Unix systems, setting the foundation for future shell environments with its powerful scripting capabilities and control structures.

Building upon the Bourne Shell’s framework, the **Bash (Bourne Again SHell)** was introduced in 1989 as part of the GNU Project. Designed as a free software replacement for the Bourne Shell, Bash incorporated numerous enhancements, including improved scripting features, better error handling, and additional programming constructs. Today, Bash is the most widely used Unix shell, favored for its versatility and robust functionality across Unix-like operating systems, including Linux and macOS.

In addition to Bash, several other Unix shells have been developed over time, each offering unique features tailored to different user preferences and system requirements. These include the **C Shell (csh)**, which introduced C-like syntax; the **TENEX C Shell (tcsh)**, an enhanced version of csh with improved interactive features; the lightweight **Dash (Debian Almquist Shell)**, optimized for speed and minimal resource usage; the **Korn Shell (ksh)**, known for its advanced scripting capabilities and compatibility with both Bourne and C shell syntax; and the highly customizable **Z Shell (zsh)**, which combines features from multiple shells and offers extensive configurability for power users.

### Purpose of Shell Scripts

- Shell scripts are invaluable for repetitive command sequences by **automating** tasks, particularly in programming and server administration, especially for file and directory operations, text processing, and network configuration.
- Bash and other scripting languages incorporate features like variables, conditional statements, loops, arrays, and functions, providing more **sophisticated** control flow.
- The true strength of shell scripting lies in its ability to **utilize** the vast array of Unix commands.
- When scripts become overly complex for Bash, transitioning to more powerful languages like **Python** is advisable.
- Bash scripts can be used to integrate or 'glue' together complex scripts written in languages such as **Python**.

### Limitations of Bash

- Bash is not well-suited for developing **complex** applications.
- It's not designed for building **GUI** applications.
- Bash scripts may not be **portable** across different operating systems without modification.
- It's less efficient for **complex** calculations compared to languages like Python.
- Bash has limitations in handling advanced **network** programming tasks.

### "Hello World" in Bash

A basic example of a Bash script is the famous "Hello World". It demonstrates how to output text to the console.

```text
#!/usr/bin/env bash
echo "Hello world"
```

### Executing a script

To execute a Bash script, you need to make it executable and then run it from the terminal. Here's how you can do it:

```text
chmod u+x filename.sh  # Make the script executable
./filename.sh          # Execute the script
```

### The Shebang

The shebang (`#!`) line at the beginning of a script is crucial for defining the script's interpreter. It's more than just a convention; it's an essential aspect of script execution in Unix-like systems. Here's an expanded view:

Example Shebang for Bash:

```text
#!/usr/bin/env bash
```

Execution Contexts

- When a script is executed directly from a terminal, the shebang's specified **interpreter** is used. Example: `./filename.sh`
- If the script is invoked from another shell script, the parent script's **interpreter** is used, and the shebang in the child script is ignored.
- When a script is executed with an explicit interpreter command (like `bash ./filename.sh`), the shebang line is **bypassed**.

Shebang in Other Languages

- The shebang is not limited to Bash scripts, as it is used in various scripting languages to specify their respective **interpreters**.
- An example of a shebang for Perl is `#!/usr/bin/env perl`.
- An example of a shebang for Python is `#!/usr/bin/env python3`.

### Variables

Variables in Bash are not just simple placeholders for values; they can be used in more complex ways:

- To assign a value to a **variable**, you use `var="Test"`.
- To retrieve the value stored in a variable, you use `$var` or `${var}`.
- Bash supports explicitly defining variable types such as integers and **arrays**.

```text
declare -i var    # 'var' is an integer
declare -a arr    # 'arr' is an array
declare -r var2=5 # 'var2' is a read-only variable
```

- Bash allows storing the output of a command in a **variable** using command substitution, like `var=$(whoami)`.
- Environment variables are global and can be accessed by any process running in the shell **session**, such as `PATH`, `HOME`, and `USER`.
- To make a variable available to child processes, it needs to be **exported** using `export var`.
- Variables in functions can be made local to avoid affecting the global **scope**.

```text
function myFunc() {
    local localVar="value"
}
```

### Command Line Arguments in Bash

Command line arguments in Bash scripts are accessed using special variables:

- `$1` represents the first **argument** passed to the script.
- `$@` is an array-like construct that holds all command line **arguments**.
- `$#` gives the number of command line arguments **passed**.
- `$?` contains the exit status of the last executed **command**.

### If Statements in Bash

If statements in Bash are crucial for decision-making processes based on conditions.

Basic Syntax:

```text
if [ condition ]; then
  # commands
fi
```

- **Integer Comparisons**: Use specific operators for comparing integer values.

```text
if [ $i -eq 10 ]; then echo True; fi  # Integer comparison
```

- **String Comparisons**: Strings are compared differently from integers.

```text
if [ "$name" == "10" ]; then echo True; fi  # String comparison
```

Operators for Integer Comparison

| Operator | Description |
| --- | --- |
| `-eq` | equal |
| `-ne` | not equal |
| `-gt` | greater than |
| `-ge` | greater than or equal to |
| `-lt` | less than |
| `-le` | less than or equal to |

Operators for String Comparison

| Operator | Description |
| --- | --- |
| `==` | equal |
| `!=` | not equal |
| `>` | greater than |
| `<` | less than |
| `-n` | string is not null |
| `-z` | string is null |

Single vs Double Square Brackets:

- Single brackets `[ ]` are compatible with POSIX shell and suitable for basic **tests**.
- Double brackets `[[ ]]` are used in Bash and other shells like Zsh and Ksh to offer enhanced test **constructs**.

  - They support logical operators like `||` and regex matching with `=~`.
  - They do not perform word splitting or filename **expansion**.

Filename Expansion Example:

- No Globbing with Double Brackets:

```text
if [[ -f *.csv ]]; then echo True; fi  # Checks for a file named "*.csv"
```

- Globbing with Single Brackets:

```text
if [ -f *.csv ]; then echo True; fi  # Performs filename expansion
```

### Loops

Loops are used in Bash to execute a series of commands multiple times. There are several types of loops, each serving different purposes.

#### For Loop

The `for` loop is used to iterate over a list of items or a range of values.

Syntax:

```text
for var in list; do
  # commands
done
```

Example with a List:

```text
for i in 1 2 3; do
  echo $i
done
```

Example with a Range:

```text
for i in {1..3}; do
  echo $i
done
```

Example with Command Output:

```text
for file in $(ls); do
  echo $file
done
```

#### While Loop

The while loop executes as long as a specified condition is true.

Syntax:

```text
while [ condition ]; do
  # commands
done
```

Example:

```text
i=1
while [ $i -le 3 ]; do
  echo $i
  ((i++))
done
```

#### Until Loop

The until loop is similar to the while loop but runs until a condition becomes true.

Syntax:

```text
until [ condition ]; do
  # commands
done
```

Example:

```text
i=1
until [ $i -gt 3 ]; do
  echo $i
  ((i++))
done
```

#### Loop Control: Break and Continue

- **break**: Exits the loop.

```text
for i in 1 2 3 4 5; do
  if [ $i -eq 3 ]; then
    break
  fi
  echo $i
done
```

- **continue**: Skips the rest of the loop iteration and continues with the next one.

```text
for i in 1 2 3 4 5; do
  if [ $i -eq 3 ]; then
    continue
  fi
  echo $i
done
```

#### C-Style For Loop

Bash also supports a C-style syntax for for loops, which provides more control over the iteration process.

Syntax:

```text
for (( initialisation; condition; increment )); do
  # commands
done
```

Example:

```text
for (( i=1; i<=3; i++ )); do
  echo $i
done
```

### Arrays

An array is a variable that holds an ordered list of values. The values are separated by spaces. The following example creates an array named `array` and assigns the values 1, 2, 3, 4, 5 to it:

```text
array=(1 2 3 4 5)
```

It is possible to create an array with specified element indices:

```text
array=([3]='elem_a' [4]='elem_b')
```

To insert an elementat (e.g. 'abc') at a given index (e.g. 2) in the array, use the following syntax:

```text
array=("${array[@]:0:2}" 'new' "${array[@]:2}")
```

To iterate over the elements of an array, use the following syntax:

```text
items=('item_1' 'item_2' 'item_3' 'item_4')

for item in "${items[@]}"; do
  echo "$item"
done
# => item_1
# => item_2
# => item_3
# => item_4
```

It is often useful to print the elements of an array on a single line. The following code will print the elements of the array on a single line:

```text
echo "${array[*]}"
```

### Functions

Functions are used to group a sequence of commands into a single unit. They are used to perform repetitive tasks. Functions can be called from anywhere in the script. The following example creates a function named `hello_world` that prints the string `Hello World` to the standard output (stdout):

```text
hello_world()
{
  echo "Hello World!"
}
```

To call the function, use the following syntax:

```text
hello_world
```

The above function does not take any arguments and does not explicitly return a value. It is possible to pass any number of arguments to the function. It is also possible to return a value from the function, but only an integer from range \[0,255\] is allowed.

Here is a complete example of a script that defines and uses a function to sum two numbers:

```text
#!/usr/bin/env bash

sum_two()
{
    return $(($1 + $2))
}

sum_two 5 3
echo $?
```

### Pipes

The pipe is used to pass the output of one command as input to the next:

```text
ps -x | grep chromium
```

### Redirections

But what if you'd want to save the results to a file? Bash has a redirect operator > that may be used to control where the output is delivered.

```text
some_command > out.log            # Redirect stdout to out.log
some_command 2> err.log           # Redirect stderr to file err.log
some_command 2>&1                 # Redirect stderr to stdout
some_command 1>/dev/null 2>&1     # Silence both stdout and stderr
```

Complete summary:

| Syntax | StdOut visibility | StdErr visibility | StdOut in file | StdErr in file | existing file |
| --- | --- | --- | --- | --- | --- |
| `>` | no | yes | yes | no | overwrite |
| `>>` | no | yes | yes | no | append |
| `2>` | yes | no | no | yes | overwrite |
| `2>>` | yes | no | no | yes | append |
| `&>` | no | no | yes | yes | overwrite |
| `&>>` | no | no | yes | yes | append |
| `tee` | yes | yes | yes | no | overwrite |
| `tee -a` | yes | yes | yes | no | append |
| `n.e. (*)` | yes | yes | no | yes | overwrite |
| `n.e. (*)` | yes | yes | no | yes | append |
| `|& tee` | yes | yes | yes | yes | overwrite |
| `|& tee -a` | yes | yes | yes | yes | append |

### Formatting and linting

It is important to keep the formatting of your script as consistent as possible. [Beautysh](https://github.com/lovesegfault/beautysh) is an amazing tool that helps you to format your script. To use it, just run the following command in a directory where your scripts are located:

```text
beautysh **/*.sh
```

Additionally we advise to use [shellcheck](https://github.com/koalaman/shellcheck) for code inspection.

```text
shellcheck **/*.sh
```

## Available scripts

### Intro

| # | Description | Code |
| --- | --- | --- |
| 1 | Prints "Hello, world!" to the console. | [hello\_world.sh](https://github.com/djeada/Bash-scripts/blob/master/src/hello_world.sh) |
| 2 | Demonstrates the use of if statements to check conditions. | [conditionals.sh](https://github.com/djeada/Bash-scripts/blob/master/src/conditionals.sh) |
| 3 | Shows the use of a while loop to repeatedly execute code. | [while\_loop.sh](https://github.com/djeada/Bash-scripts/blob/master/src/while_loop.sh) |
| 4 | Demonstrates the use of a for loop to iterate over elements. | [for\_loop.sh](https://github.com/djeada/Bash-scripts/blob/master/src/for_loop.sh) |
| 5 | Displays the digits of a given number, one digit per line. | [digits.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/digits.sh) |
| 6 | Prints all of the numbers within a specified range, one number per line. | [numbers\_in\_interval.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/numbers_in_interval.sh) |
| 7 | Prints a Christmas tree pattern to the console. | [christmas\_tree.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/christmas_tree.sh) |
| 8 | Prompts the user for a response to a given question and stores their response in a variable. | [prompt\_for\_answer.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/prompt_for_answer.sh) |

### Math

| # | Description | Code |
| --- | --- | --- |
| 1 | Performs basic arithmetic operations (addition, subtraction, multiplication, and division) on two numbers. | [arithmetic\_operations.sh](https://github.com/djeada/Bash-scripts/blob/master/src/arithmetic_operations.sh) |
| 2 | Calculates the sum of all the arguments passed to it, treating them as numbers. | [sum\_args.sh](https://github.com/djeada/Bash-scripts/blob/master/src/sum_args.sh) |
| 3 | Converts a number from the decimal (base 10) system to its equivalent in the binary (base 2) system. | [decimal\_binary.sh](https://github.com/djeada/Bash-scripts/blob/master/src/decimal_binary.sh) |
| 4 | Calculates the factorial of a given integer. | [factorial.sh](https://github.com/djeada/Bash-scripts/blob/master/src/factorial.sh) |
| 5 | Determines whether a given number is a prime number or not. | [is\_prime.sh](https://github.com/djeada/Bash-scripts/blob/master/src/is_prime.sh) |
| 6 | Calculates the square root of a given number. | [sqrt.sh](https://github.com/djeada/Bash-scripts/blob/master/src/sqrt.sh) |

### Strings

| # | Description | Code |
| --- | --- | --- |
| 1 | Counts the number of times a specific character appears in a given string. | [count\_char.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/count_char.sh) |
| 2 | Converts all uppercase letters in a given string to lowercase. | [lower.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/lower.sh) |
| 3 | Converts all lowercase letters in a given string to uppercase. | [upper.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/upper.sh) |
| 4 | Checks if a given string is a palindrome, i.e., a word that is spelled the same way forwards and backwards. | [is\_palindrome.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/is_palindrome.sh) |
| 5 | Checks if two given strings are anagrams, i.e., if they are made up of the same letters rearranged in a different order. | [are\_anagrams.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/are_anagrams.sh) |
| 6 | Calculates the Hamming Distance between two strings, i.e., the number of positions at which the corresponding characters are different. | [hamming\_distance.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/hamming_distance.sh) |
| 7 | Sorts a given string alphabetically, considering all letters to be lowercase. | [sort\_string.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/sort_string.sh) |
| 8 | Creates a word histogram. | [word\_histogram.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/word_histogram.sh) |

### Arrays

| # | Description | Code |
| --- | --- | --- |
| 1 | Calculates the arithmetic mean of a given list of numbers. | [arith\_mean.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/arith_mean.sh) |
| 2 | Finds the maximum value in a given array of numbers. | [max\_array.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/max_array.sh) |
| 3 | Finds the minimum value in a given array of numbers. | [min\_array.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/min_array.sh) |
| 4 | Removes duplicates from a given array of numbers. | [remove\_duplicates\_in\_array.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/remove_duplicates_in_array.sh) |

### Files

| # | Description | Code |
| --- | --- | --- |
| 1 | Counts the number of files in a specified directory. | [count\_files.sh](https://github.com/djeada/Bash-scripts/blob/master/src/count_files.sh) |
| 2 | Creates a new directory with a specified name. | [make\_dir.sh](https://github.com/djeada/Bash-scripts/blob/master/src/make_dir.sh) |
| 3 | Counts the number of lines in a specified text file. | [line\_counter.sh](https://github.com/djeada/Bash-scripts/blob/master/src/line_counter.sh) |
| 4 | Gets the middle line from a specified text file. | [middle\_line.sh](https://github.com/djeada/Bash-scripts/blob/master/src/middle_line.sh) |
| 5 | Removes duplicate lines from a specified file. | [remove\_duplicate\_lines.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/remove_duplicate_lines.sh) |
| 6 | Replaces all forward slashes with backward slashes and vice versa in a specified file. | [switch\_slashes.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/switch_slashes.sh) |
| 7 | Adds specified text to the beginning of a specified file. | [prepend\_text\_to\_file.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/prepend_text_to_file.sh) |
| 8 | Removes all lines in a specified file that contain only whitespaces. | [remove\_empty\_lines.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/remove_empty_lines.sh) |
| 9 | Renames all files in a specified directory with a particular extension to a new extension. | [rename\_extension.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/rename_extension.sh) |
| 10 | Strips digits from every string found in a given file. | [strip\_digits.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/strip_digits.sh) |
| 11 | Lists the most recently modified files in a given directory. | [recently\_modified\_files.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/recently_modified_files.sh) |

### System administration

| # | Description | Code |
| --- | --- | --- |
| 1 | Retrieves basic system information, such as hostname and kernel version. | [system\_info.sh](https://github.com/djeada/Bash-scripts/blob/master/src/system_info.sh) |
| 2 | Determines the type and version of the operating system running on the machine. | [check\_os.sh](https://github.com/djeada/Bash-scripts/blob/master/src/check_os.sh) |
| 3 | Checks whether the current user has root privileges. | [check\_if\_root.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/check_if_root.sh) |
| 4 | Checks if the apt command, used for package management on Debian-based systems, is available on the machine. | [check\_apt\_avail.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/check_apt_avail.sh) |
| 5 | Retrieves the size of the machine's random access memory (RAM). | [ram\_memory.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/ram_memory.sh) |
| 6 | Gets the current temperature of the machine's central processing unit (CPU). | [cpu\_temp.sh](https://github.com/djeada/Bash-scripts/blob/master/src/cpu_temp.sh) |
| 7 | Retrieves the current overall CPU usage of the machine. | [cpu\_usage.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/cpu_usage.sh) |
| 8 | Blocks certain websites from being visited on the local machine by modifying the hosts file. | [web\_block.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/web_block.sh) |
| 9 | Creates a backup of the system's files, compresses the backup, and encrypts the resulting archive for storage. | [backup.sh](https://github.com/djeada/Bash-scripts/blob/master/src/backup.sh) |
| 10 | Displays processes that are not being waited on by any parent process. Orphan processes are created when the parent process terminates. | [orphans.sh](https://github.com/djeada/Bash-scripts/blob/master/src/orphans.sh) |
| 11 | Displays processes that are in an undead state, also known as a "zombie" state. Zombie processes have completed execution but remain in the process table. | [zombies.sh](https://github.com/djeada/Bash-scripts/blob/master/src/zombies.sh) |

### Programming workflow

| # | Description | Code |
| --- | --- | --- |
| 1 | Removes the carriage return character (`\r`) from the given files, which may be present in files transferred between systems with different line ending conventions. | [remove\_carriage\_return.sh](https://github.com/djeada/Bash-scripts/blob/master/src/remove_carriage_return.sh) |
| 2 | Replaces all characters with diacritical marks in the given files with their non-diacritical counterparts. Diacritical marks are small signs added above or below letters to indicate different pronunciations or tones in some languages. | [remove\_diacritics.sh](https://github.com/djeada/Bash-scripts/blob/master/src/remove_diacritics.sh) |
| 3 | Changes all spaces in file names to underscores and converts them to lowercase. This can be useful for making the file names more compatible with systems that do not support spaces in file names or for making the file names easier to read or type. | [correct\_file\_names.sh](https://github.com/djeada/Bash-scripts/blob/master/src/correct_file_names.sh) |
| 4 | Removes any trailing whitespace characters (spaces or tabs) from the end of every file in a given directory. Trailing whitespace can cause formatting issues or interfere with certain tools and processes. | [remove\_trailing\_whitespaces.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/remove_trailing_whitespaces.sh) |
| 5 | Formats and beautifies every shell script found in the current repository. This can make the scripts easier to read and maintain by adding consistent indentation and whitespace. | [beautify\_script.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/beautify_script.sh) |
| 6 | Finds functions and classes in a Python project that are not being used or called anywhere in the code. This can help identify and remove unnecessary code, which can improve the project's performance and maintainability. | [dead\_code.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/dead_code.sh) |

### Git

| # | Description | Code |
| --- | --- | --- |
| 1 | Resets the local repository to match the state of the remote repository, discarding any local commits and changes. This can be useful for starting over or synchronizing with the latest version on the remote repository. | [reset\_to\_origin.sh](https://github.com/djeada/Bash-scripts/blob/master/src/reset_to_origin.sh) |
| 2 | Deletes the specified branch both locally and on the remote repository. This can be useful for removing branches that are no longer needed or for consolidating multiple branches into a single branch. | [remove\_branch.sh](https://github.com/djeada/Bash-scripts/blob/master/src/remove_branch.sh) |
| 3 | Counts the total number of lines of code in a git repository, including lines in all branches and commits. This can be useful for tracking the size and complexity of a project over time. | [count\_lines\_of\_code.sh](https://github.com/djeada/Bash-scripts/blob/master/src/count_lines_of_code.sh) |
| 4 | Combines multiple commits into a single commit. This can be useful for simplifying a commit history or for cleaning up a series of small, incremental commits that were made in error. | [squash\_n\_last\_commits.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/squash_n_last_commits.sh) |
| 5 | Removes the `n` last commits from the repository. This can be useful for undoing mistakes or for removing sensitive information that was accidentally committed. | [remove\_n\_last\_commits.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/remove_n_last_commits.sh) |
| 6 | Changes the date of the last commit in the repository. This can be useful for altering the commit history for cosmetic purposes. | [change\_commit\_date.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/change_commit_date.sh) |
| 7 | Downloads all of the public repositories belonging to a specified user on GitHub. This can be useful for backing up repositories. | [download\_all\_github\_repos.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/download_all_github_repos.sh) |
| 8 | Squashes all commits on a specified Git branch into a single commit. | [squash\_branch.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/squash_branch.sh) |
| 9 | Counts the total lines changed by a specific author in a Git repository. | [contributions\_by\_git\_author.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/contributions_by_git_author.sh) |

### Utility

| # | Description | Code |
| --- | --- | --- |
| 1 | Finds the public IP address of the device running the script. | [ip\_info.sh](https://github.com/djeada/Bash-scripts/blob/master/src/ip_info.sh) |
| 2 | Deletes all files in the trash bin. | [empty\_trash.sh](https://github.com/djeada/Bash-scripts/blob/master/src/empty_trash.sh) |
| 3 | Extracts files with a specified extension from a given directory. | [extract.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/extract.sh) |
| 4 | Determines which programs are currently using a specified port number on the local system. | [program\_on\_port.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/program_on_port.sh) |
| 5 | Converts month names to numbers and vice versa in a string. For example, "January" to "1" and "1" to "January". | [month\_to\_number.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/month_to_number.sh) |
| 6 | Creates command aliases for all the scripts in a specified directory, allowing them to be run by simply typing their names. | [alias\_all\_the\_scripts.sh](https://github.com/djeada/Bash-scripts/blob/master/src/alias_all_the_scripts.sh) |
| 7 | Generates a random integer within a given range. The range can be specified as arguments to the script. | [rand\_int.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/rand_int.sh) |
| 8 | Generates a random password of the specified length, using a combination of letters, numbers, and special characters. | [random\_password.sh](https://github.com/djeada/Bash-Scripts/blob/master/src/random_password.sh) |
| 9 | Measures the time it takes to run a program with the specified input parameters. Output the elapsed time in seconds. | [time\_execution.sh](https://github.com/djeada/Bash-scripts/blob/master/src/time_execution.sh) |
| 10 | Downloads the audio from a YouTube video or playlist in MP3 format. Specify the video or playlist URL and the destination directory for the downloaded files. | [youtube\_to\_mp3.sh](https://github.com/djeada/Bash-scripts/blob/master/src/youtube_to_mp3.sh) |
| 11 | Clears the local caches in the user's cache directory (e.g. `~/.cache`) that are older than a specified number of days. | [clear\_cache.sh](https://github.com/djeada/Bash-scripts/blob/master/src/clear_cache.sh) |
| 12 | Resizes all JPG files in the current directory to a specified dimension (A4). | [resize\_to\_a4](https://github.com/djeada/Bash-Scripts/edit/master/src/resize_to_a4.sh) |

## References

### Official Documentation

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/bash.html): The official documentation for GNU Bash, detailing built-in commands, syntax, and features.
- [Linux Documentation Project](https://www.tldp.org/): Comprehensive collection of HOWTOs, guides, and FAQs for Linux users and administrators.

### Guides and Tutorials

- [Bash Guide by Greg's Wiki](http://mywiki.wooledge.org/BashGuide): An excellent resource for learning Bash scripting, written in an approachable and detailed manner.
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/): A thorough guide for mastering advanced Bash scripting techniques and best practices.
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/): In-depth explanations and tips for Bash scripting, focusing on practical usage and pitfalls.

### Learning Platforms

- [Codecademy's Learn the Command Line](https://www.codecademy.com/learn/learn-the-command-line): An interactive platform for beginners to learn basic command line skills.
- [edX's Linux Foundation Courses](https://www.edx.org/school/linuxfoundationx): Online courses covering various aspects of Linux, including command line proficiency and system administration.

### Community and Support

- [Unix & Linux Stack Exchange](https://unix.stackexchange.com/): A Q&A site for users of Linux, FreeBSD, and other Un\*x-like operating systems.
- [Reddit's r/bash](https://www.reddit.com/r/bash/): A subreddit dedicated to discussions and questions about Bash scripting and shell programming.

### Tools and Utilities

- [ShellCheck](https://www.shellcheck.net/): An online tool that helps you find and fix bugs in your shell scripts.
- [Explainshell](https://explainshell.com/): A web application that breaks down complex command lines into simple explanations.
- [Oh My Zsh](https://ohmyz.sh/): A framework for managing your Zsh configuration, making it easier to customize your shell.

### Books

- "Learning the bash Shell" by Cameron Newham: A comprehensive guide to Bash programming, suitable for beginners and experienced users alike.
- "Linux Command Line and Shell Scripting Bible" by Richard Blum and Christine Bresnahan: A detailed book covering Linux command line and shell scripting from the basics to advanced topics.
- "Bash Cookbook" by Carl Albing, JP Vossen, and Cameron Newham: A collection of useful Bash scripting recipes for various tasks and problems.

### Blogs and Articles

- [Linux Journal's Bash Articles](https://www.linuxjournal.com/tag/bash): A series of articles covering various Bash scripting topics and tips.
- [DigitalOcean's Bash Tutorials](https://www.digitalocean.com/community/tutorial_series/understanding-bash): Tutorials and guides to help you understand and use Bash effectively.
- [Bash-One-Liners Explained](https://www.bashoneliners.com/): A collection of Bash one-liners, with explanations on how they work and when to use them.

## How to Contribute

We encourage contributions that enhance the repository's value. To contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the [MIT License](https://github.com/djeada/Bash-Scripts/blob/master/LICENSE) \- see the LICENSE file for details.

## Star History

[![Star History Chart](https://camo.githubusercontent.com/083743e89875a288a3aabe94797a08a0b694e518da4da21e9a0c70b2c16e5f72/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d646a656164612f426173682d5363726970747326747970653d44617465)](https://star-history.com/#djeada/Bash-Scripts&Date)

## About

100+ Bash scripts for automating routine tasks and streamlining your workflow.

[adamdjellouli.com/articles/linux\_notes](https://adamdjellouli.com/articles/linux_notes "https://adamdjellouli.com/articles/linux_notes")

### Topics

[shell](https://github.com/topics/shell "Topic: shell") [bash](https://github.com/topics/bash "Topic: bash") [unix](https://github.com/topics/unix "Topic: unix") [scripting](https://github.com/topics/scripting "Topic: scripting") [shell-script](https://github.com/topics/shell-script "Topic: shell-script")

### Resources

[Readme](https://github.com/djeada/Bash-Scripts#readme-ov-file)

### License

[MIT license](https://github.com/djeada/Bash-Scripts#MIT-1-ov-file)

[Activity](https://github.com/djeada/Bash-Scripts/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fdjeada%2FBash-Scripts&report=djeada+%28user%29)

## [Releases](https://github.com/djeada/Bash-Scripts/releases)

No releases published

## [Packages\  0](https://github.com/users/djeada/packages?repo_name=Bash-Scripts)

No packages published

You can’t perform that action at this time.

---

### 8. Bash Pitfalls · GitHub

**Source:** [https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c)
**Domain:** `gist.github.com`
**Quality Score:** 20

_Bash Pitfalls. GitHub Gist: instantly share code, notes, and snippets._

[Gist Homepage](https://gist.github.com/)

Search Gists

Search Gists

[Gist Homepage](https://gist.github.com/)

[Sign in](https://gist.github.com/auth/github?return_to=https%3A%2F%2Fgist.github.com%2Fdsoares%2F7608d68538be606f3b6a6f0c557bfc8c) [Sign up](https://gist.github.com/join?return_to=https%3A%2F%2Fgist.github.com%2Fdsoares%2F7608d68538be606f3b6a6f0c557bfc8c&source=header-gist)

Instantly share code, notes, and snippets.

[![@dsoares](https://avatars.githubusercontent.com/u/673736?s=64&v=4)](https://gist.github.com/dsoares)

## [dsoares](https://gist.github.com/dsoares)/ **[BashPitfalls.md](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c)**

Last active
4 months agoJuly 8, 2025 19:22

Show Gist options

- [Download ZIP](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c/archive/c600d6cdbc2f12ad269b144f2a2833c1ae0fd3ae.zip)

- [Star2(2)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fdsoares%2F7608d68538be606f3b6a6f0c557bfc8c) You must be signed in to star a gist
- [Fork0(0)](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fdsoares%2F7608d68538be606f3b6a6f0c557bfc8c) You must be signed in to fork a gist

- Embed

## Select an option

- Embed

Embed this gist in your website.

- Share

Copy sharable link for this gist.

- Clone via HTTPS

Clone using the web URL.

## No results found

[Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

Clone this repository at &lt;script src=&quot;<https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c.js&quot;&gt;&lt;/script&gt>;

- Save dsoares/7608d68538be606f3b6a6f0c557bfc8c to your computer and use it in GitHub Desktop.

Embed

## Select an option

- Embed

Embed this gist in your website.

- Share

Copy sharable link for this gist.

- Clone via HTTPS

Clone using the web URL.

## No results found

[Learn more about clone URLs](https://docs.github.com/articles/which-remote-url-should-i-use)

Clone this repository at &lt;script src=&quot;<https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c.js&quot;&gt;&lt;/script&gt>;

Save dsoares/7608d68538be606f3b6a6f0c557bfc8c to your computer and use it in GitHub Desktop.

[Download ZIP](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c/archive/c600d6cdbc2f12ad269b144f2a2833c1ae0fd3ae.zip)

Bash Pitfalls

[Raw](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c/raw/c600d6cdbc2f12ad269b144f2a2833c1ae0fd3ae/BashPitfalls.md)

[**BashPitfalls.md**](https://gist.github.com/dsoares/7608d68538be606f3b6a6f0c557bfc8c#file-bashpitfalls-md)

Saved from [http://mywiki.wooledge.org/BashPitfalls?utm\_source=DigitalOcean\_Newsletter](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter)

## Bash Pitfalls

This page is a compilation of common mistakes made by bash users. Each example is flawed in some way.

Contents

01. [for f in $(ls \*.mp3)](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#for_f_in_.24.28ls_.2A.mp3.29)
02. [cp $file $target](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cp_.24file_.24target)
03. [Filenames with leading dashes](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#Filenames_with_leading_dashes)
04. [\[ $foo = "bar" \]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B_.24foo_.3D_.22bar.22_.5D)
05. [cd $(dirname "$f")](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cd_.24.28dirname_.22.24f.22.29)
06. [\[ "$foo" = bar && "$bar" = foo \]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B_.22.24foo.22_.3D_bar_.26.26_.22.24bar.22_.3D_foo_.5D)
07. [\[\[ $foo > 7 \]\]](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B.5B_.24foo_.3E_7_.5D.5D>)
08. [grep foo bar \| while read -r; do ((count++)); done](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#grep_foo_bar_.7C_while_read_-r.3B_do_.28.28count.2B-.2B-.29.29.3B_done)
09. [if \[grep foo myfile\]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#if_.5Bgrep_foo_myfile.5D)
10. [if \[bar="$foo"\]; then ...](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#if_.5Bbar.3D.22.24foo.22.5D.3B_then_...)
11. [if \[ \[ a = b \] && \[ c = d \] \]; then ...](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#if_.5B_.5B_a_.3D_b_.5D_.26.26_.5B_c_.3D_d_.5D_.5D.3B_then_>...)
12. [read $foo](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#read_.24foo)
13. [cat file \| sed s/foo/bar/ > file](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cat_file_.7C_sed_s.2Ffoo.2Fbar.2F_.3E_file)
14. [echo $foo](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#echo_.24foo)
15. [$foo=bar](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.24foo.3Dbar)
16. [foo = bar](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#foo_.3D_bar)
17. [echo <<EOF](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#echo_.3C.3CEOF)
18. [su -c 'some command'](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#su_-c_.27some_command.27)
19. [cd /foo; bar](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cd_.2Ffoo.3B_bar)
20. [\[ bar == "$foo" \]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B_bar_.3D.3D_.22.24foo.22_.5D)
21. [for i in {1..10}; do ./something &; done](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#for_i_in_.7B1..10.7D.3B_do_..2Fsomething_.26.3B_done)
22. [cmd1 && cmd2 \|\| cmd3](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cmd1_.26.26_cmd2_.7C.7C_cmd3)
23. [echo "Hello World!"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#echo_.22Hello_World.21.22)
24. [for arg in $\*](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#for_arg_in_.24.2A)
25. [function foo()](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#function_foo.28.29)
26. [echo "~"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#echo_.22.2BAH4.22)
27. [local var=$(cmd)](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#local_var.3D.24.28cmd.29)
28. [export foo=~/bar](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#export_foo.3D.2BAH4-.2Fbar)
29. [sed 's/$foo/good bye/'](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#sed_.27s.2F.24foo.2Fgood_bye.2F.27)
30. [tr \[A-Z\] \[a-z\]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#tr_.5BA-Z.5D_.5Ba-z.5D)
31. [ps ax \| grep gedit](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#ps_ax_.7C_grep_gedit)
32. [printf "$foo"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#printf_.22.24foo.22)
33. [for i in {1..$n}](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#for_i_in_.7B1...24n.7D)
34. [if \[\[ $foo = $bar \]\] (depending on intent)](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#if_.5B.5B_.24foo_.3D_.24bar_.5D.5D_.28depending_on_intent.29>)
35. [if \[\[ $foo =~ 'some RE' \]\]](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#if_.5B.5B_.24foo_.3D.2BAH4_.27some_RE.27_.5D.5D>)
36. [\[ -n $foo \] or \[ -z $foo \]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B_-n_.24foo_.5D_or_.5B_-z_.24foo_.5D)
37. [\[\[ -e "$broken\_symlink" \]\] returns 1 even though $broken\_symlink exists](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#A.5B.5B_-e_.22.24broken_symlink.22_.5D.5D_returns_1_even_though_.24broken_symlink_exists>)
38. [ed file <<<"g/d{0,3}/s//e/g" fails](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#ed_file_.3C.3C.3C.22g.2Fd.2BAFw.7B0.2C3.2BAFw.7D.2Fs.2F.2Fe.2Fg.22_fails)
39. [expr sub-string fails for "match"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#expr_sub-string_fails_for_.22match.22)
40. [On UTF-8 and Byte-Order Marks (BOM)](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#On_UTF-8_and_Byte-Order_Marks_.28BOM.29)
41. [content=$(<file)](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#content.3D.24.28.3Cfile.29)
42. [for file in ./\* ; do if \[\[ $file != _._ \]\]](<http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#for_file_in_..2F.2A_.3B_do_if_.5B.5B_.24file_.21.3D_.2A..2A_.5D.5D>)
43. [somecmd 2>&1 >>logfile](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#somecmd_2.3E.261_.3E.3Elogfile)
44. [cmd; (( ! $? )) \|\| die](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#cmd.3B_.28.28_.21_.24.3F_.29.29_.7C.7C_die)
45. [y=$(( array\[$x\] ))](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#y.3D.24.28.28_array.5B.24x.5D_.29.29)
46. [read num; echo $((num+1))](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#read_num.3B_echo_.24.28.28num.2B-1.29.29)
47. [IFS=, read -ra fields <<< "$csv\_line"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#IFS.3D.2C_read_-ra_fields_.3C.3C.3C_.22.24csv_line.22)
48. [export CDPATH=.:~/myProject](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#export_CDPATH.3D.:.2BAH4-.2FmyProject)
49. [OIFS="$IFS"; ...; IFS="$OIFS"](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#OIFS.3D.22.24IFS.22.3B_....3B_IFS.3D.22.24OIFS.22)
50. [hosts=( $(aws ...) )](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#hosts.3D.28_.24.28aws_....29_.29)
51. [Non-atomic writes with xargs -P](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#Non-atomic_writes_with_xargs_-P)
52. [find . -exec sh -c 'echo {}' ;](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#find_._-exec_sh_-c_.27echo_.7B.7D.27_.2BAFw.3B)
53. [sudo mycmd > /myfile](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#sudo_mycmd_.3E_.2Fmyfile)
54. [sudo ls /foo/\*](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#sudo_ls_.2Ffoo.2F.2A)
55. [myprogram 2>&-](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#myprogram_2.3E.26-)
56. [Using xargs without -0](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#Using_xargs_without_-0)
57. [unset a\[0\]](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#unset_a.5B0.5D)
58. [month=$(date +%m); day=$(date +%d)](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#month.3D.24.28date_.2B-.25m.29.3B_day.3D.24.28date_.2B-.25d.29)
59. [i=$(( 10#$i ))](http://mywiki.wooledge.org/BashPitfalls?utm_source=DigitalOcean_Newsletter#i.3D.24.28.28_10.23.24i_.29.29)

## 1\. for f in $(ls \*.mp3)

One of the most common mistakes [BASH](http://mywiki.wooledge.org/BASH) programmers make is to write a loop like this:

```text
for f in $(ls *.mp3); do    # Wrong!
    some command $f         # Wrong!
done

for f in $(ls)              # Wrong!
for f in `ls`               # Wrong!

for f in $(find . -type f)  # Wrong!
for f in `find . -type f`   # Wrong!

files=($(find . -type f))   # Wrong!
for f in ${files[@]}        # Wrong!
```

Yes, it would be great if you could just treat the output of `ls` or `find` as a list of filenames and iterate over it. But you **cannot**. This entire approach is fatally flawed, and there is no trick that can make it work. You must use an entirely different approach.

There are at least 6 problems with this:

1. If a filename contains whitespace, it undergoes [WordSplitting](http://mywiki.wooledge.org/WordSplitting). Assuming we have a file named `01 - Don't Eat the Yellow Snow.mp3` in the current directory, the `for` loop will iterate over each word in the resulting file name: _01_, _-_, _Don't_, _Eat_, etc.

2. If a filename contains [glob](http://mywiki.wooledge.org/glob) characters, it undergoes filename expansion (" [globbing](http://mywiki.wooledge.org/glob)"). If `ls` produces any output containing a \*\*\*\*\* character, the word containing it will become recognized as a pattern and substituted with a list of all filenames that match it.

3. If the command substitution returns multiple filenames, there is no way to tell where the first one ends and the second one begins. Pathnames may contain _any_ character except NUL. Yes, this includes newlines.

4. The `ls` utility may mangle filenames. Depending on which platform you're on, which arguments you used (or didn't use), and whether its standard output is pointing to a terminal or not, `ls` may randomly decide to replace certain characters in a filename with "?", or simply not print them at all. [Never try to parse the output of ls](http://mywiki.wooledge.org/ParsingLs). `ls` is just plain unnecessary. It's an external command whose output is intended specifically to be read by a human, not parsed by a script.

5. The [CommandSubstitution](http://mywiki.wooledge.org/CommandSubstitution) strips _all_ trailing newline characters from its output. That may seem desirable since `ls` adds a newline, but if the last filename in the list ends with a newline, `...` or `$()` will remove _that_ one also.

6. In the `ls` examples, if the first filename starts with a hyphen, it may lead to [pitfall #3](http://mywiki.wooledge.org/BashPitfalls#pf3).

You can't simply double-quote the substitution either:

```text
for f in "$(ls *.mp3)"; do     # Wrong!
```

This causes the entire output of `ls` to be treated as a single word. Instead of iterating over each file name, the loop will only execute _once_, assigning to `f` a string with all the filenames rammed together.

Nor can you simply change [IFS](http://mywiki.wooledge.org/IFS) to a newline. Filenames can also contain newlines.

Another variation on this theme is abusing word splitting and a `for` loop to (incorrectly) read lines of a file. For example:

```text
IFS=/pre>\n'
for line in $(cat file); do ...     # Wrong!
```

[This doesn't work](http://mywiki.wooledge.org/DontReadLinesWithFor)! Especially if those lines are filenames. Bash (or any other Bourne family shell) just doesn't work this way.

**So, what's the right way to do it?**

There are several ways, primarily depending on whether you need a recursive expansion or not.

If you don't need recursion, you can use a simple [glob](http://mywiki.wooledge.org/glob). Instead of `ls`:

```text
for file in ./*.mp3; do    # Better! and...
    some command "$file"   # ...always double-quote expansions!
done
```

POSIX shells such as Bash have the globbing feature specifically for this purpose -- to allow the shell to expand patterns into a list of matching filenames. There is no need to interpret the results of an external utility. Because globbing is the very last expansion step, each match of the `./*.mp3` pattern correctly expands to a separate word, and isn't subject to the effects of an unquoted expansion.

_Question:_ What happens if there are no _.mp3-files in the current directory? Then the for loop is executed once, with i="./_.mp3", which is not the expected behavior! The workaround is to test whether there is a matching file:

```text
# POSIX
for file in ./*.mp3; do
    [ -e "$file" ] || continue
    some command "$file"
done
```

Another solution is to use Bash's `shopt -s nullglob` feature, though this should only be done after reading the documentation and carefully considering the effect of this setting on all other globs in the script.

If you need recursion, the standard solution is `find`. When [using find](http://mywiki.wooledge.org/UsingFind), be sure you use it properly. For POSIX sh portability, use the `-exec` option:

```text
find . -type f -name '*.mp3' -exec some command {} \;

# Or, if the command accepts multiple input filenames:

find . -type f -name '*.mp3' -exec some command {} +
```

If you're using bash, then you have two additional options. One is to use GNU or BSD `find`'s `-print0` option, together with bash's `read -d ''` option and a [ProcessSubstitution](http://mywiki.wooledge.org/ProcessSubstitution):

```text
while IFS= read -r -d '' file; do
  some command "$file"
done < <(find . -type f -name '*.mp3' -print0)
```

The advantage here is that "some command" (indeed, the entire `while` loop body) is executed in the current shell. You can set variables and have them [persist after the loop ends](http://mywiki.wooledge.org/BashFAQ/024).

The other option, available in [Bash 4.0 and higher](http://mywiki.wooledge.org/BashFAQ/061), is `globstar`, which permits a glob to be expanded recursively:

```text
shopt -s globstar
for file in ./**/*.mp3; do
  some command "$file"
done
```

Note the double quotes around `$file` in the examples above. This leads to our second pitfall:

## 2\. cp $file $target

What's wrong with the command shown above? Well, nothing, **if** you happen to know in advance that `$file` and `$target` have no white space or [wildcards](http://mywiki.wooledge.org/glob) in them. However, the results of the expansions are still subject to [WordSplitting](http://mywiki.wooledge.org/WordSplitting) and [pathname expansion](http://mywiki.wooledge.org/glob). Always double-quote parameter expansions.

```text
cp -- "$file" "$target"
```

Without the double quotes, you'll get a command like `cp 01 - Don't Eat the Yellow Snow.mp3 /mnt/usb`, which will result in errors like ``cp: cannot stat `01': No such file or directory``. If `$file` has wildcards in it (\*\*\*\*\* or **?** or **\[**), they will be [expanded](http://mywiki.wooledge.org/glob) if there are files that match them. With the double quotes, all's well, unless "$file" happens to start with a `-`, in which case `cp` thinks you're trying to feed it command line options (See [pitfall #3](http://mywiki.wooledge.org/BashPitfalls#pf3) below.)\
\
Even in the somewhat uncommon circumstance that you can guarantee the variable contents, it is conventional and good practice to [quote](http://mywiki.wooledge.org/Quotes) parameter expansions, especially if they contain file names. Experienced script writers will always use [quotes](http://mywiki.wooledge.org/Quotes) except perhaps for a small number of cases in which it is _absolutely_ obvious from the immediate code context that a parameter contains a guaranteed safe value. Experts will most likely consider the `cp` command in the title always wrong. You should too.\
\

## 3\. Filenames with leading dashes\

\
\
Filenames with leading dashes can cause many problems. Globs like `*.mp3` are sorted into an expanded list (according to your current [locale](http://mywiki.wooledge.org/locale)), and `-` sorts before letters in most locales. The list is then passed to some command, which may incorrectly interpret the `-filename` as an option. There are two major solutions to this.\
\
One solution is to insert `--` between the command (like `cp`) and its arguments. That tells it to stop scanning for options, and all is well:\
\

```\
cp -- "$file" "$target"\
```\
\
There are potential problems with this approach. You have to be sure to insert `--` for _every_ usage of the parameter in a context where it might possibly be interpreted as an option -- which is easy to miss and may involve a lot of redundancy.\
\
Most well-written option parsing libraries understand this, and the programs that use them correctly should inherit that feature for free. However, still be aware that it is ultimately up to the application to recognize _end of options_. Some programs that manually parse options, or do it incorrectly, or use poor 3rd-party libraries may not recognize it. Standard utilities _should_, with a few exceptions that are specified by POSIX. `echo` is one example.\
\
Another option is to ensure that your filenames always begin with a directory by using relative or absolute pathnames.\
\
```\
for i in ./*.mp3; do\
    cp "$i" /target\
    ...\
done\
```\
\
In this case, even if we have a file whose name begins with `-`, the glob will ensure that the variable always contains something like `./-foo.mp3`, which is perfectly safe as far as `cp` is concerned.\
\
Finally, if you can guarantee that all results will have the same prefix, and are only using the variable a few times within a loop body, you can simply concatenate the prefix with the expansion. This gives a theoretical savings in generating and storing a few extra characters for each word.\
\
```\
for i in *.mp3; do\
    cp "./$i" /target\
    ...\
done\
```\
\

## 4\. \[ $foo = "bar" \]\

\
This is very similar to the issue in pitfall #2, but I repeat it because it's _so_ important. In the example above, the [quotes](http://mywiki.wooledge.org/Quotes) are in the wrong place. You do _not_ need to quote a string literal in bash (unless it contains metacharacters or pattern characters). But you _should_ quote your variables if you aren't sure whether they could contain white space or wildcards.\
\
This example can break for several reasons:\
\

- If a variable referenced in `[` doesn't exist, or is blank, then the `[` command would end up looking like:\
\
- ```\

[ = "bar" ] # Wrong!\
```\
\
- ...and will throw the error: `unary operator expected`. (The `=` operator is _binary_, not unary, so the `[` command is rather shocked to see it there.)\
\
- If the variable contains internal whitespace, then it gets [split into separate words](http://mywiki.wooledge.org/WordSplitting) before the `[` command sees it. Thus:\
\
- ```\
[ multiple words here = "bar" ]\
```\
\

- While that may look OK to you, it's a syntax error as far as `[` is concerned. The correct way to write this is:\
\
- ```\

## POSIX\

[ "$foo" = bar ] # Right!\
```\
\
- This works fine on POSIX-conformant implementations even if `$foo` begins with a `-`, because POSIX `[` determines its action depending on the number of arguments passed to it. Only very ancient shells have a problem with this, and you shouldn't worry about them when writing new code (see the `x"$foo"` workaround below).\
\
\
In Bash and many other ksh-like shells, there is a superior alternative which uses the \[\[ [keyword](http://mywiki.wooledge.org/BashFAQ/031).\
\
```\

## Bash / Ksh\

[[ $foo == bar ]] # Right!\
```\
\
You don't need to quote variable references on the left-hand side of `=` in `[[ ]]` because they don't undergo word splitting or [globbing](http://mywiki.wooledge.org/glob), and even blank variables will be handled correctly. On the other hand, quoting them won't hurt anything either. Unlike `[` and `test`, you may also use the identical `==`. Do note however that comparisons using `[[` perform pattern matching against the string on the right hand side, not just a plain string comparison. To make the string on the right literal, you must quote it if any characters that have special meaning in pattern matching contexts are used.\
\
```\

## Bash / Ksh\

match=b*r\
[[ $foo == "$match" ]] # Good! Unquoted would also match against the pattern b*r.\
```\
\
You may have seen code like this:\
\
```\

## POSIX / Bourne\

[ x"$foo" = xbar ] # Ok, but usually unnecessary.\
```\
\
The `x"$foo"` hack is required for code that must run on _very_ ancient shells which lack \[\[, and have a more primitive `[`, which gets confused if `$foo` begins with a `-`. On said older systems, `[` still doesn't care whether the token on the right hand side of the `=` begins with a `-`. It just uses it literally. It's just the left-hand side that needs extra caution.\
\
Note that shells that require this workaround are not POSIX-conforming. Even the Heirloom Bourne shell doesn't require this (probably the non-POSIX Bourne shell clone that's still most widely in use as a system shell). Such extreme portability is rarely a requirement and makes your code less readable (and uglier).\
\
## 5\. cd $(dirname "$f")\
\
\
This is yet another [quoting](http://mywiki.wooledge.org/Quotes) error. As with a variable expansion, the result of a [CommandSubstitution](http://mywiki.wooledge.org/CommandSubstitution) undergoes [WordSplitting](http://mywiki.wooledge.org/WordSplitting) and [pathname expansion](http://mywiki.wooledge.org/glob). So you should quote it:\
\
```\
cd -P -- "$(dirname -- "$f")"\
```\
\
What's not obvious here is how the [quotes](http://mywiki.wooledge.org/Quotes) nest. A C programmer reading this would expect the first and second double-quotes to be grouped together; and then the third and fourth. But that's not the case in Bash. Bash treats the double-quotes _inside_ the command substitution as one pair, and the double-quotes _outside_ the substitution as another pair.\
\
Another way of writing this: the parser treats the command substitution as a "nesting level", and the quotes inside it are separate from the quotes outside it.\
\
## 6\. \[ "$foo" = bar && "$bar" = foo \]\
\
You can't use `&&` inside the \[old test (or [) command](http://mywiki.wooledge.org/BashFAQ/031). The Bash parser sees `&&` outside of `[[ ]]` or `(( ))` and breaks your command into _two_ commands, before and after the `&&`. Use one of these instead:\
\
```\
[ bar = "$foo" ] && [ foo = "$bar" ] # Right! (POSIX)\
[[ $foo = bar && $bar = foo ]]       # Also right! (Bash / Ksh)\
```\
\
(Note that we reversed the constant and the variable inside `[` for the legacy reasons discussed in pitfall #4. We could also have reversed the `[[` case, but the expansions would require quoting to prevent interpretation as a pattern.) The same thing applies to `||`. Either use `[[` instead, or use two `[` commands.\
\
Avoid this:\
\
```\
[ bar = "$foo" -a foo = "$bar" ] # Not portable.\
```\
\
The binary `-a` and `-o`, and `(` / `)` (grouping) operators are XSI extensions to the POSIX standard. All are marked as obsolescent in POSIX-2008. They should not be used in new code. One of the practical problems with `[ A = B -a C = D ]` (or `-o`) is that [POSIX does not specify](http://www.opengroup.org/onlinepubs/9699919799/utilities/test.html) the results of a `test` or `[` command with more than 4 arguments. It probably works in most shells, but you can't count on it. If you have to write for POSIX shells, then you should use two `test` or `[` commands separated by a `&&` operator instead.\
\
## 7\. \[\[ $foo > 7 \]\]\
\
There are multiple issues here. First, the \[\[ [command](http://mywiki.wooledge.org/BashFAQ/031) should _not_ be used solely for evaluating [arithmetic expressions](http://mywiki.wooledge.org/ArithmeticExpression). It should be used for test expressions involving one of the supported test operators. Though technically you _can_ do math using some of `[[`'s operators, it only makes sense to do so in conjunction with one of the non-math test operators somewhere in the expression. If you just want to do a numeric comparison (or any other shell arithmetic), it is much better to just use `(( ))` instead:\
\
```\

## Bash / Ksh\

((foo > 7))     # Right!\
[[ foo -gt 7 ]] # Works, but is pointless. Most will consider it wrong. Use ((...)) or let instead.\
```\
\
If you use the `>` operator inside `[[ ]]`, it's treated as a string comparison (test for collation order by locale), _not_ an integer comparison. This may work sometimes, but it will fail when you least expect it. If you use `>` inside `[ ]`, it's even worse: it's an output redirection. You'll get a file named `7` in your directory, and the test will succeed as long as `$foo` is not empty.\
\
If strict POSIX-conformance is a requirement, and `((` is not available, then the correct alternative using old-style `[` is\
\
```\

## POSIX\

[ "$foo" -gt 7 ]       # Also right!\
[ $((foo > 7)) -ne 0 ] # POSIX-compatible equivalent to ((, for more general math operations.\
```\
\
Note that the `test ... -gt` command will fail in interesting ways if `$foo` is [not an integer](http://mywiki.wooledge.org/BashFAQ/054). Therefore, there's not much point in quoting it properly other than for performance and to confine the arguments to a single word to reduce the likelihood of obscure side-effects possible in some shells.\
\
If the input to any arithmetic context (including `((` or `let`), or `[` test expression involving numeric comparisons can't be guaranteed then you must _always_ [validate your input before evaluating the expression](http://mywiki.wooledge.org/BashFAQ/054).\
\
```\

## POSIX\

case $foo in\
    _[![:digit:]]_)\
```
printf '$foo expanded to a non-digit: %s\n' "$foo" >&2\        printf '$foo expanded to a non-digit: %s\n' "$foo" >&2\
        exit 1\
        ;;\
    *)\
        [ $foo -gt 7 ]\
esac\
```\
\
## 8\. grep foo bar \| while read -r; do ((count++)); done\
\
\
The code above looks OK at first glance, doesn't it? Sure, it's just a poor implementation of `grep -c`, but it's intended as a simplistic example. Changes to `count` won't propagate outside the `while` loop because each command in a pipeline is executed in a separate [SubShell](http://mywiki.wooledge.org/SubShell). This surprises almost every Bash beginner at some point.\
\
POSIX doesn't specify whether or not the last element of a pipeline is evaluated in a subshell. Some shells such as ksh93 and Bash >= 4.2 with `shopt -s lastpipe` enabled will run the `while` loop in this example in the original shell process, allowing any side-effects within to take effect. Therefore, portable scripts must be written in such a way as to not depend upon either behavior.\
\
For workarounds for this and similar issues, please see [Bash FAQ #24](http://mywiki.wooledge.org/BashFAQ/024). It's a bit too long to fit here.\
\
## 9\. if \[grep foo myfile\]\
\
Many beginners have an incorrect intuition about `if` statements brought about by seeing the very common pattern of an `if` keyword followed immediately by a `[` or `[[`. This convinces people that the `[` is somehow part of the `if` statement's syntax, just like parentheses used in C's `if` statement.\
\
This is _not_ the case! `if` takes a _command_. `[` is a command, not a syntax marker for the `if` statement. It's equivalent to the `test` command, except that the final argument must be a `]`. For example:\
\
```\

## POSIX\

if [ false ]; then echo "HELP"; fi\
if test false; then echo "HELP"; fi\
```\
\
are equivalent -- both checking that the argument "false" is non-empty. In both cases HELP will always be printed, to the surprise of programmers from other languages guessing about shell syntax.\
\
The syntax of an `if` statement is:\
\
```\
if COMMANDS\
then\
elif  # optional\
then\
else  # optional\
fi # required\
```\
\
Once again, `[` is a command. It takes arguments like any other regular _simple command_. `if` is a _compound command_ which contains other commands -- and **there is no \[** in its syntax!\
\
While bash has a builtin command `[` and thus `knows` about `[` it has nothing special to do with `]`. Bash only passes `]` as argument to the `[` command, which requires `]` to be the last argument only to make scripts look better.\
\
There may be zero or more optional `elif` sections, and one optional `else` section.\
\
The `if` compound command is made up of two or more sections containing _lists_ of commands, each delimited by a `then`, `elif`, or `else` keyword, and is terminated by the `fi` keyword. The exit status of the final command of the first section and each subsequent `elif` section determines whether each corresponding `then` section is evaluated. Another `elif` is evaluated until one of the `then` sections is executed. If no `then` section is evaluated, then the `else` branch is taken, or if no `else` is given, the `if` block is complete and the overall `if` command returns 0 (true).\
\
If you want to make a decision based on the output of a `grep` command, you do _not_ want to enclose it in parentheses, brackets, backticks, or _any other_ syntax! Just use `grep` as the `COMMANDS` after the `if`, like this:\
\
```\
if grep -q fooregex myfile; then\
...\
fi\
```\
\
If the `grep` matches a line from `myfile`, then the exit code will be 0 (true), and the `then` part will be executed. Otherwise, if there are no matches, `grep` will return non-zero and the overall `if` command will be zero.\
\
**See also:**\
\
- [BashGuide/TestsAndConditionals](http://mywiki.wooledge.org/BashGuide/TestsAndConditionals)\
\
- [http://wiki.bash-hackers.org/syntax/ccmd/if\_clause](http://wiki.bash-hackers.org/syntax/ccmd/if_clause)\
\
\
## 10\. if \[bar="$foo"\]; then ...\
\
```\
[bar="$foo"]   # Wrong!\
[ bar="$foo" ] # Still wrong!\
```\
\
As explained in the previous example, `[` is a command (which can be proven with `type -t [` or `whence -v [`). Just like with any other simple command, Bash expects the command to be followed by a space, then the first argument, then another space, etc. You can't just run things all together without putting the spaces in! Here is the correct way:\
\
```\
if [ bar = "$foo" ]; then ...\
```\
\
Each of `bar`, `=`, the expansion of `"$foo"`, and `]` is a separate [argument](http://mywiki.wooledge.org/Arguments) to the `[` command. There must be whitespace between each pair of arguments, so the shell knows where each argument begins and ends.\
\
## 11\. if \[ \[ a = b \] && \[ c = d \] \]; then ...\
\
Here we go again. `[` is a _command_. It is not a syntactic marker that sits between `if` and some sort of C-like "condition". Nor is it used for grouping. You cannot take C-like `if` commands and translate them into Bash commands just by replacing parentheses with square brackets!\
\
If you want to express a compound conditional, do this:\
\
```\
if [ a = b ] && [ c = d ]; then ...\
```\
\
Note that here we have two _commands_ after the `if`, joined by an `&&` (logical AND, shortcut evaluation) operator. It's precisely the same as:\
\
```\
if test a = b && test c = d; then ...\
```\
\
If the first `test` command returns false, the body of the `if` statement is not entered. If it returns true, then the second `test` command is run; and if that also one returns true, then the body of the `if` statement _will_ be entered. (C programmers are already familiar with `&&`. Bash uses the same _short-circuit evaluation_. Likewise `||` does short-circuit evaluation for the _OR_ operation.)\
\
The \[\[ [keyword](http://mywiki.wooledge.org/BashFAQ/031) _does_ permit the use of `&&`, so it could also be written this way:\
\
```\
if [[ a = b && c = d ]]; then ...\
```\
\
See [pitfall #6](http://mywiki.wooledge.org/BashPitfalls#pf6) for a pitfall related to _tests_ combined with conditional operators.\
\
## 12\. read $foo\
\
\
You don't use a `$` before the variable name in a `read` command. If you want to put data into the variable named `foo`, you do it like this:\
\
- ```\
read foo\
```\
\
\
Or more safely:\
\

- ```\

IFS= read -r foo\
```\
\
\
`read $foo` would read a line of input and put it in the variable(s) whose name(s) are in `$foo`. This might be useful if you actually intended `foo` to be a [reference](http://mywiki.wooledge.org/BashFAQ/006) to some other variable; but in the majority of cases, this is simply a bug.\
\
## 13\. cat file \| sed s/foo/bar/ > file\
\
\
You **cannot** read from a file and write to it in the same pipeline. Depending on what your pipeline does, the file may be clobbered (to 0 bytes, or possibly to a number of bytes equal to the size of your operating system's pipeline buffer), or it may grow until it fills the available disk space, or reaches your operating system's file size limitation, or your quota, etc.\
\
If you want to make a change to a file safely, other than appending to the end of it, use a text editor.\
\
- ```\
printf %s\\n ',s/foo/bar/g' w q | ed -s file\
```\
\
\
If you are doing something that cannot be done with a text editor there _must_ be a temporary file created at some point(\*). For example, the following is completely portable:\
\

- ```\

sed 's/foo/bar/g' file > tmpfile && mv tmpfile file\
```\
\
\
The following will _only_ work on GNU sed 4.x:\
\
- ```\
sed -i 's/foo/bar/g' file(s)\
```\
\
\
Note that this also creates a temporary file, and does the same sort of renaming trickery -- it just handles it transparently.\
\
And the following equivalent command requires perl 5.x:\
\

- ```\

perl -pi -e 's/foo/bar/g' file(s)\
```\
\
\
For more details on replacing contents of files, please see [Bash FAQ #21](http://mywiki.wooledge.org/BashFAQ/021).\
\
(\*) `sponge` from [moreutils](http://packages.debian.org/sid/moreutils) uses this example in its manual:\
\
- ```\
sed '...' file | grep '...' | sponge file\
```\
\
\
Rather than using a temporary file plus an atomic `mv`, this version "soaks up" (the actual description in the manual!) all the data, before opening and writing to the `file`. This version will cause data loss if the program or system crashes during the write operation, because there's no copy of the original file on disk at that point.\
\
Using a temporary file + `mv` still incurs a slight risk of data loss in case of a system crash / power loss; to be 100% certain that either the old or the new file will survive a power loss, you must use `sync` before the `mv`.\
\

## 14\. echo $foo\

\
\
This relatively innocent-looking command causes _massive_ confusion. Because the `$foo` isn't [quoted](http://mywiki.wooledge.org/Quotes), it will not only be subject to [WordSplitting](http://mywiki.wooledge.org/WordSplitting), but also file [globbing](http://mywiki.wooledge.org/glob). This misleads Bash programmers into thinking their variables _contain_ the wrong values, when in fact the variables are OK -- it's just the word splitting or filename expansion that's messing up their view of what's happening.\
\

- ```\

msg="Please enter a file name of the form *.zip"\
echo $msg\
```\
\
\
This message is split into words and any globs are expanded, such as the \*.zip. What will your users think when they see this message:\
\
- ```\
Please enter a file name of the form freenfss.zip lw35nfss.zip\
```\
\
\
To demonstrate:\
\

- ```\

var="*.zip"   # var contains an asterisk, a period, and the word "zip"\
echo "$var"   # writes *.zip\
echo $var     # writes the list of files which end with .zip\
```\
\
\
In fact, the `echo` command cannot be used with absolute safety here. If the variable contains `-n` for example, `echo` will consider that an option, rather than data to be printed. The only absolutely _sure_ way to print the value of a variable is using `printf`:\
\
- ```\
printf "%s\n" "$foo"\
```\
\
\

## 15\. $foo=bar\

\
\
No, you don't assign a variable by putting a `$` in front of the variable name. This isn't perl.\
\

## 16\. foo = bar\

\
\
No, you can't put spaces around the `=` when assigning to a variable. This isn't C. When you write `foo = bar` the shell splits it into three words. The first word, `foo`, is taken as the command name. The second and third become the arguments to that command.\
\
Likewise, the following are also wrong:\
\

- ```\

foo= bar    # WRONG!\
foo =bar    # WRONG!\
$foo = bar; # COMPLETELY WRONG!\
\
foo=bar     # Right.\
foo="bar"   # More Right.\
```\
\
\
## 17\. echo <<EOF\
\
\
A here document is a useful tool for embedding large blocks of textual data in a script. It causes a redirection of the lines of text in the script to the standard input of a command. Unfortunately, `echo` is not a command which reads from stdin.\
\
- ```\
    # This is wrong:\
    echo <\
```\
\
\
Using quotes like that is fine -- it works great, in all shells -- but it doesn't let you just drop a block of lines into the script. There's syntactic markup on the first and last line. If you want to have your lines untouched by shell syntax, and don't want to spawn a `cat` command, here's another alternative:\
\

- ```\

## Or use printf (also efficient, printf is built-in):\

```
printf %s "\\    printf %s "\\
    Hello world\
    How's it going?\
    "\
```\
\
\
In the `printf` example, the `</tt> on the first line prevents an extra newline at the beginning of the text block. There's a literal newline at the end (because the final quote is on a new line). The lack of \n in the printf format argument prevents printf adding an extra newline at the end. The </tt> trick won't work in single quotes. If you need/want single quotes around the block of text, you have two choices, both of which necessitate shell syntax "contaminating" your data:`\
\
``\
printf %s \\
'Hello world\
'\
printf %s 'Hello world\
'\
This syntax is almost correct. The problem is, on many platforms, su takes a -c argument, but it's not the one you want. For example, on OpenBSD:\
$ su -c 'echo hello'\
su: only the superuser may specify a login class\
You want to pass -c 'some command' to a shell, which means you need a username before the -c.\
su root -c 'some command' # Now it's right.\
su assumes a username of root when you omit one, but this falls on its face when you want to pass a command to the shell afterward. You must supply the username in this case.\
If you don't check for errors from the cd command, you might end up executing bar in the wrong place. This could be a major disaster, if for example bar happens to be rm -f *.\
You must always check for errors from a cd command. The simplest way to do that is:\
cd /foo && bar\
If there's more than just one command after the cd, you might prefer this:\
cd /foo || exit 1\
bar\
baz\
bat ... # Lots of commands.\
cd will report the failure to change directories, with a stderr message such as "bash: cd: /foo: No such file or directory". If you want to add your own message in stdout, however, you could use command grouping:\
cd /net || { echo >&2 "Can't read /net. Make sure you've logged in to the Samba network, and try again."; exit 1; }\
do_stuff\
more_stuff\
Note there's a required space between { and echo, and a required ; before the closing }. You could also write a die function, if you prefer.\
Some people also like to enable [set -e](http://mywiki.wooledge.org/BashFAQ/105) to make their scripts abort on any command that returns non-zero, but this can be [rather tricky to use correctly](http://mywiki.wooledge.org/BashFAQ/105) (since many common commands may return a non-zero for a warning condition, which you may not want to treat as fatal).\
By the way, if you're changing directories a lot in a Bash script, be sure to read the Bash help on pushd, popd, and dirs. Perhaps all that code you wrote to manage cd's and pwd's is completely unnecessary.\
Speaking of which, compare this:\
find ... -type d -print0 | while IFS= read -r -d '' subdir; do\
here=$PWD\
cd "$subdir" && whatever && ...\
cd "$here"\
done\
With this:\
find ... -type d -print0 | while IFS= read -r -d '' subdir; do\
(cd "$subdir" || exit; whatever; ...)\
done\
Forcing a [SubShell](http://mywiki.wooledge.org/SubShell) here causes the cd to occur only in the subshell; for the next iteration of the loop, we're back to our normal location, regardless of whether the cd succeeded or failed. We don't have to change back manually, and we aren't stuck in a neverending string of ... && ... logic preventing the use of other conditionals. The subshell version is simpler and cleaner (albeit a tiny bit slower).\
Another approach is to cd unconditionally to where we're supposed to be, at the start of each loop iteration:\
here=$PWD\
find ... -type d -print0 | while IFS= read -r -d '' subdir; do\
    cd "$here" || continue\
    cd "$subdir" || continue\
    whatever\
    ...\
done\
At least this way, we can continue to the next loop iteration and don't have to string an indefinite series of && together to ensure that we reach the cd at the end of the loop body.\
The == operator is not valid for the POSIX [ command. Use = or the [[ [keyword](http://mywiki.wooledge.org/BashFAQ/031) instead.\
[ bar = "$foo" ] && echo yes\
[[ bar == $foo ]] && echo yes\
In Bash, [ "$x" == y ] is accepted as an extension, which often leads Bash programmers to think it's the correct syntax. It's not; it's a [Bashism](http://mywiki.wooledge.org/Bashism). If you're going to use Bashisms, you might as well just use [[ instead.\
You cannot put a ; immediately after an &. Just remove the extraneous ; entirely.\
for i in {1..10}; do ./something & done\
Or:\
for i in {1..10}; do\
./something &\
done\
& already functions as a command terminator, just like ; does. And you cannot mix the two.\
In general, a ; can be replaced by a newline, but not all newlines can be replaced by ;.\
Some people try to use && and || as a shortcut syntax for if ... then ... else ... fi, perhaps because they think they are being clever. For instance,\
# WRONG!\
[[ -s $errorlog ]] && echo "Uh oh, there were some errors." || echo "Successful."\
However, this construct is not completely equivalent to if ... fi in the general case. The command that comes after the && also generates an exit status, and if that exit status isn't "true" (0), then the command that comes after the || will also be invoked. For example:\
i=0\
true && ((i++)) || ((i--))  # WRONG!\
echo "$i"                   # Prints 0\
What happened here? It looks like i should be 1, but it ends up 0. Why? Because both the i++ and the i-- were executed. The ((i++)) command has an exit status, and that exit status is derived from a C-like evaluation of the expression inside the parentheses. That expression's value happens to be 0 (the initial value of i), and in C, an expression with an integer value of 0 is considered false. So ((i++)) (when i is 0) has an exit status of 1 (false), and therefore the ((i--)) command is executed as well.\
Another clever person thinks that we can fix it by using the pre-increment operator, since the exit status from ++i (with i initially 0) is true:\
i=0\
true && (( ++i )) || (( --i ))  # STILL WRONG!\
echo "$i"                       # Prints 1 by dumb luck\
But that's missing the point of the example. It just happens to work by coincidence, and you cannot rely on x && y || z if y has any chance of failure! (This example still fails if we initialize i to -1 instead of 0.)\
If you need safety, or if you simply aren't sure how this works, or if anything in the preceding paragraphs wasn't completely clear, please just use the simple if ... fi syntax in your programs.\
i=0\
if true; then\
((i++))\
else\
((i--))\
fi\
echo "$i"    # Prints 1\
This section also applies to Bourne shell, here is the code that illustrates it:\
# WRONG!\
true && { echo true; false; } || { echo false; true; }\
Output is two lines "true" and "false", instead the single line "true".\
The problem here is that, in an interactive Bash shell (in versions prior to 4.3), you'll see an error like:\
bash: !": event not found\
This is because, in the default settings for an interactive shell, Bash performs csh-style history expansion using the exclamation point. This is not a problem in shell scripts; only in interactive shells.\
Unfortunately, the obvious attempt to "fix" this won't work:\
$ echo "hi\!"\
hi\!\
The easiest solution is unsetting the histexpand option: this can be done with set +H or set +o histexpand\
Question: Why is playing with histexpand more apropriate than single quotes?\
I personally ran into this issue when I was manipulating song files, using commands like\
mp3info -t "Don't Let It Show" ...\
mp3info -t "Ah! Leah!" ...\
Using single quotes is extremely inconvenient because of all the songs with apostrophes in their titles. Using double quotes ran into the history expansion issue. (And imagine a file that has both in its name. The quoting would be atrocious.) Since I never actually use history expansion, my personal preference was to turn it off in ~/.bashrc. -- [GreyCat](http://mywiki.wooledge.org/GreyCat)\
These solutions will work:\
echo 'Hello World!'\
or\
echo "Hello World"!\
or\
set +H\
echo "Hello World!"\
or\
histchars=\
Many people simply choose to put set +H or set +o histexpand in their ~/.bashrc to deactivate history expansion permanently. This is a personal preference, though, and you should choose whatever works best for you.\
Another solution is:\
exmark='!'\
echo "Hello, world$exmark"\
In Bash 4.3 and newer, a double quote following ! no longer triggers history expansion, but history expansion is still performed within double quotes, so while echo "Hello World!" is OK, these will still be a problem:\
echo "Hello, World!(and the rest of the Universe)"\
echo "foo!'bar'"\
Bash (like all Bourne shells) has a special syntax for referring to the list of positional parameters one at a time, and $* isn't it. Neither is $@. Both of those expand to the list of words in your script's parameters, not to each parameter as a separate word.\
The correct syntax is:\
for arg in "$@"\
# Or simply:\
for arg\
Since looping over the positional parameters is such a common thing to do in scripts, for arg defaults to for arg in "$@". The double-quoted "$@" is special magic that causes each parameter to be used as a single word (or a single loop iteration). It's what you should be using at least 99% of the time.\
Here's an example:\
# Incorrect version\
for x in $*; do\
echo "parameter: '$x'"\
done\
$ ./myscript 'arg 1' arg2 arg3\
parameter: 'arg'\
parameter: '1'\
parameter: 'arg2'\
parameter: 'arg3'\
It should have been written:\
# Correct version\
for x in "$@"; do\
echo "parameter: '$x'"\
done\
# or better:\
for x do\
echo "parameter: '$x'"\
done\
$ ./myscript 'arg 1' arg2 arg3\
parameter: 'arg 1'\
parameter: 'arg2'\
parameter: 'arg3'\
This works in some shells, but not in others. You should never combine the keyword function with the parentheses () when defining a function.\
Bash (at least some versions) will allow you to mix the two. Most of the shells won't accept that (zsh 4.x and perhaps above will - for example). Some shells will accept function foo, but for maximum portability, you should always use:\
foo() {\
...\
}\
Tilde expansion only applies when '' is unquoted. In this example echo writes '' to stdout, rather than the path of the user's home directory.\
Quoting path parameters that are expressed relative to a user's home directory should be done using $HOME rather than '~'. For instance consider the situation where $HOME is "/home/my photos".\
"~/dir with spaces" # expands to "~/dir with spaces"\
~"/dir with spaces" # expands to "~/dir with spaces"\
~/"dir with spaces" # expands to "/home/my photos/dir with spaces"\
"$HOME/dir with spaces" # expands to "/home/my photos/dir with spaces"\
When declaring a local variable in a function, the local acts as a command in its own right. This can sometimes interact oddly with the rest of the line -- for example, if you wanted to capture the exit status ($?) of the [CommandSubstitution](http://mywiki.wooledge.org/CommandSubstitution), you can't do it. local's exit status masks it.\
Another problem with this syntax is that in some shells (like bash), local var=$(cmd) is treated as an assignment, meaning the right hand side is given special treatment, just like var=$(cmd); while in other shells (like dash), local var=$(cmd) is not treated as an assignment, and the right hand side will undergo [word splitting](http://mywiki.wooledge.org/WordSplitting) (because it isn't quoted).\
Quoting the right hand side will work around the word splitting issue, but not the exit status masking issue. For both reasons, it's best to use separate commands for this:\
local var\
var=$(cmd)\
rc=$?\
Both issues are also true of export.\
The next pitfall describes another issue with this syntax:\
[Tilde expansion](http://mywiki.wooledge.org/TildeExpansion) (with or without a username) is only guaranteed to occur when the tilde appears at the beginning of a [word](http://mywiki.wooledge.org/Arguments), either by itself or followed by a slash. It is also guaranteed to occur when the tilde appears immediately after the = in an assignment.\
However, the export and local commands do not necessarily constitute an assignment. In some shells (like Bash), export foo=~/bar will undergo tilde expansion; in others (like dash), it will not.\
foo=~/bar; export foo    # Right!\
export foo="$HOME/bar"   # Right!\
In [single quotes](http://mywiki.wooledge.org/Quotes), bash parameter expansions like $foo do not get expanded. That is the purpose of single quotes, to protect characters like $ from the shell.\
Change the quotes to double quotes:\
foo="hello"; sed "s/$foo/good bye/"\
But keep in mind, if you use double quotes you might need to use more escapes. See the [Quotes](http://mywiki.wooledge.org/Quotes) page.\
There are (at least) three things wrong here. The first problem is that [A-Z] and [a-z] are seen as [glob](http://mywiki.wooledge.org/glob) s by the shell. If you don't have any single-lettered filenames in your current directory, it'll seem like the command is correct; but if you do, things will go wrong. Probably at 0300 hours on a weekend.\
The second problem is that this is not really the correct notation for tr. What this actually does is translate '[' into '['; anything in the range A-Z into a-z; and ']' into ']'. So you don't even need those brackets, and the first problem goes away.\
The third problem is that depending on the [locale](http://mywiki.wooledge.org/locale), A-Z or a-z may not give you the 26 ASCII characters you were expecting. In fact, in some locales z is in the middle of the alphabet! The solution to this depends on what you want to happen:\
# Use this if you want to change the case of the 26 latin letters\
LC_COLLATE=C tr A-Z a-z\
# Use this if you want the case conversion to depend upon the locale, which might be more like what a user is expecting\
tr '[:upper:]' '[:lower:]'\
The quotes are required on the second command, to avoid [globbing](http://mywiki.wooledge.org/glob).\
The fundamental problem here is that the name of a running process is inherently unreliable. There could be more than one legitimate gedit process. There could be something else disguising itself as gedit (changing the reported name of an executed command is trivial). For real answers to this, see [ProcessManagement](http://mywiki.wooledge.org/ProcessManagement).\
The following is the quick and dirty stuff.\
Searching for the PID of (for example) gedit, many people start with\
$ ps ax | grep gedit\
10530 ?        S      6:23 gedit\
32118 pts/0    R+     0:00 grep gedit\
which, depending on a [RaceCondition](http://mywiki.wooledge.org/RaceCondition), often yields grep itself as a result. To filter grep out:\
ps ax | grep -v grep | grep gedit   # will work, but ugly\
An alternative to this is to use:\
ps ax | grep '[g]edit'              # quote to avoid shell GLOB\
This will ignore the grep itself in the process table as that is [g]edit and grep is looking for gedit once evaluated.\
On GNU/Linux, the parameter -C can be used instead to filter by commandname:\
$ ps -C gedit\
PID TTY          TIME CMD\
10530 ?        00:06:23 gedit\
But why bother when you could just use pgrep instead?\
$ pgrep gedit\
10530\
Now in a second step the PID is often extracted by awk or cut:\
$ ps -C gedit | awk '{print $1}' | tail -n1\
but even that can be handled by some of the trillions of parameters for ps:\
$ ps -C gedit -opid=\
10530\
If you're stuck in 1992 and aren't using pgrep, you could use the ancient, obsolete, deprecated pidof (GNU/Linux only) instead:\
$ pidof gedit\
10530\
and if you need the PID to kill the process, pkill might be interesting for you. Note however that, for example, pgrep/pkill ssh would also find processes named sshd, and you wouldn't want to kill those.\
Unfortunately some programs aren't started with their name, for example firefox is often started as firefox-bin, which you would need to find out with - well - ps ax | grep firefox. [![:)](https://gist.github.com/dsoares/BashPitfalls_files/smile.png)](https://gist.github.com/dsoares/BashPitfalls_files/smile.png) Or, you can stick with pgrep by adding some parameters:\
$ pgrep -fl firefox\
3128 /usr/lib/firefox/firefox\
7120 /usr/lib/firefox/plugin-container /usr/lib/flashplugin-installer/libflashplayer.so -greomni /usr/lib/firefox/omni.ja 3128 true plugin\
Please read [ProcessManagement](http://mywiki.wooledge.org/ProcessManagement). Seriously.\
This isn't wrong because of [quotes](http://mywiki.wooledge.org/Quotes), but because of a format string exploit. If $foo is not strictly under your control, then any </tt> or % characters in the variable may cause undesired behavior.\
Always supply your own format string:\
printf %s "$foo"\
printf '%s\n' "$foo"\
The [BashParser](http://mywiki.wooledge.org/BashParser) performs [BraceExpansion](http://mywiki.wooledge.org/BraceExpansion) before any other expansions or substitutions. So the brace expansion code sees the literal $n, which is not numeric, and therefore it doesn't expand the curly braces into a list of numbers. This makes it nearly impossible to use brace expansion to create lists whose size is only known at run-time.\
Do this instead:\
for ((i=1; i<=n; i++)); do\
...\
done\
In the case of simple iteration over integers, an arithmetic for loop should almost always be preferred over brace expansion to begin with, because brace expansion pre-expands every argument which can be slower and unnecessarily consumes memory.\
When the right-hand side of an = operator inside [[ is not quoted, bash does [pattern matching](http://mywiki.wooledge.org/glob) against it, instead of treating it as a string. So, in the code above, if bar contains *, the result will always be true. If you want to check for equality of strings, the right-hand side should be quoted:\
if [[ $foo = "$bar" ]]\
If you want to do pattern matching, it might be wise to choose variable names that indicate the right-hand side contains a pattern. Or use comments.\
It's also worth pointing out that if you quote the right-hand side of =~ it also forces a simple string comparison, rather than a regular expression matching. This leads us to:\
The quotes around the right-hand side of the =~ operator cause it to become a string, rather than a [RegularExpression](http://mywiki.wooledge.org/RegularExpression). If you want to use a long or complicated regular expression and avoid lots of backslash escaping, put it in a variable:\
re='some RE'\
if [[ $foo =~ $re ]]\
This also works around the difference in how =~ works across different versions of bash. Using a variable avoids some nasty and subtle problems.\
The same problem occurs with [pattern matching](http://mywiki.wooledge.org/glob) inside [[:\
[[ $foo = "*.glob" ]]      # Wrong! *.glob is treated as a literal string.\
[[ $foo = *.glob ]]        # Correct. *.glob is treated as a glob-style pattern.\
When using the [ command, you must  [quote](http://mywiki.wooledge.org/Quotes) each substitution that you give it. Otherwise, $foo could expand to 0 words, or 42 words, or any number of words that isn't 1, which breaks the syntax.\
[ -n "$foo" ]\
[ -z "$foo" ]\
[ -n "$(some command with a "$file" in it)" ]\
# [[ doesn't perform word-splitting or glob expansion, so you could also use:\
[[ -n $foo ]]\
[[ -z $foo ]]\
Test follows symlinks, therefore if a symlink is broken, i.e. it points to a file that doesn't exists or is in a directory you don't have access to, test -e returns 1 for it even though it exists.\
In order to work around it (and prepare against it) you should use:\
# bash/ksh/zsh\
[[ -e "$broken_symlink" || -L "$broken_symlink" ]]\
# POSIX sh+test\
[ -e "$broken_symlink" ] || [ -L "$broken_symlink" ]\
The problem caused because ed doesn't accept 0 for {0,3}.\
You can check that the following do work:\
ed file <<<"g/d\{1,3\}/s//e/g"\
Note that this happens even though POSIX states that BRE (which is the Regular Expression flavor used by ed) [should accept 0 as the minimum number of occurrences (see section 5)](http://www.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html#tag_09_03_06).\
This works reasonably well\
most of the time\
word=abcde\
expr "$word" : ".\(.*\)"\
bcde\
But WILL fail for the word "match"\
word=match\
expr "$word" : ".\(.*\)"\
The problem is "match" is a keyword. Solution (GNU only) is prefix with a '+'\
word=match\
expr + "$word" : ".\(.*\)"\
atch\
Or, y'know, stop using expr. You can do everything expr does by using [Parameter Expansion](http://mywiki.wooledge.org/BashFAQ/073). What's that thing up there trying to do? Remove the first letter of a word? That can be done in POSIX shells using PE or Substring Expansion:\
$ word=match\
$ echo "${word#?}"    # PE\
atch\
$ echo "${word:1}"    # SE\
atch\
Seriously, there's no excuse for using expr unless you're on Solaris with its non-POSIX-conforming /bin/sh. It's an external process, so it's much slower than in-process string manipulation. And since nobody uses it, nobody understands what it's doing, so your code is obfuscated and hard to maintain.\
In general: Unix UTF-8 text does not use BOM. The encoding of plain text is determined by the locale or by mime types or other metadata. While the presence of a BOM would not normally damage a UTF-8 document meant only for reading by humans, it is problematic (often syntactically illegal) in any text file meant to be interpreted by automated processes such as scripts, source code, configuration files, and so on. Files starting with BOM should be considered equally foreign as those with MS-DOS linebreaks.\
In shell scripting: 'Where UTF-8 is used transparently in 8-bit environments, the use of a BOM will interfere with any protocol or file format that expects specific ASCII characters at the beginning, such as the use of "#!" of at the beginning of Unix shell scripts.' [http://unicode.org/faq/utf\_bom.html#bom5](http://unicode.org/faq/utf_bom.html#bom5)\
There isn't anything wrong with this expression, but you should be aware that command substitutions (all forms: ..., $(...), $(<file), <file, and ${ ...; } (ksh)) remove any trailing newlines. This is often inconsequential or even desirable, but if you must preserve the literal output including any possible trailing newlines, it gets tricky because you have no way of knowing whether the output had them or how many. One ugly but usable workaround is to add a postfix inside the command substitution and remove it on the outside:\
absolute_dir_path_x=$(readlink -fn -- "$dir_path"; printf x)\
absolute_dir_path=${absolute_dir_path_x%x}\
A less portable but arguably prettier solution is to use read with an empty delimiter.\
# Ksh (or bash 4.2+ with lastpipe enabled)\
readlink -fn -- "$dir_path" | IFS= read -rd '' absolute_dir_path\
The downside to this method is that the read will always return false unless the command outputs a NUL byte causing only part of the stream to be read. The only way to get the exit status of the command is through PIPESTATUS. You could also intentionally output a NUL byte to force read to return true, and use pipefail.\
set -o pipefail\
{ readlink -fn -- "$dir_path" && printf '\0'; } | IFS= read -rd '' absolute_dir_path\
set +o pipefail\
This is somewhat of a portability mess, as Bash supports both pipefail and PIPESTATUS, ksh93 supports pipefail only, and only recent versions of mksh support pipefail, while earlier versions supported PIPESTATUS only. Additionally, a bleeding-edge ksh93 version is required in order for read to stop at the NUL byte.\
One way to prevent programs from interpreting filenames passed to them as options is to use pathnames (see [pitfall #3](http://mywiki.wooledge.org/BashPitfalls#pf3) above). For files under the current directory, names may be prefixed with a relative pathname ./.\
In the case of a pattern like . however, problems can arise because it matches a string of the form ./filename. In a simple case, you can just use the glob directly to generate the desired matches. If however a separate pattern-matching step is required (e.g. the results have been preprocessed and stored in an array, and need to be filtered), it could be solved by taking the prefix into account in the pattern: [[ $file != ./. ]], or by stripping the pattern from the match.\
# Bash\
shopt -s nullglob\
for path in ./*; do\
    [[ ${path##*/} != *.* ]] && rm "$path"\
done\
# Or even better\
for file in *; do\
    [[ $file != *.* ]] && rm "./$file"\
done\
# Or better still\
for file in *.*; do\
    rm "./$file"\
done\
Another possibility is to signal the end of options with a -- argument. (Again, covered in [#pf3](http://mywiki.wooledge.org/BashPitfalls#pf3)).\
shopt -s nullglob\
for file in *; do\
    [[ $file != *.* ]] && rm -- "$file"\
done\
This is by far the most common mistake involving redirections, typically performed by someone wanting to direct both stdout and stderr to a file or pipe will try this and not understand why stderr is still showing up on their terminal. If you're perplexed by this, you probably don't understand how [redirections](http://wiki.bash-hackers.org/howto/redirection_tutorial) or possibly [file descriptors](http://mywiki.wooledge.org/FileDescriptor) work to begin with. Redirections are evaluated left-to-right before the command is executed. This semantically incorrect code essentially means: "first redirect standard error to where standard out is currently pointing (the tty), then redirect standard out to logfile". This is backwards. Standard error is already going to the tty. Use the following instead:\
somecmd >>logfile 2>&1\
See [a more in-depth explanation](http://mywiki.wooledge.org/BashFAQ/055), [Copy descriptor explained](http://wiki.bash-hackers.org/scripting/copydescriptor), and [BashGuide - redirection](http://mywiki.wooledge.org/BashGuide/InputAndOutput#Redirection).\
$? is only required if you need to retrieve the exact status of the previous command. If you only need to test for success or failure (any non-zero status), just test the command directly. e.g.:\
if cmd; then\
    ...\
fi\
Checking an exit status against a list of alternatives might follow a pattern like this:\
cmd\
status=$?\
case $status in\
    0)\
        echo success >&2\
        ;;\
    1)\
        echo 'Must supply a parameter, exiting.' >&2\
        exit 1\
        ;;\
    *)\
        echo "Unknown error $status, exiting." >&2\
        exit "$status"\
esac\
The code given to an arithmetic expansion or compound command undergoes a pass of expansions and substitutions prior to evaluation. It is the text generated by these initial expansions that is ultimately evaluated as an arithmetic expression. This must be handled correctly or unintended code execution can easily result.\
Here, an expression is stitched together by expanding one code fragment into another.\
$ x='$(date >&2)'        # redirection is just so we can see everything happen\
$ y=$((array["$x"]))       # Quotes don't help. The array doesn't even have to exist\
Mon Jun  2 10:49:08 EDT 2014\
The arithmetic processor needs to get a reference to this array variable in bash's internal symbol table, so it passes array[$(date >&2)] to a lookup function (just like e.g. read or printf -v do with variable names passed as arguments) which in turn expands the command substitution to resolve the index.\
(For numeric indexed arrays, the lookup function next evaluates the expanded text of the index as an arithmetic expression. Consequently, mutually recursive variable lookups and arithmetic expansions can occur to any depth (up to Bash's defined limit), any of which can produce unintended side-effects.)\
Most of the time, there is no need to use any kind of expansion within an arithmetic expansion. Use variable names directly in the expression (no $) wherever possible (i.e. except for positional parameters and POSIX "special variables"). If you validate variables before using them and guarantee that no expansion generates anything other than a numeric literal then most issues are automatically avoided.\
Escape any expansions to pass them into the expression without expanding them first:\
# Typical task reading some columns into an associative array.\
typeset -A arr\
printf -v offset '%(%s)T' -1\
while IFS=' ' read -r x y; do\
    [[ $x $y == +([0-9]) +([0-9]) ]] # validate input (see next pitfall)\
    (( arr[\$(date -d "@$x" +%F)] = y - offset )) # Escaped substitution passes the entire expression literally.\
done\
Another option is to use let with single-quoted arguments. ((expr)) is equivalent to let "expr" (double-quoted args).\
Always validate your input (see [BashFAQ/054](http://mywiki.wooledge.org/BashFAQ/054)) before using num in an arithmetic context as it allows code injection.\
$ echo 'a[$(echo injection >&2)]' | bash -c 'read num; echo $((num+1))'\
injection\
1\
Unbelievable as it may seem, POSIX requires the treatment of [IFS](http://mywiki.wooledge.org/IFS) as a field terminator, rather than a field separator. What this means in our example is that if there's an empty field at the end of the input line, it will be discarded:\
$ IFS=, read -ra fields <<< "a,b,"\
$ declare -p fields\
declare -a fields='([0]="a" [1]="b")'\
Where did the empty field go? It was eaten for historical reasons ("because it's always been that way"). This behavior is not unique to bash; all conformant shells do it. A non-empty field is properly scanned:\
$ IFS=, read -ra fields <<< "a,b,c"\
$ declare -p fields\
declare -a fields='([0]="a" [1]="b" [2]="c")'\
So, how do we work around this nonsense? As it turns out, appending an IFS character to the end of the input string will force the scanning to work. If there was a trailing empty field, the extra IFS character "terminates" it so that it gets scanned. If there was a trailing non-empty field, the IFS character creates a new, empty field that gets dropped.\
$ input="a,b,"\
$ IFS=, read -ra fields <<< "$input,"\
$ declare -p fields\
declare -a fields='([0]="a" [1]="b" [2]="")'\
Do not export CDPATH.\
Setting CDPATH in .bashrc is not an issue, but exporting it will cause any bash or sh script you run, that happen to use cd, to potentially change behaviour.\
There are two problems. A script that does the following:\
cd some/dir || exit\
cmd to be run in some/dir\
may change directory to ~/myProject/some/dir instead of ./some/dir, depending on what directories exist at the time. So the cd may succeed and take the script to the wrong directory, with potentially harmful effects of the following commands which now run in a different directory than intended.\
The second problem is when cd is run in a context where the output is captured:\
output=$(cd some/dir && some command)\
As a side-effect when CDPATH is set, cd will output something like /home/user/some/dir to stdout to indicate that it found a directory through CDPATH, which in turn will end up in the output variable along with the intended output of some command.\
A script can make itself immune to a CDPATH inherited from the environment by always prepending ./ to relative paths, or run unset CDPATH at the start of the script, but don't assume every scripter has taken this pitfall into account, so don't export CDPATH.\
Directly assigning a variable's value to a temporary variable isn't alone enough to restore its state. The assignment will always result in a set but empty temporary variable even if the initial variable was unset. This is a particular problem for IFS because an empty IFS has a completely different meaning from an unset IFS, and setting IFS to a temporary value for a command or two is a common requirement.\
An easy workaround is to designate a prefix to distinguish set from unset vars, then strip it when finished.\
oIFS=${IFS+_${IFS}}\
IFS=/; echo "${array[*]}"\
${oIFS:+'false'} unset -v IFS || IFS=${oIFS#_}\
A local variable is usually preferable when possible.\
f() {\
local IFS\
IFS=/; echo "${array[*]}"\
}\
f\
Subshells are another possibility.\
( IFS=/; echo "${array[*]}" )\
It is not safe to populate an array with a raw $(...)  [CommandSubstitution](http://mywiki.wooledge.org/CommandSubstitution). The output of the command undergoes word splitting (on all whitespace, even ones that are inside quotes) and then [globbing](http://mywiki.wooledge.org/glob). If there's a word like * or eh? or [abc] in the result, it will be expanded based on filenames in the current working directory.\
To select a replacement, you need to know whether the command writes its output on a single line, or multiple lines. If it's a single line:\
read -ra hosts < <(aws ...)\
If it's multiple lines (and you're targeting bash 4.0 or later):\
readarray -t hosts < <(aws ...)\
If it's multiple lines (and you want compatibility with bash 3.x, or want your command's exit status to be reflected in success or failure of the read operation without depending on behavior only available in bash 4.4 and newer):\
IFS=/pre>\n' read -r -d '' -a hosts < <(aws ... && printf '\0')\
This will prevent globbing. It still won't help you if you needed to avoid splitting on quoted whitespace, but unfortunately nothing bash can do handles that case. For generalized CSV (comma-separated value) file handling, you really need to switch to a language that has a dedicated CSV input library.\
GNU xargs supports running multiple jobs in parallel. -P n where n is the number of jobs to run in parallel.\
seq 100 | xargs -n1 -P10 echo "$a" | grep 5\
seq 100 | xargs -n1 -P10 echo "$a" > myoutput.txt\
This will work fine for many situations but has a deceptive flaw: If $a contains more than 8192 characters (the limit depends on platform and version), the echo may not be atomic (it may be split into multiple write() calls), and there is a risk that two lines will be mixed.\
$ perl -e 'print "a"x10000, "\n"' > foo\
$ strace -e write bash -c 'read -r foo < foo; echo "$foo"' >/dev/null\
write(1, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"..., 8192) = 8192\
write(1, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"..., 1809) = 1809\
+++ exited with 0 +++\
Obviously the same issue arises if there are multiple calls to echo or printf:\
slowprint() {\
printf 'Start-%s ' "$1"\
sleep "$1"\
printf '%s-End\n' "$1"\
}\
export -f slowprint\
seq 10 | xargs -n1 -I {} -P4 bash -c "slowprint {}"\
# Compare to no parallelization\
seq 10 | xargs -n1 -I {} bash -c "slowprint {}"\
# Be sure to see the warnings in the next Pitfall!\
Outputs from the parallel jobs are mixed together, because each job consists of two (or more) separate write() calls.\
If you need the outputs unmixed, it is therefore recommended to use a tool that guarantees output will be serialized (such as GNU Parallel).\
For further details see [a demonstration of the mixing problem](https://gist.github.com/ole-tange/88ae153797748b3618e2433377e2870a).\
This command contains a [CodeInjection](http://mywiki.wooledge.org/CodeInjection) vulnerability. The filename that is found by find is injected into a shell command and parsed by sh. If the filename contains shell metacharacters like ; or $( ... ) then the filename may be executed as code by `sh'.\
The "slowprint" example in the previous Pitfall would have been a [CodeInjection](http://mywiki.wooledge.org/CodeInjection) bug if the input weren't guaranteed to be integers.\
To be more precise, [POSIX find](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/find.html#tag_20_47) does not specify whether an argument which contains more than just {} is expanded. GNU find allows this [CodeInjection](http://mywiki.wooledge.org/CodeInjection) to occur. Other implementations choose a safer path:\
# uname -a\
HP-UX imadev B.10.20 A 9000/785 2008897791 two-user license\
# find /dev/null -exec sh -c 'echo {}' \;\
{}\
The correct approach is to separate the filename argument from the script argument:\
find . -exec sh -c 'echo "$1"' x {} \;\
[Redirection](http://mywiki.wooledge.org/Redirection) is done before the command is executed. Usually that doesn't matter, but with sudo we have a command being executed as a different user than the redirection.\
If the redirection must be executed with sudo-granted privileges, then you need a wrapper:\
sudo sh -c 'mycmd > /myfile'\
Instead of a wrapper you can use tee:\
mycmd | sudo tee /myfile >/dev/null\
This may be easier to write if mycmd has a lot of quoting.\
This is very similar to the previous pitfall. [Globbing](http://mywiki.wooledge.org/glob) is also done before the command is executed. If the directory isn't readable by your normal user privileges, then you may need the globbing to be done in a shell that has the sudo-granted privileges:\
sudo sh -c 'ls /foo/*'\
Do not close stdin, stdout or stderr as a "shorthand" for redirecting to /dev/null. Write it out correctly.\
myprogram 2>/dev/null\
Why? Consider what happens when your program tries to write an error message to stderr. If stderr has been redirected to /dev/null, the write succeeds, and your program is free to carry on, secure in the knowledge that it has diligently reported the error condition.\
But if stderr has been closed, then the write will fail. At that point, your program may do something unpredictable. It may carry on and ignore the failure, or it may immediately exit, considering the execution environment so broken that it cannot safely continue. Or whatever else the programmer decided the program should do when its world has become a dystopian hell.\
All programs are assured that stdin, stdout and stderr will exist and will be readable/writable in an appropriate and reasonable manner. By closing one of them, you have violated your promise to this program. This is not acceptable.\
Of course, an even better solution would be to actually log the errors somewhere, so you can go back and read them and figure out what's wrong.\
xargs splits on whitespace. This is unfortunate because whitespace is allowed in filenames and commonly used by GUI users. xargs also treats ' and " specially, which can also lead to problems:\
touch Dad\'s\ \"famous\"\ 1\'\ pizza.txt\
touch Dad\'s\ 12\"\ records.txt\
touch 2\"x1\'\ wood.txt\
touch 2\"x4\"\ wood.txt\
Here xargs warns:\
# Do not do this\
$ find . -type f | xargs wc\
xargs: unmatched single quote; by default quotes are special to xargs unless you use the -0 option\
Here xargs does not warn at all:\
# Do not do this\
echo * | xargs wc\
find *famous* -type f | xargs wc\
find *4* -type f | xargs wc\
Instead use xargs -0:\
# Do this instead\
printf '%s\0' * | xargs -0 wc\
find . -type f -name '*famous*' -print0 | xargs -0 wc\
find . -type f -name '*4*' -exec wc {} +\
If using -0 is not simple, an alternative is to use GNU Parallel, which splits on \n. And while \n is also allowed in filenames they never occur unless your users are malicious. In any case: If you use xargs without -0 put a comment in your code explaining why that is safe in your particular situation.\
When passing an [indexed array element](http://mywiki.wooledge.org/BashFAQ/005) to unset, it needs to be quoted. Otherwise, it may be treated as a [glob](http://mywiki.wooledge.org/glob), and expanded against the files in the current directory. If there happens to be a file named a0 then the glob is expanded to a0 and you end up executing unset a0.\
unset 'a[0]'     # Always quote indexed array elements when unsetting.\
Calling date multiple times is a bad idea. Imagine what happens if the first call occurs a millisecond before midnight on April 30, and the second call occurs a millisecond after midnight on May 1. You would end up with month=04 and day=01.\
It's better to call date one time, retrieving all of the fields you want in a single invocation.\
A common idiom for that:\
eval "$(date +'month=%m day=%d year=%Y dayname="%A" monthname="%B"')"\
Or with bash's (4.2 or above) printf builtin:\
printf -v d '%(month=%m day=%d year=%Y dayname="%A" monthname="%B")T'\
eval "$d"\
Remember things like month or day names are locale-dependent, hence the quotes around %A or %B to avoid problems in locales where day or month names contain spaces or other special characters for the shell.\
Or, you may retrieve a timestamp in epoch format (seconds since the start of 1970), and then use that to generate human-readable date/time fields as needed.\
# Requires bash 4.2 or above\
printf -v now '%(%s)T' -1        # Or now=$EPOCHSECONDS in bash 5.0\
                                 # -1 may be omitted in 4.3 or above\
printf -v month '%(%m)T' "$now"\
printf -v day '%(%d)T' "$now"\
If your system's strftime() doesn't support %s, you can get the epoch time with:\
now=$(awk 'BEGIN{srand(); print srand()}')\
Forced base 10 interpretation only works with signless numbers. As long as $i contains a string of digits with no leading - or +, everything is fine. But if $i might be negative, this conversion could fail, either noisily (with an error message), or even worse, silently (simply yielding the wrong result).\
If there's any chance $i could be negative, use this instead:\
i=$(( ${i%%[!+-]*}10#${i#[-+]} ))\
For explanations, please see [ArithmeticExpression](http://mywiki.wooledge.org/ArithmeticExpression).\
BashPitfalls (last edited 2019-11-09 08:49:48 by 89-23-224-57)\
``\
\
`\
[MoinMoin Powered](http://moinmo.in/ "This site uses the MoinMoin Wiki software.")\
[Python Powered](http://moinmo.in/Python "MoinMoin is written in Python.")\
[GPL licensed](http://moinmo.in/GPL "MoinMoin is GPL licensed.")\
[Valid HTML 4.01](http://validator.w3.org/check?uri=referer "Click here to validate this page.")\
`\
\
[Sign up for free](https://gist.github.com/join?source=comment-gist) **to join this conversation on GitHub**.\
Already have an account?\
[Sign in to comment](https://gist.github.com/login?return_to=https%3A%2F%2Fgist.github.com%2Fdsoares%2F7608d68538be606f3b6a6f0c557bfc8c)\
\
You can’t perform that action at this time.

---

### 9. GitHub - hegdepavankumar/shell-scripting-tutorial: Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced developer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting.

**Source:** [https://github.com/hegdepavankumar/shell-scripting-tutorial](https://github.com/hegdepavankumar/shell-scripting-tutorial)
**Domain:** `github.com`
**Quality Score:** 18

*Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced developer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting. - hegdepavankumar/shell-scripting-tutorial*


Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced developer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting.


[hegdepavankumar.github.io/shell-scripting-tutorial/](https://hegdepavankumar.github.io/shell-scripting-tutorial/ "https://hegdepavankumar.github.io/shell-scripting-tutorial/")

### License

[Apache-2.0 license](https://github.com/hegdepavankumar/shell-scripting-tutorial/blob/main/LICENSE)

[**1** Branch](https://github.com/hegdepavankumar/shell-scripting-tutorial/branches) [**0** Tags](https://github.com/hegdepavankumar/shell-scripting-tutorial/tags)

[![GitHub](https://camo.githubusercontent.com/1e829b325691a5bb6c094f0efa729bae98eaa8e4919bcb03f3a91240e0f8a141/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)](https://camo.githubusercontent.com/1e829b325691a5bb6c094f0efa729bae98eaa8e4919bcb03f3a91240e0f8a141/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)[![GitHub top language](https://camo.githubusercontent.com/84e49330c3d75c7a0b7213ef7fc95e027878bd220c732b47853f3041a61c6ada/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c616e6775616765732f746f702f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)](https://camo.githubusercontent.com/84e49330c3d75c7a0b7213ef7fc95e027878bd220c732b47853f3041a61c6ada/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c616e6775616765732f746f702f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)[![GitHub last commit](https://camo.githubusercontent.com/8f9cdae77daf92ccb31b91dcc8507acc217299674d927806326fcc4a4b1f816d/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6173742d636f6d6d69742f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)](https://camo.githubusercontent.com/8f9cdae77daf92ccb31b91dcc8507acc217299674d927806326fcc4a4b1f816d/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6173742d636f6d6d69742f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7475746f7269616c3f7374796c653d666c6174)[![ViewCount](https://camo.githubusercontent.com/ae2ceccf74a488c541227776c962cc4233b4d9394c1f835604177c882de313b6/68747470733a2f2f76696577732e77686174696c656172656e65642e746f6461792f76696577732f6769746875622f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7a65726f2d746f2d6865726f2e7376673f63616368653d72656d6f7665)](https://camo.githubusercontent.com/ae2ceccf74a488c541227776c962cc4233b4d9394c1f835604177c882de313b6/68747470733a2f2f76696577732e77686174696c656172656e65642e746f6461792f76696577732f6769746875622f6865676465706176616e6b756d61722f7368656c6c2d736372697074696e672d7a65726f2d746f2d6865726f2e7376673f63616368653d72656d6f7665)

[![telegram (1)](https://private-user-images.githubusercontent.com/85627085/322892977-ab437638-444e-4887-bab1-7ed21413fa68.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjMyOTE5MDcsIm5iZiI6MTc2MzI5MTYwNywicGF0aCI6Ii84NTYyNzA4NS8zMjI4OTI5NzctYWI0Mzc2MzgtNDQ0ZS00ODg3LWJhYjEtN2VkMjE0MTNmYTY4LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTExMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMTE2VDExMTMyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTJmOGM3YzdmYTc4NDExNTkyMmEwMDg4OTE3YzhlOGU4N2M0Y2EyZDZkNzQ2NTk4ZDc0ZWQ2NDY3Y2ViZDE3ZjImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.f-2nx27nDR5ODxMATyv0t13ib_2RApNMm3_-qvmpvU8)](https://t.me/resourcehub1)[![telegram (1)](https://private-user-images.githubusercontent.com/85627085/322892977-ab437638-444e-4887-bab1-7ed21413fa68.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjMyOTE5MDcsIm5iZiI6MTc2MzI5MTYwNywicGF0aCI6Ii84NTYyNzA4NS8zMjI4OTI5NzctYWI0Mzc2MzgtNDQ0ZS00ODg3LWJhYjEtN2VkMjE0MTNmYTY4LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTExMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMTE2VDExMTMyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTJmOGM3YzdmYTc4NDExNTkyMmEwMDg4OTE3YzhlOGU4N2M0Y2EyZDZkNzQ2NTk4ZDc0ZWQ2NDY3Y2ViZDE3ZjImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.f-2nx27nDR5ODxMATyv0t13ib_2RApNMm3_-qvmpvU8)](https://t.me/resourcehub1)[Open in new window](https://t.me/resourcehub1)

# SUPPORT ME -- 🚩💲🙏

### 🚀 Love my Shell Scripting Tutorial repo? It's your go-to resource for mastering shell scripting for network/security engineer roles and automating daily tasks. I've invested valuable time to create a comprehensive guide. If you find it helpful, consider showing your support with a coffee ☕️ or your best wishes. Your appreciation keeps this resource thriving!

[![Buy Me A Coffee](https://camo.githubusercontent.com/0cf29a542375e1a46e84d8bf5805a4e5c0a6ee98b6547ccdc0c55eed49d99c69/68747470733a2f2f63646e2e6275796d6561636f666665652e636f6d2f627574746f6e732f76322f64656661756c742d79656c6c6f772e706e67)](https://www.buymeacoffee.com/hegdepavankumar)

* * *

# Free and Paid Learning Resources: [Claim now](https://buymeacoffee.com/hegdepavankumar/extras)

# Shell Scripting: A Complete Guide

Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced Network/Software Engineer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting.

🚀 **What's Inside:**

- **Foundational Concepts:** Learn the fundamentals of Bash, including basic commands, variables, and data types.
- **Control Flow:** Master conditional statements and loops for efficient script execution.
- **Functions and Arrays:** Dive into the world of functions, arrays, and advanced data manipulation.
- **File Handling and Text Processing:** Explore file operations, regular expressions, and powerful text-processing tools.
- **Automation Techniques:** Discover how to automate tasks, manage processes, and schedule jobs with cron.
- **Security and Best Practices:** Write secure scripts, adhere to coding standards, and implement best practices.
- **Real-world Examples:** Apply your skills to practical examples, from log analysis to system monitoring.
- **Version Control and Documentation:** Learn to manage scripts with version control and document your code effectively.

👩‍💻 **Hands-On Learning:** Each section comes with hands-on exercises and real-world scenarios to reinforce your understanding.

🌐 **Who Is This For?**

- Beginners eager to start their scripting journey.
- Intermediate users seeking to deepen their knowledge.
- Professionals wanting to apply scripting in corporate environments.

📚 **Why "Zero to Hero"?**
This repository is designed to take you from a novice to a scripting hero, providing the tools and knowledge needed to excel in real-world scripting tasks.
Absolutely, here are 5 key points for your Bash scripting tutorial:

1. **Universal Power of Bash:**
   - Highlight the prevalence of Bash on Unix-like systems, making it an essential skill for anyone dealing with networking and system administration.
2. **Hands-on Setup:**
   - Provide a step-by-step guide for beginners to set up their scripting environment, ensuring they can dive into Bash without unnecessary obstacles.
3. **Practical Automation:**
   - Showcase real-world examples of how Bash scripting can automate common networking tasks, emphasizing its practical applications for professionals.
4. **Modularity for Efficiency:**
   - Stress the importance of writing modular scripts, enabling both beginners and professionals to create organized and reusable code for efficient problem-solving.
5. **Corporate Impact:**
   - Illustrate the value of scripting in a corporate environment, where time-saving automation can lead to increased productivity and smoother network operations.

Ready to become a scripting hero? Clone the repository, follow the tutorials, and start scripting your way to success!

## Connect with me : [Join Telegram](https://t.me/resourcehub1)

# Table of Contents

## Quick-Recap \| [Linux-cheat-sheet](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/Linux-cheat-sheet.md)

## [**Prerequisites:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/01.Introduction-to-Bash/01.What%20is%20Bash.md)

01. [**Introduction to Bash:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/01.Introduction-to-Bash)
    - [What is Bash?](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/01.Introduction-to-Bash/01.What%20is%20Bash.md)
    - [Importance of shell scripting in automation.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/01.Introduction-to-Bash/02.Importance%20of%20shell%20scripting%20in%20automation.md)
02. [**Basic Commands:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/02.Basic-Commands)
    - [Basic commands (ls, cd, mkdir, rm, cp, mv, etc.).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/02.Basic-Commands/01.Basic_Commands.md)
    - [Understanding file permissions (chmod, chown).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/02.Basic-Commands/02.Understanding_file_permissions.md)
03. [**Variables and Data Types:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/03.Variables-and-Data-Types)
    - [Declaring and using variables.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/03.Variables-and-Data-Types/01.Declaring_and_using_variables.md)
    - [String manipulation.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/03.Variables-and-Data-Types/02.String_manipulation.md)
    - [Numeric operations.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/03.Variables-and-Data-Types/03.Numeric_Operations.md)
04. [**Conditional Statements:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/04.Conditional-Statements)
    - [if, elif, else statements.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/04.Conditional-Statements/01.if_elif_else_statements.md)
    - [Case statements.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/04.Conditional-Statements/02.Case_statements.md)
05. [**Loops:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/05.Loops)
    - [for, while, until loops.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/05.Loops/01.for_while_until_loops.md)
    - [Loop control statements (break, continue).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/05.Loops/02.Loop_control%20statements_(break%2C%20continue).md)
06. [**Functions:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/06.Functions)
    - [Defining and using functions.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/06.Functions/01.Defining_and_using_functions.md)
    - [Passing arguments to functions.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/06.Functions/02.Passing_arguments_to_functions.md)
    - [Returning values from functions.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/06.Functions/03.Returning_values_from_functions.md)
07. [**Arrays:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/07.Arrays)
    - [Declaring and accessing arrays.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/07.Arrays/01.Declaring_and_accessing_arrays.md)
    - [Array manipulation.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/07.Arrays/02.Array_manipulation.md)
08. [**File Handling:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/08.File-Handling)
    - [Reading from and writing to files.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/08.File-Handling/01.Reading_from_and_writing_to_files.md)
    - [Checking file existence and type.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/08.File-Handling/02.Checking_file_existence_and_type.md)
- [File manipulation commands (sed, awk).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/08.File-Handling/03.File_manipulation_commands_(sed%2C%20awk).md)
09. [**Input/Output Redirection:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/09.Input_Output-Redirection)
    - [Redirecting standard input and output.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/09.Input_Output-Redirection/01.Redirecting_standard_input_and_output.md)
    - [Using pipes for command chaining.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/09.Input_Output-Redirection/02.Using_pipes_for_command_chaining.md)
10. [**Regular Expressions:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/10.Regular-Expressions)
    - [Basic regex patterns.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/10.Regular-Expressions/01.Basic_regex_patterns.md)
    - [grep, sed, and awk for pattern matching and text processing.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/10.Regular-Expressions/02.grep%2C%20sed%2C%20and%20awk%20for%20pattern%20matching%20and%20text%20processing.md)
11. [**Error Handling:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/11.Error-Handling)
    - [Handling errors with exit codes.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/11.Error-Handling/01.Handling_errors_with_exit_codes.md)
    - [Using `trap` for signal handling.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/11.Error-Handling/02.Using_trap_for_signal_handling.md)
12. [**Environment Variables:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/12.Environment-Variables)
    - [Built-in environment variables.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/12.Environment-Variables/01.Built-in_environment_variables.md)
    - [Custom environment variables.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/12.Environment-Variables/02.Custom_environment_variables.md)
13. [**Debugging Techniques:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/13.Debugging-Techniques)
    - [Using `echo` and `printf` for debugging.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/13.Debugging-Techniques/01.Using_echo_and_printf_for_debugging.md)
    - [Setting and using breakpoints.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/13.Debugging-Techniques/02.Setting_and_using_breakpoints.md)
14. [**Advanced Scripting Techniques:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/14.Advanced-Scripting-Techniques)
    - [Managing processes (ps, kill, jobs).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/14.Advanced-Scripting-Techniques/01.Managing_processes%20(ps%2C%20kill%2C%20jobs).md)
    - [Job scheduling with cron.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/14.Advanced-Scripting-Techniques/02.Job_scheduling_with_cron.md)
    - [Signal handling.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/14.Advanced-Scripting-Techniques/03.Signal_handling.md)
15. [**Security Best Practices:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/15.Security-Best-Practices)
    - [Writing secure scripts.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/15.Security-Best-Practices/01.Writing_secure_scripts.md)
    - [Avoiding common pitfalls.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/15.Security-Best-Practices/02.Avoiding_common_pitfalls.md)
16. [**Interacting with External Commands:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/16.Interacting-with-External-Commands)
    - [Running external commands from scripts.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/16.Interacting-with-External-Commands/01.Running%20external%20commands%20from%20scripts.md)
    - [Capturing and using command output.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/16.Interacting-with-External-Commands/02.Capturing%20and%20using%20command%20output.md)
17. [**Real-world Examples:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/17.Real-world-Examples)
    - [Practical scripts for common tasks (log analysis, data processing, system monitoring).](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/17.Real-world-Examples/01.Practical%20scripts%20for%20common%20tasks%20(log%20analysis%2C%20data%20processing%2C%20system%20monitoring).md)
    - [Integration with other tools and technologies.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/17.Real-world-Examples/02.Integration%20with%20other%20tools%20and%20technologies.md)
18. [**Best Practices:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/tree/main/Tutorial-Files/19.Best-Practices)
    - [Coding standards.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/19.Best-Practices/01.Coding%20standards.md)
    - [Code reviews and collaboration.](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/19.Best-Practices/02.Code%20reviews%20and%20collaboration.md)
19. [**Conclusion:**](https://github.com/hegdepavankumar/bash-scripting-tutorial/blob/main/Tutorial-Files/19.Conclusion.md)

20. [**Resources for learning more about Bash scripting:**](https://github.com/hegdepavankumar/shell-scripting-tutorial/blob/main)


* * *

## Creator [🔝](https://github.com/hegdepavankumar/shell-scripting-tutorial/blob/main/Images-for-GNS3-and-EVE-NG)

( [https://github.com/hegdepavankumar](https://github.com/hegdepavankumar)). Created by:-

\| [![](https://github.com/hegdepavankumar.png?size=115)\\
\\
@hegdepavankumar](https://github.com/hegdepavankumar) \|

### Show some  ❤️  by starring some of the repositories!


If you like what I do, maybe consider buying me a coffee 🥺👉👈

[![Buy Me A Coffee](https://camo.githubusercontent.com/af7c4175cb725540f9b150c8450be14b719748cbe0445c56e51c70bb51fad263/68747470733a2f2f63646e2e6275796d6561636f666665652e636f6d2f627574746f6e732f76322f64656661756c742d7265642e706e67)](https://www.buymeacoffee.com/hegdepavankumar)

## About

Welcome to the "Shell Scripting Zero to Hero" repository, your comprehensive guide to mastering Bash shell scripting for real-world corporate scenarios. Whether you're a beginner looking to automate tedious tasks or an experienced developer aiming to enhance your scripting skills, this tutorial takes you from the basics to hero-level scripting.


[hegdepavankumar.github.io/shell-scripting-tutorial/](https://hegdepavankumar.github.io/shell-scripting-tutorial/ "https://hegdepavankumar.github.io/shell-scripting-tutorial/")

### Topics

[shell](https://github.com/topics/shell "Topic: shell") [bash](https://github.com/topics/bash "Topic: bash") [linux-shell](https://github.com/topics/linux-shell "Topic: linux-shell") [shell-script](https://github.com/topics/shell-script "Topic: shell-script") [shellscript](https://github.com/topics/shellscript "Topic: shellscript") [bash-script](https://github.com/topics/bash-script "Topic: bash-script") [linux-tutorials](https://github.com/topics/linux-tutorials "Topic: linux-tutorials") [shell-scripting](https://github.com/topics/shell-scripting "Topic: shell-scripting") [linux-beginners](https://github.com/topics/linux-beginners "Topic: linux-beginners") [bash-scripting](https://github.com/topics/bash-scripting "Topic: bash-scripting") [bash-tutorial](https://github.com/topics/bash-tutorial "Topic: bash-tutorial") [linux-learning](https://github.com/topics/linux-learning "Topic: linux-learning") [linux-tutorial](https://github.com/topics/linux-tutorial "Topic: linux-tutorial") [shell-scripting-tutorial](https://github.com/topics/shell-scripting-tutorial "Topic: shell-scripting-tutorial")

### Resources

[Readme](https://github.com/hegdepavankumar/shell-scripting-tutorial#readme-ov-file)

### License

[Apache-2.0 license](https://github.com/hegdepavankumar/shell-scripting-tutorial#Apache-2.0-1-ov-file)

### Contributing

[Contributing](https://github.com/hegdepavankumar/shell-scripting-tutorial#contributing-ov-file)

### Security policy

[Security policy](https://github.com/hegdepavankumar/shell-scripting-tutorial#security-ov-file)

[Activity](https://github.com/hegdepavankumar/shell-scripting-tutorial/activity)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fhegdepavankumar%2Fshell-scripting-tutorial&report=hegdepavankumar+%28user%29)

## [Releases](https://github.com/hegdepavankumar/shell-scripting-tutorial/releases)

No releases published

## [Packages\  0](https://github.com/users/hegdepavankumar/packages?repo_name=shell-scripting-tutorial)

No packages published

You can’t perform that action at this time.

---

### 10. GitHub - dereknguyen269/programing-best-practices: Awesome Programming Best Practices for Beginners

**Source:** [https://github.com/dereknguyen269/programing-best-practices](https://github.com/dereknguyen269/programing-best-practices)
**Domain:** `github.com`
**Quality Score:** 18

*Awesome Programming Best Practices for Beginners. Contribute to dereknguyen269/programing-best-practices development by creating an account on GitHub.*

- [Sponsor](https://github.com/sponsors/dereknguyen269)


Awesome Programming Best Practices for Beginners


### License

[Unlicense license](https://github.com/dereknguyen269/programing-best-practices/blob/master/LICENSE)

# 🌟 Programming Best Practices

[![Awesome Badge](https://camo.githubusercontent.com/2727609d8bfde9ba1a95be1449eb878bfafa4d76789ba05661857e2c8ac70fa1/68747470733a2f2f63646e2e7261776769742e636f6d2f73696e647265736f726875732f617765736f6d652f643733303566333864323966656437386661383536353265336136336531353464643865383832392f6d656469612f62616467652e737667)](https://camo.githubusercontent.com/2727609d8bfde9ba1a95be1449eb878bfafa4d76789ba05661857e2c8ac70fa1/68747470733a2f2f63646e2e7261776769742e636f6d2f73696e647265736f726875732f617765736f6d652f643733303566333864323966656437386661383536353265336136336531353464643865383832392f6d656469612f62616467652e737667)[![Star Badge](https://camo.githubusercontent.com/1ab4c8631e7f12c522ede20bf06b19bdf6a909dedb74666696cdf8b4c58c5d77/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6c6162656c3d254630253946253843253946266d6573736167653d496625323055736566756c267374796c653d666c617426636f6c6f723d424334453939)](https://camo.githubusercontent.com/1ab4c8631e7f12c522ede20bf06b19bdf6a909dedb74666696cdf8b4c58c5d77/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f6c6162656c3d254630253946253843253946266d6573736167653d496625323055736566756c267374796c653d666c617426636f6c6f723d424334453939)[![GitHub issues](https://camo.githubusercontent.com/e2a9d6e5efe5f206b8642a282f7ca2cc55e81e62aec63134a6ed17afcf23598c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)](https://camo.githubusercontent.com/e2a9d6e5efe5f206b8642a282f7ca2cc55e81e62aec63134a6ed17afcf23598c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6973737565732f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)[![GitHub stars](https://camo.githubusercontent.com/a124d4b910e2fd75a672938c190e159849fe85cfb8d637ff23e86b404dfe0a6a/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)](https://camo.githubusercontent.com/a124d4b910e2fd75a672938c190e159849fe85cfb8d637ff23e86b404dfe0a6a/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)[![Github license](https://camo.githubusercontent.com/291e3e0c747fb2e26276e04b313bb7fbc5a76d6c37d62233ea67ea449c892b1c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)](https://camo.githubusercontent.com/291e3e0c747fb2e26276e04b313bb7fbc5a76d6c37d62233ea67ea449c892b1c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f646572656b6e677579656e3236392f70726f6772616d696e672d626573742d707261637469636573)

* * *

## 📖 Introduction

This repository is a **curated collection of programming best practices** across multiple languages, frameworks, and tools.

It is not an exhaustive list but rather a practical resource containing articles, guidelines, and style guides that have proven helpful in real-world development.

The focus is primarily on **Web Development** (Ruby, Rails, JavaScript, etc.), but it also covers **databases, DevOps, cloud practices, AI tools, and career growth**.

With this collection, I hope to support developers in writing **cleaner, more maintainable code** and growing in their careers.

**Status:** 🚧 _Work in Progress — continuously updated_

* * *

## 📂 Table of Contents

### 🔹 Backend Development

#### Systems Programming

- [C](https://github.com/dereknguyen269/programing-best-practices#c-best-practices)
- [C++](https://github.com/dereknguyen269/programing-best-practices#c-best-practices-1)
- [Rust](https://github.com/dereknguyen269/programing-best-practices#rust-best-practices)

#### Enterprise & JVM Languages

- [Java](https://github.com/dereknguyen269/programing-best-practices#java-best-practices)
- [Kotlin](https://github.com/dereknguyen269/programing-best-practices#kotlin-best-practices)
- [Scala](https://github.com/dereknguyen269/programing-best-practices#scala-best-practices)
- [C#](https://github.com/dereknguyen269/programing-best-practices#c-best-practices-2)

#### Web Backend

- [Node.js](https://github.com/dereknguyen269/programing-best-practices#nodejs-best-practices)
- [Python](https://github.com/dereknguyen269/programing-best-practices#python-best-practices)
- [Ruby](https://github.com/dereknguyen269/programing-best-practices#ruby-best-practices)
- [Rails](https://github.com/dereknguyen269/programing-best-practices#rails-best-practices)
- [PHP](https://github.com/dereknguyen269/programing-best-practices#php-best-practices)
- [Laravel](https://github.com/dereknguyen269/programing-best-practices#laravel-best-practices)
- [NestJS](https://github.com/dereknguyen269/programing-best-practices#nestjs-best-practices)

#### Functional & Specialized

- [Elixir](https://github.com/dereknguyen269/programing-best-practices#elixir-best-practices)
- [Go](https://github.com/dereknguyen269/programing-best-practices#go-golang-best-practices)
- [Swift](https://github.com/dereknguyen269/programing-best-practices#swift-best-practices)
- [Objective-C](https://github.com/dereknguyen269/programing-best-practices#objective-c-best-practices)
- [Perl](https://github.com/dereknguyen269/programing-best-practices#perl-best-practices)
- [Lua](https://github.com/dereknguyen269/programing-best-practices#lua-best-practices)

### 🔹 Frontend Development

#### Core Technologies

- [HTML](https://github.com/dereknguyen269/programing-best-practices#html-best-practices)
- [CSS](https://github.com/dereknguyen269/programing-best-practices#css-best-practices)
- [SASS](https://github.com/dereknguyen269/programing-best-practices#sass-best-practices)
- [JavaScript](https://github.com/dereknguyen269/programing-best-practices#javascript-best-practices)
- [TypeScript](https://github.com/dereknguyen269/programing-best-practices#typescript-best-practices)

#### Frameworks & Libraries

- [React](https://github.com/dereknguyen269/programing-best-practices#reactjs-best-practices)
- [React Native](https://github.com/dereknguyen269/programing-best-practices#react-native-best-practices)
- [Vue](https://github.com/dereknguyen269/programing-best-practices#vue-best-practices)
- [Angular](https://github.com/dereknguyen269/programing-best-practices#angular-best-practices)
- [Next.js](https://github.com/dereknguyen269/programing-best-practices#nextjs-best-practices)
- [Nuxt](https://github.com/dereknguyen269/programing-best-practices#nuxt-best-practices)

#### Performance

- [Frontend Performance](https://github.com/dereknguyen269/programing-best-practices#frontend-performance-best-practices)

### 🔹 Database & Data

#### SQL Databases

- [SQL](https://github.com/dereknguyen269/programing-best-practices#sql-best-practices)
- [PostgreSQL](https://github.com/dereknguyen269/programing-best-practices#postgresql-best-practices)
- [MySQL](https://github.com/dereknguyen269/programing-best-practices#mysql-best-practices)

#### NoSQL & Big Data

- [NoSQL](https://github.com/dereknguyen269/programing-best-practices#nosql-best-practices)

### 🔹 Mobile Development

- [Flutter](https://github.com/dereknguyen269/programing-best-practices#flutter-best-practices)
- [Dart](https://github.com/dereknguyen269/programing-best-practices#dart-best-practices)
- [React Native](https://github.com/dereknguyen269/programing-best-practices#react-native-best-practices)

### 🔹 DevOps & Infrastructure

#### Cloud & Deployment

- [AWS](https://github.com/dereknguyen269/programing-best-practices#aws-best-practices)
- [Microservices & Cloud-Native](https://github.com/dereknguyen269/programing-best-practices#microservices--cloud-native-best-practices)

#### Security

- [API Security](https://github.com/dereknguyen269/programing-best-practices#api-security-best-practices)
- [DevSecOps](https://github.com/dereknguyen269/programing-best-practices#devsecops--security-best-practices)

### 🔹 AI & Data Science

- [AI/ML Engineering](https://github.com/dereknguyen269/programing-best-practices#aiml-engineering-best-practices)
- [AI Tools for Developers](https://github.com/dereknguyen269/programing-best-practices#ai-tools-for-developers)

### 🔹 Development Tools & Practices

#### Version Control & Collaboration

- [Code Review](https://github.com/dereknguyen269/programing-best-practices#code-review-best-practices)
- [Team Collaboration](https://github.com/dereknguyen269/programing-best-practices#team--collaboration-best-practices)

#### Scripting & Automation

- [Bash](https://github.com/dereknguyen269/programing-best-practices#bash-script-best-practices)

#### Performance & Architecture

- [System Design](https://github.com/dereknguyen269/programing-best-practices#system-design-best-practices)
- [Performance & Scalability](https://github.com/dereknguyen269/programing-best-practices#performance--scalability-best-practices)

### 🔹 Specialized Languages

- [R](https://github.com/dereknguyen269/programing-best-practices#r-best-practices)

* * *

# 🔹 Backend Development

## Systems Programming

### 🖥️ C Best Practices

- [C Programming Best Practices – Must know to become an Expert](https://data-flair.training/blogs/c-programming-best-practices/)
- [c-style](https://github.com/mcinglis/c-style) — _@mcinglis_

* * *

### 🖥️ C++ Best Practices

- [3 Coding Best Practices for C++](https://www.perforce.com/blog/qac/3-coding-best-practices-cpp)
- [Collaborative Collection of C++ Best Practices](https://github.com/lefticus/cppbestpractices) — _@lefticus_
- [The C++ Core Guidelines](https://github.com/isocpp/CppCoreGuidelines) — _@isocpp_
- [C++ Best Practices (CppCon)](https://cppcon.org/cpp-best-practices/)
- [C++ Best Practices by Puppet Labs](https://github.com/puppetlabs/cppbestpractices) — _@puppetlabs_
- [Modern C++ Exception Handling](https://docs.microsoft.com/en-us/cpp/cpp/errors-and-exception-handling-modern-cpp) — _Microsoft_
- [Top Ten Tips for Correct C++ Coding](https://www.informit.com/articles/article.aspx?p=1712962)

* * *

### 🦀 Rust Best Practices

- [Rust Style Guide](https://github.com/ubsan/style/blob/master/guide.md) — _@ubsan_
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
- [Design Patterns in Rust](https://refactoring.guru/design-patterns/rust) — _Refactoring.Guru_

* * *

## Enterprise & JVM Languages

### ☕ Java Best Practices

- [Java Best Practices](https://github.com/in28minutes/java-best-practices) — _@in28minutes_
- [Selenium Best Practices](https://github.com/previousdeveloper/Selenium-best-practices) — _@previousdeveloper_
- [Java Style Guide (Ray Wenderlich)](https://github.com/raywenderlich/java-style-guide) — _@raywenderlich_
- [Java Best Practices Guide](https://howtodoinjava.com/java-best-practices/)
- [30 Java Programming Tips for Beginners](https://www.javacodegeeks.com/2015/06/java-programming-tips-best-practices-beginners.html)

* * *

### 🌀 Kotlin Best Practices

- [Best Practices in Kotlin](https://github.com/JackyAndroid/kotlin-best-practices) — _@JackyAndroid_
- [Kotlin Style Guide](https://github.com/yole/kotlin-style-guide) — _@yole_
- [Kotlin Style Guide (Ray Wenderlich)](https://github.com/raywenderlich/kotlin-style-guide) — _@raywenderlich_

* * *

### 🌀 Scala Best Practices

- [Scala Best Practices](https://github.com/alexandru/scala-best-practices) — _@alexandru_
- [Databricks Scala Guide](https://github.com/databricks/scala-style-guide) — _@databricks_

* * *

### 🖥️ C\# Best Practices

- [C# Coding Best Practices – Conventions with Examples](https://www.freecodecamp.org/news/coding-best-practices-in-c-sharp/)
- [22 C# Best Practices](https://code-maze.com/csharp-22-best-practices/)

* * *

## Web Backend

### 🟢 Node.js Best Practices

- [Node.js Style Guide](https://github.com/felixge/node-style-guide) — _@felixge_
- [RisingStack Node.js Style Guide](https://github.com/RisingStack/node-style-guide) — _@RisingStack_

* * *

### 🐍 Python Best Practices

- [Python Best Practices – Become an Expert](https://data-flair.training/blogs/python-best-practices/)
- [Best of the Best Practices (BOBP) Guide](https://gist.github.com/sloria/7001839) — _@sloria_
- [Python Best Practices (Toptal)](https://www.toptal.com/python/tips-and-practices)
- [Python Code Style Guide](https://docs.python-guide.org/writing/style/)
- [11 Tips to Write Better Python Code](https://www.python-engineer.com/posts/11-tips-to-write-better-python-code/)
- [Python Tutorial: Best Practices & Mistakes](https://jaxenter.com/python-tutorial-best-practices-145959.html)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python) — _Refactoring.Guru_

* * *

### 💎 Ruby Best Practices

- [Ruby Style Guide](https://github.com/airbnb/ruby) — _@airbnb_
- [Ruby Tricks & Best Practices](https://github.com/franzejr/best-ruby) — _@franzejr_
- [Best Practice Patterns in Ruby](https://github.com/avdi/sbpprb) — _@avdi_
- [Ruby Best Practices (Gregory Brown)](https://github.com/practicingruby/rbp-book) — _@practicingruby_
- [The Ruby Style Guide](https://github.com/bbatsov/ruby-style-guide) — _@bbatsov_
- [Shopify Ruby Style Guide](https://github.com/Shopify/ruby-style-guide) — _@Shopify_
- [53 Ruby on Rails Interview Questions](https://medium.com/ruby-daily/53-ruby-on-rails-interview-questions-and-answers-eb99eed1aeb7)
- [Ruby Best Practices (Toptal)](https://www.toptal.com/ruby/tips-and-practices)
- [Ruby Best Practices for Beginners](https://deepsource.io/blog/ruby-dev-best-practices-for-beginners/)
- [Ruby Timeouts Guide](https://github.com/ankane/the-ultimate-guide-to-ruby-timeouts) — _@ankane_
- [Design Patterns in Ruby](https://refactoring.guru/design-patterns/ruby) — _Refactoring.Guru_
- [Best Practices for Writing Ruby](https://reintech.io/blog/best-practices-for-writing-ruby)
- [6 Ruby Best Practices for Beginners](https://www.codementor.io/ruby-on-rails/tutorial/6-ruby-best-practices-beginners-should-know)

* * *

### 🚂 Rails Best Practices

- [Rails Style Guide](https://github.com/bbatsov/rails-style-guide) — _@bbatsov_
- [rails\_best\_practices](https://github.com/flyerhzm/rails_best_practices) — _@flyerhzm_
- [RSpec Style Guide](https://github.com/reachlocal/rspec-style-guide) — _@reachlocal_
- [RSpec Best Practices](https://github.com/abinoda/rspec-best-practices) — _@abinoda_
- [Rails Database Best Practices](https://blog.carbonfive.com/rails-database-best-practices/)
- [Active Record Query Optimization Tips](https://medium.com/@User3141592/active-record-query-performance-tips-a3c3947b968)
- [ActiveRecord SQL Query Optimization](https://phrase.com/blog/posts/activerecord-speed-up-your-sql-queries/)
- [Arel Cheatsheet](https://devhints.io/arel)
- [Production Rails](https://github.com/ankane/production_rails) — _@ankane_
- [Securing Sensitive Data in Rails](https://ankane.org/sensitive-data-rails) — _@ankane_
- [Toptal Rails Best Practices](https://www.toptal.com/ruby-on-rails/tips-and-practices)

* * *

### 🐘 PHP Best Practices

- [PHP: The Right Way](https://github.com/codeguy/php-the-right-way) — _@codeguy_
- [PHP Knowledge](https://github.com/php-earth/php-knowledge) — _@php-earth_
- [PHP Coding Standards](https://github.com/maxdmyers/php-style-guide) — _@maxdmyers_

* * *

### 🎯 Laravel Best Practices

- [Laravel: The Right Way](https://github.com/laraveltherightway/laraveltherightway.github.io) — _@laraveltherightway_
- [Laravel Best Practices](https://github.com/uonick/laravel-best-practices) — _@uonick_

* * *

### 🟣 NestJS Best Practices

- [Best NestJS Practices and Advanced Techniques](https://dev.to/drbenzene/best-nestjs-practices-and-advanced-techniques-9m0)

* * *

## Functional & Specialized

### 🧪 Elixir Best Practices

- [The Elixir Style Guide](https://github.com/christopheradams/elixir_style_guide) — _@christopheradams_
- [Elixir Style Guide](https://github.com/lexmag/elixir-style-guide) — _@lexmag_
- [Credo's Elixir Style Guide](https://github.com/rrrene/elixir-style-guide) — _@rrrene_
- [10 Killer Elixir Tips #1](https://medium.com/blackode/10-killer-elixir-tips-2a9be1bec9be)
- [10 Killer Elixir Tips #2](https://medium.com/blackode/10-killer-elixir-tips-2-c5f87f8a70c8)
- [10 Killer Elixir Tips #3](https://medium.com/blackode/10-killer-elixir-tips-3-5c196eaec376)
- [Elixir Cheatsheet](https://devhints.io/elixir)
- [Elixir Metaprogramming Cheatsheet](https://devhints.io/elixir-metaprogramming)

* * *

### 🐹 Go (Golang) Best Practices

- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md) — _@uber-go_
- [Go Best Practices](https://github.com/mehrdadrad/GoBestPractices) — _@mehrdadrad_
- [Go Style Guide](https://github.com/AgtLucas/go-style-guide) — _@AgtLucas_
- [Golang Tutorial Series](https://golangbot.com/learn-golang-series/)
- [Golang Cheat Sheet (Golang Dojo)](https://products.golangdojo.com/golang-cheat-sheet-by-golang-dojo)
- [Soham Kamani – Golang](https://www.sohamkamani.com/golang/)
- [Design Patterns in Go](https://refactoring.guru/design-patterns/go) — _Refactoring.Guru_

* * *

### 🍎 Swift Best Practices

- [Swift Style Guide (Eure)](https://github.com/eure/swift-style-guide) — _@eure_
- [Design Patterns in Swift](https://github.com/ochococo/Design-Patterns-In-Swift) — _@ochococo_
- [Swift Style Guide (Ray Wenderlich)](https://github.com/raywenderlich/swift-style-guide) — _@raywenderlich_

* * *

### 🍏 Objective-C Best Practices

- [NYTimes Objective-C Style Guide](https://github.com/NYTimes/objective-c-style-guide) — _@NYTimes_
- [Objective-C Style Guide (Ray Wenderlich)](https://github.com/raywenderlich/objective-c-style-guide) — _@raywenderlich_
- [GitHub Objective-C Style Guide](https://github.com/github/objective-c-style-guide) — _@github_
- [Code Style & Best Practices for Objective-C](https://github.com/wangshengjia/-Code-Style---Best-Practise-for-Objective-C) — _@wangshengjia_

* * *

### 🐪 Perl Best Practices

- [Effective Perl Programming: Idiomatic Perl](https://www.effectiveperlprogramming.com/)
- [Perl Style Guide](https://perldoc.perl.org/perlstyle) — _Perl.org_

* * *

### 🪶 Lua Best Practices

- [Lua Best Practices (Lua.org)](https://www.lua.org/gems/sample.pdf)
- [Lua Style Guide](http://lua-users.org/wiki/LuaStyleGuide)

* * *

# 🎨 Frontend Development

## Core Technologies

### 🌐 HTML Best Practices

- [HTML Best Practices](https://github.com/hail2u/html-best-practices) — _@hail2u_
- [HTML5 (and Some CSS) Best Practice](https://www.codeproject.com/Tips/666578/HTML-and-Some-CSS-Best-Practice)
- [Frontend Guidelines](https://github.com/bendc/frontend-guidelines) — _@bendc_
- [Google HTML Style Guide](https://google.github.io/styleguide/htmlcssguide.html#HTML) — _@google_

* * *

### 🎨 CSS Best Practices

- [Airbnb CSS / Sass Styleguide](https://github.com/airbnb/css) — _@airbnb_
- [Dropbox (S)CSS Style Guide](https://github.com/dropbox/css-style-guide) — _@dropbox_
- [CSS Coding Standards & Best Practices](https://github.com/stevekwan/best-practices/blob/master/css/best-practices.md) — _@stevekwan_
- [Google CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html#CSS) — _@google_

* * *

### 🎨 SASS Best Practices

- [Sass Coding Guidelines](https://github.com/bigcommerce/sass-style-guide) — _@bigcommerce_
- [Sass-Guidelines](https://github.com/blackfalcon/Sass-Guidlines/blob/master/SASS-Guidelines.md) — _@blackfalcon_
- [Sass-lang Style Rules](https://sass-lang.com/documentation/style-rules)

* * *

### 📜 JavaScript Best Practices

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) — _@airbnb_
- [ES6 Cheatsheet](https://github.com/DrkSephy/es6-cheatsheet) — _@DrkSephy_
- [Common JavaScript "Gotchas"](https://github.com/stevekwan/best-practices/blob/master/javascript/gotchas.md) — _@stevekwan_
- [Pragmatic JavaScript Standards](https://github.com/stevekwan/best-practices/blob/master/javascript/best-practices.md) — _@stevekwan_
- [JavaScript 规范](https://github.com/adamlu/javascript-style-guide) — _@adamlu_
- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html) — _@google_
- [JavaScript The Right Way](https://jstherightway.org/) — _@braziljs_
- [MDN JavaScript Guidelines](https://developer.mozilla.org/en-US/docs/MDN/Guidelines/Code_guidelines/JavaScript) — _@mozilla_
- [W3C JavaScript Best Practices](https://www.w3.org/wiki/JavaScript_best_practices) — _@w3c_
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript) — _@ryanmcdermott_

* * *

### 🟦 TypeScript Best Practices

- [TypeScript Best Practices](https://github.com/BestCoderDotInfo/TypeScript-best-practices) — _@BestCoderDotInfo_

* * *

## Frameworks & Libraries

### ⚛️ ReactJS Best Practices

- [Advanced ReactJS Patterns](https://github.com/kentcdodds/advanced-react-patterns-v2) — _@kentcdodds_
- [React Interview Questions & Answers](https://github.com/sudheerj/reactjs-interview-questions) — _@sudheerj_

* * *

### 📱 React Native Best Practices

- [React Native Guide](https://github.com/reactnativecn/react-native-guide) — _@reactnativecn_

* * *

### 🖼️ Vue Best Practices

- [Tips & Best Practices (Vue 0.12)](https://012.vuejs.org/guide/best-practices.html)
- [10 Good Practices for Large Vue.js Projects](https://www.telerik.com/blogs/10-good-practices-building-maintaining-large-vuejs-projects)
- [12 VueJS Best Practices for Pro Developers](https://learnvue.co/2020/01/12-vuejs-best-practices-for-pro-developers/)

* * *

### 🅰️ Angular Best Practices

- [AngularJS Style Guide](https://github.com/mgechev/angularjs-style-guide) — _@mgechev_
- [Angular 2 Style Guide](https://github.com/mgechev/angular2-style-guide) — _@mgechev_
- [Angular.js Advanced Design Patterns](https://github.com/trochette/Angular-Design-Patterns-Best-Practices) — _@trochette_

* * *

### ⚡ Next.js Best Practices

- [Best Practices for Clean React/Next.js Projects](https://blogs.perficient.com/2023/04/25/best-practices-for-building-and-sustaining-a-clean-react-next-js-project/)
- [10 Tips for Optimal Next.js Performance](https://www.fronttribe.com/stories/next-js-best-practices-10-tips-for-optimal-performance)
- [Best Practices to Increase Next.js Speed](https://stackoverflow.blog/2022/12/20/best-practices-to-increase-the-speed-for-next-js-apps/)

* * *

### ⚡ Nuxt Best Practices

- [10 Nuxt Best Practices](https://climbtheladder.com/10-nuxt-best-practices/)

* * *

## Performance

### 🚀 Frontend Performance Best Practices

- [Frontend Performance Best Practices (Roadmap.sh)](https://roadmap.sh/best-practices/frontend-performance)
- [Web Vitals Best Practices (Google)](https://web.dev/vitals/)
- [High Performance Web Apps (MDN)](https://developer.mozilla.org/en-US/docs/Learn/Performance)

* * *

# 🗄️ Database & Data

## SQL Databases

### 📊 SQL Best Practices

- [SQL Style Guide](https://www.sqlstyle.guide/)
- [Best Practices for Writing SQL Queries](https://www.metabase.com/learn/sql-questions/sql-best-practices)
- [SQL Performance Explained (Markus Winand)](https://use-the-index-luke.com/)
- [GitLab SQL Style Guide](https://about.gitlab.com/handbook/business-technology/data-team/platform/sql-style-guide/)

* * *

### 🐘 PostgreSQL Best Practices

- [PostgreSQL Performance Best Practices](https://www.adservio.fr/post/postgresql-performance-best-practices)
- [Best Practices for PostgreSQL Database](https://www.e2enetworks.com/blog/best-practices-for-postgresql-database)
- [Run ANALYZE, Run ANALYZE, Run ANALYZE](https://ottertune.com/blog/run-postgresql-analyze-to-fix-a-slowdow-in-db/)
- [Best Practices for Designing PostgreSQL Databases](https://appmaster.io/blog/best-practices-for-designing-postgresql-databases)

* * *

### 🐬 MySQL Best Practices

- [MySQL Performance Best Practices](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL Security Best Practices](https://dev.mysql.com/doc/refman/8.0/en/security-guidelines.html)

* * *

## NoSQL & Big Data

### 📦 NoSQL Best Practices

- [10 NoSQL Data Modeling Best Practices](https://climbtheladder.com/10-nosql-data-modeling-best-practices/)
- [MongoDB Schema Design Best Practices](https://www.mongodb.com/developer/products/mongodb/mongodb-schema-design-best-practices/)
- [11 MongoDB Security Features & Best Practices](https://satoricyber.com/mongodb-security/11-mongodb-security-features-and-best-practices/)

* * *

# 📱 Mobile Development

## 📱 Flutter Best Practices

- [Performance Best Practices](https://flutter.dev/docs/perf/rendering/best-practices)
- [Flutter: Best Practices and Tips](https://medium.com/flutter-community/flutter-best-practices-and-tips-7c2782c9ebb5) — _Kinjal Dhamat_
- [Flutter Development Best Practices](https://heartbeat.fritz.ai/flutter-development-best-practices-3e162765340a) — _Derrick Mwiti_

* * *

## 🎯 Dart Best Practices

- [Dart & Flutter Best Practices](https://lazebny.io/flutter-best-practices/)
- [Performance Best Practices](https://docs.flutter.dev/perf/best-practices)
- [Writing Clean Code in Dart: Best Practices & Design Patterns](https://clouddevs.com/dart/clean-code/)

* * *

# ☁️ DevOps & Infrastructure

## Cloud & Deployment

### ☁️ AWS Best Practices

- [AWS Best Practices (Roadmap.sh)](https://roadmap.sh/best-practices/aws)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

* * *

### 📦 Microservices & Cloud-Native Best Practices

- [12 Factors for Building Cloud-Native Apps](https://12factor.net/)
- [Microservices Best Practices (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/microservices/)
- [Cloud-Native Patterns (CNCF)](https://github.com/cncf/presentations)

* * *

## Security

### 🔐 API Security Best Practices

- [API Security Best Practices (Roadmap.sh)](https://roadmap.sh/best-practices/api-security)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

* * *

### 🔐 DevSecOps & Security Best Practices

- [OWASP Top 10 (2024)](https://owasp.org/www-project-top-ten/)
- [Zero Trust Security Model](https://www.microsoft.com/security/blog/zero-trust/)
- [Best Practices for Secure CI/CD](https://snyk.io/blog/devsecops-best-practices/)

* * *

# 🤖 AI & Data Science

## 🤖 AI/ML Engineering Best Practices

- [MLOps Best Practices (Google Cloud)](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [Responsible AI Practices (Google)](https://ai.google/responsibilities/responsible-ai-practices/)
- [Best Practices for LLM Applications](https://www.promptingguide.ai/)
- [IBM Data Science – Best Practices](https://github.com/IBM/data-science-best-practices)
- [AI Best Practices (XenonStack Blog)](https://www.xenonstack.com/blog/ai-best-practices)
- [Best Practices for Deep Learning in Julia (FastAI.jl)](https://github.com/FluxML/FastAI.jl)
- [ETL Best Practices with Airflow](https://github.com/gtoonstra/etl-with-airflow)

* * *

## 🤖 AI Tools for Developers

- [9 of the Best AI Tools for Software Developers in 2024](https://www.stepsize.com/blog/best-ai-tools-for-software-developers)
- [The Best AI Tools for Developers in 2024](https://daily.dev/blog/the-best-ai-tools-for-developers-in-2024)
- [Awesome AI Tools](https://github.com/mahseema/awesome-ai-tools) — _@mahseema_
- [Awesome AI-Powered Developer Tools](https://github.com/jamesmurdza/awesome-ai-devtools) — _@jamesmurdza_
- [Best Practices for Coding with AI (2024)](https://blog.codacy.com/best-practices-for-coding-with-ai)
- [AI Tools for Developers: 5 Types of Tools & How to Choose](https://swimm.io/learn/ai-tools-for-developers/ai-tools-for-developers-5-types-of-tools-and-how-to-choose)
- [The Do's and Don'ts of Using AI in Software Development](https://www.kodeco.com/41989083-the-do-s-and-don-ts-of-using-ai-in-software-development)
- [10 Best Practices for Secure AI Development](https://snyk.io/blog/10-best-practices-for-securely-developing-with-ai/)
- [AI Hacks to Maximize Productivity in 2024](https://www.smarttrick.org/post/work-smarter-not-harder-ai-hacks-to-maximize-your-productivity-in-2024)

* * *

# 🛠️ Development Tools & Practices

## Version Control & Collaboration

### 🔎 Code Review Best Practices

- [Code Review Best Practices (Roadmap.sh)](https://roadmap.sh/best-practices/code-review)

* * *

### 🧑‍🤝‍🧑 Team & Collaboration Best Practices

- [Remote Engineering Best Practices](https://about.gitlab.com/remote/)
- [Agile Development Best Practices](https://www.atlassian.com/agile)
- [Effective Pair Programming](https://martinfowler.com/articles/on-pair-programming.html)

* * *

## Scripting & Automation

### 🐚 Bash Script Best Practices

- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)
- [progrium/bashstyle](https://github.com/progrium/bashstyle)
- [Best Practices for Bash Scripts](https://hyperskill.org/learn/step/19230)
- [Best Practices for Writing Bash Scripts](https://expeditor.chef.io/docs/patterns/bash-scripts/)

* * *

## Performance & Architecture

### 🏗️ System Design Best Practices

- [System Design 101](https://github.com/ByteByteGoHq/system-design-101#system-design-101) — _@ByteByteGoHq_

* * *

### ⚡ Performance & Scalability Best Practices

- [Scaling Applications (Netflix Tech Blog)](https://netflixtechblog.com/)

* * *

# 🌍 Specialized Languages

## 📊 R Best Practices

- [Beyond Basic R – Introduction & Best Practices](https://waterdata.usgs.gov/blog/intro-best-practices/)
- [R Code – Best Practices](https://www.r-bloggers.com/r-code-best-practices/)
- [Best Practices for Writing R Code](https://swcarpentry.github.io/r-novice-inflammation/06-best-practices-R.html) — _@swcarpentry_
- [R Coding Style Best Practices](https://www.datanovia.com/en/blog/r-coding-style-best-practices/)
- [Good Practices in R Programming (ETH Zürich)](https://stat.ethz.ch/Teaching/maechler/R/useR_2014/Maechler-2014-pr.pdf)

* * *

# 🤝 Contributing

Contributions are always welcome! 🎉
Before contributing, please read the [Contribution Guidelines](https://github.com/dereknguyen269/programing-best-practices/blob/master/contributing.md).

* * *

# 📜 License

[![CC0](https://camo.githubusercontent.com/dc5dafd103feb167be372f069c52972bd8cd86cf2fdfc28a1b8aa44e35463b27/68747470733a2f2f6c6963656e7365627574746f6e732e6e65742f702f7a65726f2f312e302f38387833312e706e67)](https://creativecommons.org/publicdomain/zero/1.0/)
This project is licensed under **Creative Commons Zero v1.0 Universal (CC0 1.0)** — _Public Domain Dedication_.

---

```
