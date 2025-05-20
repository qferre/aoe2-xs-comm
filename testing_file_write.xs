void test_file_write() {

    int a = 100;
    int b = 200;
    bool file_status = false;
    bool closing_status = false;

    file_status = xsCreateFile(); //Note : the file will have the same name as the scenario
    // For us : C:\Users\Quentin\Games\Age of Empires 2 DE\76561198007343704\profile\Testing_MODIFIED.xsdat

    //xsOpenFile("testing_file_write.xsdat");

    xsSetFilePosition(0);

    xsWriteInt(a);
    xsWriteInt(b);

    closing_status = xsCloseFile();

    if(closing_status) {
        xsChatData("File written successfully.");
    }

}

