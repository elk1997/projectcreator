# Project Creator for web developers on Mac

This command line tool help web developers to create new web project set. Once you run the script, the following features will be automated.

Do not stop coding what you have in your mind!

## Features
 * adds new configurations to your hosts file to access local server.
 * adds new configurations to your .htaccess file for your virtual host.
 * creates project directory.
 * sets up html/css/javascript from some default templates.
 * restarts Apache.

## Configuration
### Configuration Settings
Change the configuration settings on `config.py` if you need.
You may want to change **projectPath**. **projectPath** indicates the base path to place project directory.

### Default templates
Two templates are originally placed, but you can put in more default templates. Just put in your own html/css/javascript packed in one directory to `default` directory.

e.g. You put in the directory named **mobile** to `default` directory. Command line will be the following.

	> Choose a template from 'bootstrap/plain/mobile'. []

## Usage
Run the following command.

	python ./run.py

## Notes
- It may be working on Linux.

## Todo
-  Woring for Nginx.
-  Creating also project files for Sublime Text 2, Eclipse, and so on.

## Author
 * Created by [Takashi Aoki](http://elkc.net).
 * Email address: <aoki@elkc.net>
 * [@elk1997](https://twitter.com/elk1997) on Twitter.