Sublime-SessionManager
======================

Why?
----

Let's be honest: Sublime Text's session management is weird. It doesn't outright suck, but it's inflexible and hard to use if you don't have a project file.

As long as you work in a single project everything is fine, but as soon as you want have multiple projects open at once, or just want to open a bunch of files and hack away, the sublime's session management screws you over.

Sometimes you simply want to save your current state, do something different, and come back to wherever you left. Preferably quick and uncomplicated.

If you've ever been in such a situation, then this plugin is for you.

Installation
------------

The easiest way to install Session Manager is obviously through Sublime Package Control. Open `Package Control` (`Preferences` > `Package Control`), select `Package Control: Install package`, and search for "Session Manager".

Alternatively, you can install the plugin via git or simply download the repository.

For this you have to navigate to your package folder (use `Preferences` > `Browse Packages...` for this) and clone or unpack this repository in there.

How to use
----------

Using Session Manager you can *save*, *load* and *delete* your current state. It handles all currently opened __windows__, __folders__ and __files__, down to the currently visible __region__ and all __selections__ and __cursors__.

When you load a session you can continue your work as if nothing ever happened.

The commands, accessible through the command palette (`ctrl+shift+p`), are:

    Session Manager: Save Session
    Session Manager: Load Session
    Session Manager: Delete Session

The default name for a session consists of the keyword __session__ and the __current timestamp__ (example: `session_15-03-13T15-37-22`). If you don't like the format, you can configure it with the `session_name_format` setting.

Each of your sessions will be saved in a `Packages/User/sessions` folder. This can be changed via the `session_path` setting.

The sessions are simple JSON files; this means you can edit and change them as you see fit.

You can also bind the commands to the keyboard:

    Session Manager: Save Session       is   save_session,
    Session Manager: Load Session       is   load_session, and
    Session Manager: Delete Session     is   delete_session.

Configuration
-------------

Just take a look at the default configuration file to learn about the available options:

```js
{
    // If session_path is null, the sessions will be saved in your sublime User folder in sessions
    // (User/sessions)
    "session_path": null,

    // The format which shall be used to generate the default session name;
    // Example result: session_15-02-07T15-09-32
    // take a look at the python docs for details:
    // https://docs.python.org/3.3/library/datetime.html#strftime-strptime-behavior
    "session_name_format": "session_%y-%m-%dT%H-%M-%S"
}
```


Plans for the future
--------------------

These are the features I'm planning to add in the future:

- Save only current window
- Close everything and open a new window after saving (*configurable or another command?*)
- More information when loading sessions (*so we can easier distinguish between them*)

If you think I should add some other features, then don't hesitate to open an issue.

And if you want to make a donation, you can find me on [Gratipay](https://gratipay.com/). Thank you in advance!

__Happy session saving!__
