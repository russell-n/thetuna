Help Page
=========

.. currentmodule:: optimization.infrastructure.helppage
.. _help-page:

This is a module to help with creating help-pages.



Font Constants
--------------

ASCII codes are used to change the text sent to standard output. The available codes are:

   * BLUE
   * RED
   * RESET
   * BOLD

* RESET gets rid of the previously set codes (it turns off bold and makes the color black).
* These codes are used in the TEMPLATE so you can use them but it is not required.

Python TextWrapper
------------------

`TextWrapper <http://docs.python.org/2/library/textwrap.html#textwrap.TextWrapper>`_ is being used to make the output (hopefully) a little nicer. These are some notes generated while I figure out how to use it. TextWrapper has many options and two methods but I anticipate only use the `width`, and `subsequent_indent` attributes and the `fill(text)` method.

.. currentmodule:: textwrap
.. autosummary::

   textwrap.TextWrapper
   textwrap.TextWrapper.width
   textwrap.TextWrapper.drop_whitespace
   textwrap.TextWrapper.subsequent_indent
   textwrap.TextWrapper.fill

::

    if output_documentation:
        indent = ' ' * 5
        tw = textwrap.TextWrapper(width=80, subsequent_indent=indent,
                                  drop_whitespace=False)
        text = """
    A Little Text:
    
    Now is the winter of our discontent;
    Made glorious summer by this Son of York;
    And all the clouds that lour'd upon our house;
    In the deep bosom of the ocean buried.
    """
        wrapped_text = tw.fill(text)
        print wrapped_text
    

::

     A Little Text:  Now is the winter of our discontent; Made glorious summer by 
         this Son of York; And all the clouds that lour'd upon our house; In the 
         deep bosom of the ocean buried. 
    



That was not really what I wanted -- I thought that the empty line before the paragraph would be preserved. It looks like in order to do what I wanted you would need to do it as two separate print calls (and and initial indent added so that the body will be entirely indented).

.. autosummary::

   textwrap.TextWrapper.initial_indent

::

    if output_documentation:
        tw.initial_indent = indent
        header = 'A Little Text:\n'
        text = """
    Now is the winter of our discontent;
    Made glorious summer by this Son of York;
    And all the clouds that lour'd upon our house;
    In the deep bosom of the ocean buried.
    """
        print header
        headerless_wrapped_text = tw.fill(text)
        print headerless_wrapped_text
    

::

    A Little Text:
    
          Now is the winter of our discontent; Made glorious summer by this Son of 
         York; And all the clouds that lour'd upon our house; In the deep bosom of 
         the ocean buried. 
    



Okay, but now the output is all blocky. Try again with the `drop_whitespace` set to True.

::

    if output_documentation:
        tw.drop_whitespace = True    
        print header
        headerless_wrapped_text = tw.fill(text)
        print headerless_wrapped_text
    

::

    A Little Text:
    
          Now is the winter of our discontent; Made glorious summer by this Son of
         York; And all the clouds that lour'd upon our house; In the deep bosom of
         the ocean buried.
    



Well, it *is* closer, but that first line in the body is still mysteriously off.

::

    if output_documentation:
        tw.initial_indent = ' ' * 4
        headerless_wrapped_text = tw.fill(text)
        print header
        print headerless_wrapped_text
    

::

    A Little Text:
    
         Now is the winter of our discontent; Made glorious summer by this Son of
         York; And all the clouds that lour'd upon our house; In the deep bosom of
         the ocean buried.
    



.. warning:: I initially misspelled ``initial_indent`` and it just silently did not change the output behavior -- use the constructor instead of assigning the values like I do here.

Less is More
------------

In addition to using `TextWrap` I will use the less command to keep the text from rolling off the screen.

This will break if the computer does not have `less`, which seems unlikely since I do not run Windows, but just in case I will use `check_call` so that it can fall back to printing.

.. currentmodule:: subprocess
.. autosummary::

   subprocess.check_call

.. currentmodule:: shlex
.. autosummary::

   shlex.split

::

    if output_documentation:
        long_text = text * 100
        long_wrapped_text = tw.fill(long_text)
        command = shlex.split('echo "{0}" | less -R'.format(long_wrapped_text))
    
        subprocess.check_call(command)
        try:
            subprocess.check_call('ummagumma')
        except OSError as error:
            print wrapped_text    
    

::

     A Little Text:  Now is the winter of our discontent; Made glorious summer by 
         this Son of York; And all the clouds that lour'd upon our house; In the 
         deep bosom of the ocean buried. 
    



The output from the first call will not show up in the documentation output, so it might not be obvious that it does not work. Apparently to do a pipe you need to use ``Popen`` and ``communicate``.

.. currentmodule:: subprocess
.. autosummary::

   Popen
   Popen.communicate
   PIPE

So you need to do something like this::

    command = 'less -R'.split()
    subprocess.Popen(command, stdin=subprocess.PIPE).communicate(input=long_wrapped_text)

The HelpPage
------------

With that background material to the aside, here is the actual pager.

.. uml::

   HelpPage -|> BaseClass
   HelpPage o- subprocess.Popen
   HelpPage o- textwrap.TextWrapper

.. currentmodule:: ape.plugins.helppage
.. autosummary::
   :toctree: api

   HelpPage
   HelpPage.__call__
   HelpPage.text

.. warning:: The HelpPage is using the `string.format <http://docs.python.org/2/library/stdtypes.html#str.format`_ method so putting curly braces ('{}') in the help-strings is probably a bad idea. If you need them, make sure to double them -- ('{{like this}}').

If the `headers` argument is not set then the keys from the `sections` argument will be used (this way an ordered dict can be used to make things simpler).
   


Suggested Sections
------------------

My original idea was to put suggested sections in the HelpPage but it made the constructor-signature too big (and seemed too inflexible). So here are what the sections were going to be (taken from `man pages <http://man7.org/linux/man-pages/man7/man-pages.7.html>`_):

.. csv-table:: Suggested Sections
   :header: Header, Contents

   NAME, The topic of the help and a short description.
   SYNOPSIS, Comprehensive listing of usage options.
   CONFIGURATION, Setting up.
   DESCRIPTION, The main body of the help describing the topic.
   OPTIONS, Description of the options.
   RETURN VALUE, Values returned on exit (if any).
   ERRORS, Possible errors raised.
   FILES, Paths to relevant files.
   NOTES, Miscellaneous notes.
   BUGS, Known bugs.
   EXAMPLE, Usage examples.
   AUTHORS, Code authors.
   SEE ALSO, Related topics.

The man-pages have other sections but these were the ones I thought might be the most relevant for the way I am planning to use this.   




Example Use
-----------

It is getting too hard to test this thing, so I will just do a plain old usage check.

::

    if __name__ == '__main__':
        headers = 'title poem author source'.split()
        poem = """
        They fuck you up, your mum and dad.
            They may not mean to, but they do.
        They fill you with the faults they had
            And add some extra, just for you.
        
        But they were fucked up in their turn
            By fools in old-style hats and coats,
        Who half the time were soppy-stern
            And half at one another's throats.
        
        Man hands on misery to man.
            It deepens like a coastal shelf.
        Get out as early as you can,
            And don't have any kids yourself.
        """
        poem = textwrap.dedent(poem)
        title='{red}This Be The Verse{reset}'
        author = '{blue}Philip Larkin{reset}'
        source = 'http://www.poetryfoundation.org/poem/178055'
        sections = dict(zip(headers, (title, poem, author, source)))
        pager = HelpPage(headers = headers,
                         sections = sections)
        pager()
    

