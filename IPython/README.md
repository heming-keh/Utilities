Install
============================================================

```bash
  git clone git@github.com:heming-keh/IPython.git ~/.ipython/profile_default/startup/
```

Usage
============================================================

```bash
# In the current directory '.', search for the file name matching pattern [ab]
find . [ab]

# In the home directory, search for the files which size are bigger than 100M
find /home .* -size >100M

# In the home directory, search for the files which size are smaller than 100M
find /home .* -size <100M

# In the home directory, search for the files which size are between 100M~200M
find /home .* -size 100M~200M
```

License
============================================================

Apache License 2.0 https://www.apache.org/licenses/LICENSE-2.0
