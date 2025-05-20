void main() {

    // DEFINITIONS
    int NUM_VARS = 4;    // Must match Python's NUM_VARS
    int LOCK_FREE = 0;
    int LOCK_PYTHON_DONE = 1;
    int LOCK_XS_DONE = 2;

    //xsEnableRule(chatAllVariables);

    // Open the xsdat file corresponding to the scenario, or create it if it doesn't exist
    // NOTES:
    // - The file will have the same name as the scenario
    // - The XS script is in change of creating the file, not the Python script
    bool file_status = false;
    bool closing_status = false;
    file_status = xsCreateFile(true); // "true" means we open in append mode, otherwise the file will be erased at each loop


    if (file_status == false) {
        xsChatData("ERROR: cannot open the file.");
        return;
    }

    // Read first variable, which is the lock
    xsSetFilePosition(0);
    int lock = xsReadInt();

    // Write only if the lock is free (meaning the Python thread has signaled it is done)
    if (lock == LOCK_PYTHON_DONE) {

        int values_array_id = xsArrayCreateInt(NUM_VARS, -1);

        int current_value_loop = 0;

        // Read values and write to trigger variable

        for (i = 0; < NUM_VARS) {
            current_value_loop = xsReadInt();
            xsSetTriggerVariable(i, current_value_loop);
        }

        // Optional: Here you can do something with the values, potentially modifying them
        // Gameplay may also modify them

    }

    // Write the current trigger values back to the file
    if (true) { // TODO : add an additional lock before writing, so that the triggers in game gets an opportunity to modify the values before they are written again ?
        // Write back to file
        xsSetFilePosition(0);
        xsWriteInt(LOCK_XS_DONE); // Set lock to indicate XS has processed the data
        // Note: This will overwrite the previous values in the file ! It does not append.
        for (i = 0; < NUM_VARS) {
            xsWriteInt(xsTriggerVariable(i));
        }


    closing_status = xsCloseFile();

    if(closing_status) {
        xsChatData("File closed successfully.");
    }
}


// Debug print rule
rule chatAllVariables
    active
    minInterval 1
    maxInterval 1
    group chatGroup
{
    for (i = 0; < NUM_VARS) {
        xsChatData("TV "+i+" = "+xsTriggerVariable(i));
    }
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

