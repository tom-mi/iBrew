# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(0, 5, 0, 0),
    prodvers=(0, 5, 0, 1),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Tristan Crispijn'),
        StringStruct(u'FileDescription', u'iBrew'),
        StringStruct(u'FileVersion', u'0.5.0.0 (The conundrum struggle)'),
        StringStruct(u'InternalName', u'ibrew'),
        StringStruct(u'LegalCopyright', u'© Tristan Crispijn. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'ibrew'),
        StringStruct(u'ProductName', u'iBrew: The conundrum struggle'),
        StringStruct(u'ProductVersion', u'0.5.0.1')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
