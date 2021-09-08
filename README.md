# email
A simple test project I made because mail wasn't working

# Installation

``` console
git clone https://github.com/zack-carnet/email.git
cd email
pip install .
```

# Usage
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

# Config

  * Create a .emailrc in your home directory and add the necessary settings to them. Here is an example:
  
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
  ```
  * In the above example `EMAIL_ADDRESS` and `EMAIL_PASSWORD` are supposed to be names of environment variables containing your email address and password or app password respecively.

  * Use the appropriate server and port for your email. However for common domains like the following it deduces it automaically.
  
 | domain  | server              | port |
 |:-------:|:-------------------:|:----:|
 | gmail   | smtp.gmail.com      | 465  |
 | outlook | smtp.office365.com  | 587  |
 | yahoo   | smtp.mail.yahoo.com | 465  |
  
  * Note: You can also use the `email config` command (see help) to add these settings
