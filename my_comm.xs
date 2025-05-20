void main() {

    // DEFINITIONS
    int NUM_VARS = 4;    // Must match Python's NUM_VARS
    int LOCK_PYTHON_DONE = 0;
    int LOCK_XS_DONE = 1;



    //xsEnableRule(chatAllVariables);

    // Open the xsdat file corresponding to the scenario, or create it if it doesn't exist
    // NOTES:
    // - The file will have the same name as the scenario
    // - The XS script is in change of creating the file, not the Python script
    bool file_status = false;
    bool closing_status = false;
    file_status = xsCreateFile(true); // "true" means we open in append mode, so the file will not be erased at each loop and we can read the values written by Python



    if (file_status == false) {
        xsChatData("ERROR: cannot open the file.");
        return;
    }

    // Read first variable, which is the lock
    xsSetFilePosition(0);
    int lock = -6666;
    lock = xsReadInt();
    xsChatData("Lock = "+lock);

    // BUG : Python can read what I'm writing just fine, but xscript does not understand the lock ? It thinks it's -1 ?

    // Read only if the lock is free (meaning the Python thread has signaled it is done)
    if (lock == LOCK_PYTHON_DONE) {
        xsChatData("Reading...");

        int values_array_id = xsArrayCreateInt(NUM_VARS, -1);

        int current_value_loop = -1;

        // Read values and write to trigger variable

        for (i = 0; < NUM_VARS) {
            current_value_loop = xsReadInt();
            xsChatData("Read value "+i+" = "+current_value_loop);
            xsSetTriggerVariable(i, current_value_loop);
        }


    }

    // Optional: Here you can do something with the values, potentially modifying them
    // Gameplay may also modify them

    // For now, we just print them to the chat
    for (i = 0; < NUM_VARS) {
        //xsChatData("TV "+i+" = "+xsTriggerVariable(i));
    }


    // Close and reopen the file to write back the values
    //closing_status = xsCloseFile();
    //file_status = xsCreateFile(false); // "false" means we open in write mode, so the file will be erased at each loop and we can write the values back

    // Write the current trigger values back to the file
    if (true) { // TODO : add an additional lock before writing, so that the triggers in game gets an opportunity to modify the values before they are written again ?
        // Write back to file
        xsSetFilePosition(0);
        xsWriteInt(LOCK_XS_DONE); // Set lock to indicate XS has processed the data
        // Note: This will overwrite the previous values in the file ! It does not append.
        for (i = 0; < NUM_VARS) {
            
            // TODO Do not write anyhting for now, just to test the file writing
            xsWriteInt(i*10); // TODO : write the trigger variable instead of i*10
            //xsWriteInt(xsTriggerVariable(i)); /// TODO : trigger variables seem to be MUCH larger than a simple int, so we need to convert them to int first
        }
    }


    closing_status = xsCloseFile();

    if(closing_status) {
        xsChatData("Loop complete.");
    }

    return;
}









// THIS WORKED
// void test_file_write() {

//     int a = 100;
//     int b = 200;
//     bool file_status = false;
//     bool closing_status = false;

//     file_status = xsCreateFile(append = true); //Note : the file will have the same name as the scenario
//     // IMPORTANT : open in append mode, otherwise the file will be overwritten
//     // For us : C:\Users\Quentin\Games\Age of Empires 2 DE\76561198007343704\profile\Testing_MODIFIED.xsdat

//     //xsOpenFile("testing_file_write.xsdat");

//     xsSetFilePosition(0); // Go to the beginning of the file

//     xsWriteInt(a);
//     xsWriteInt(b);

//     closing_status = xsCloseFile();

//     if(closing_status) {
//         xsChatData("File written successfully.");
//     }

// }

