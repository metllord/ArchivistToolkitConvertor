Archivist Toolkit XML Creator
==============================

This is just a simple utility to convert a tab-delimited file to XML for Arcivist Toolkit. It is not
generalized for other inputs yet.

I created this to make Judy's life easier. If you find it useful, feel free to use and change it.

Usage
-----

1. Use Excel to ouput worksheets to tab delimited files. Save these files in a directory and place the
convert.py in the same directory.

2. Run the command python convert.py. To convert one or more documents, specify that document as the argument.
To convert the entire directory, pass '*' as the first arguement.

EX:

.. sourcecode::
    $ python convert.py SourceFile.tab OtherSource.tab (converts these two files)
    $ python convert.py * (Converts all files in working directory)

3. The program will move the source files for the completed conversions to the Finished folder. The
XML files will be placed in the working directory. If there are errors, they will be listed in errors.txt
and the tab files will be kept in the working directory.

Requirements
------------

* Python 2.7 (http://www.python.org/download/)
* Excel (for conversion to Tab)

File List
---------

* convert.py
* template.xml