Testing The File Storage
========================

.. currentmodule:: ape.parts.storage.tests.testfilestorage
.. autosummary::
   :toctree: api

   TestFileStorage.test_constructor
   TestFileStorage.test_write
   TestFileStorage.test_write_error
   TestFileStorage.test_writeline
   TestFileStorage.test_writelines
   TestFileStorage.test_writeable
   TestFileStorage.test_close


::

    PATH = 'ape/call'
    class TestFileStorage(unittest.TestCase):
        def setUp(self):
            self.storage = FileStorage('test')
            self.mock_file = MagicMock()
            return
    
        def test_constructor(self):
            """
            Does it set up the name and the BaseStorage parent?
            """
            storage = FileStorage(PATH)
            self.assertEqual(PATH, storage.path)
            return
            
        def test_write(self):
            self.storage._file = self.mock_file
            self.storage.write('alpha')
            self.mock_file.write.assert_called_with('alpha')
            
        def test_write_error(self):
            storage = FileStorage(PATH)
            self.assertRaises(ApeError, storage.write, ('',))
            return
    
        def test_writeline(self):
            self.storage._file = self.mock_file
            self.storage.writeline('beta')
            self.mock_file.write.assert_called_with('beta\n')
            return
    
        def test_writelines(self):
            text = 'gamma delta sigma rho'.split()
            self.storage._file = self.mock_file
            self.storage.writelines(text)
            self.mock_file.writelines.assert_called_with(text)
            return
    
        def test_writeable(self):
            mocked = mock_open()
            name = 'ummagumma.txt'
            full_name = 'test/' + name
            storage = FileStorage('test/')
            with patch('__builtin__.open', mocked):
                self.assertFalse(storage.writeable)
                opened = storage.open(name)
                self.assertTrue(opened.writeable)
                opened.close()
                self.assertFalse(opened.writeable)
            return
        
        def test_close(self):
            mock_file = MagicMock()
            self.storage._file = mock_file
            self.storage.closed = False
            self.storage.close()
            mock_file.close.assert_called_with()
            self.assertTrue(self.storage.closed)
            return
        
        def tearDown(self):
            if os.path.isdir(PATH):
                shutil.rmtree(PATH)
            return        
    



Testing Open
------------

The `overwrite` and `mode` parameters produce eight possible arrangements. The first-column of the table (`File Exists`) means that there is already a file with the same name as the one passed in. The `Final Name` column refers to whether a new file name is created to protect an existing file or not (`filename` means use given name, `mangled` means change it).

.. csv-table:: Open Parameters
   :header: File Exists, Overwrite, Append, Final Name, Mode

   0,0,0,filename,w
   0,0,1,filename, a
   0,1,0,filename, w
   0,1,1,filename,a
   1,0,0,mangled,w
   1,0,1,filename,a
   1,1,0,filename,w
   1,1,1,filename,a

The last case is ambiguous -- I'll assume that the *append* mode is what's wanted since it's the least destructive, but some kind of warning should probably be issued.

Looking at the table it appears that the only time I actually mangle the file name is if the file exists and neither *overwrite* nor *append* are true.

.. '

.. math::

   mangle &= FileExists \land \lnot(Overwrite \lor Append)\\

.. currentmodule:: ape.parts.storage.tests.testfilestorage
.. autosummary::
   :toctree: api

   TestFileStorageOpen.test_open
   TestFileStorageOpen.test_open_file_exists
   
::

    PATH = 'ape/call'
    class TestFileStorageOpen(unittest.TestCase):
        def setUp(self):
            self.storage = FileStorage('test')
            self.mock_file = MagicMock()
            return
    
        def test_open(self):
            """
            Does it open the file normally if the file doesn't already exist?
            """
            mocked = mock_open()
            name = 'ummagumma.txt'
            full_name = 'test/' + name
            storage = FileStorage('test/')
            with patch('__builtin__.open', mocked):
                self.assertTrue(storage.closed)
                opened = storage.open(name)
                self.assertEqual(full_name, opened.name)
                mocked.assert_called_with(full_name, 'w')
                self.assertFalse(opened.closed)
                self.assertEqual(opened.mode, 'w')
    
                # test append
                opened = storage.open(name, mode='a')
                mocked.assert_called_with(full_name, 'a')
    
                #test over-write
                opened = storage.open(name, overwrite=True)
                mocked.assert_called_with(full_name, 'w')
    
                # test append and over-write
                opened = storage.open(name, overwrite=True, mode='a')
                mocked.assert_called_with(full_name, 'a')
            return
    
        def test_open_file_exists(self):
            """
            Does it mangle the file-names at the right times?
            """
            mocked = mock_open()
            name = 'ummagumma.txt'
            
            storage = FileStorage('test/')
            mock_os_listdir = MagicMock()
            mock_os_path_exists = MagicMock()
            mock_os_path_join = MagicMock()
    
            mock_open_path_exists = True
            mock_os_listdir.return_value = ['ummagumma.txt']
            def join(path, name):
                return path + name
    
            mock_os_path_join.side_effect = join
    
            mangled = 'test/ummagumma_0001.txt'
            un_mangled = 'test/' + name
            
            with patch('__builtin__.open', mocked):
                with patch('os.path.join', mock_os_path_join):
                    with patch('os.path.exists', mock_os_path_exists):
                        with patch('os.listdir', mock_os_listdir):
                            # default behavior
                            opened = storage.open(name)
                            mocked.assert_called_with(mangled, 'w')
    
                            # append, don't clobber
                            opened = storage.open(name, mode='a')
                            mocked.assert_called_with(un_mangled, 'a')
    
                            # overwrite, don't clobber
                            opened = storage.open(name, overwrite=True)
                            mocked.assert_called_with(un_mangled, 'w')
    
                            # append, give warning
                            storage._logger = MagicMock()
                            opened = storage.open(name,
                                                  overwrite=True,
                                                  mode='a')
                            mocked.assert_called_with(un_mangled, 'a')
                            storage._logger.warning.assert_called_with(AMBIGUOUS)
            return
    # end class TestFileStorageOpen
    



.. autosummary::
   :toctree: api

   TestFileStorageWith.test_with

