# email
A simple test project I made because mail wasn't working

# Installation

``` console
git clone https://github.com/zack-carnet/email.git
cd email
pip install .
```

# Usage

  * Create a `.emailrc` in your home directory and add the following minimal config to it

  ``` ini
[Aliases]

[Settings]

  ```

  * You may also add the environment variables `EMAIL_ADDRESS` and `EMAIL_PASSWORD` with the appropriate values for convenience.
 
  * Use the `--help` option on any command for info regarding it

```console
❯ email --help
Usage: email [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  alias   sets an alias to an address or a list of addresses
  config  Set or Update the value of a setting in your '.emailrc' file
  debug   Sets up a Debugging server
  send    Sends a mail
  
```
  * Example
  
``` console
email send -t "Hello person with a made up email" madeupemail@gmail.com 
```

# Config

  * Here's an example (defaults) configuration:
  
  ``` ini
[Settings]
debug = False
address_at = EMAIL_ADDRESS
password_at = EMAIL_PASSWORD
server = smtp.gmail.com
port = 465

[Aliases]

  ```
  * Though it can deduce the server and port for common domains you must explicitly specify it in the config if it is not among the following:
  
 | domain  | server              | port |
 |:-------:|:-------------------:|:----:|
 | gmail   | smtp.gmail.com      | 465  |
 | outlook | smtp.office365.com  | 587  |
 | yahoo   | smtp.mail.yahoo.com | 465  |

  * `address_at` and `password_at`are the the environment variables where it looks for you email adress and password respecively. (EMAIL_ADDRESS and EMAIL_PASSWORD default values)

  * Note: You can also use the `email config` command (see help) to add these settings

# Aliases

  * Use the `email alias` command to add aliases.
  
  * You can add aliases of multiple aliases as well. Here's an example:

``` ini
[Settings]
debug = False
address_at = EMAIL_ADDRESS
password_at = EMAIL_PASSWORD
server = smtp.gmail.com
port = 465

[Aliases]
me = me@gmail.com
some_person = someperson@gmail.com
another_person = anotherperson@gmail.com
people = some_person another_person
parents = mom@gmail.com dad@gmail.com
more_people = people parents newperson@gmail.com
```
