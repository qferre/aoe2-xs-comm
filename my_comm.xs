void main() {

    // DEFINITIONS
    // NOTE: the defines here must match the ones in the config.py file!
    int NUM_VARS = 4;    // Must match Python's NUM_VARS
    int LOCK_PYTHON_DONE = 0;
    int LOCK_XS_DONE = 1;


    // Open the xsdat file corresponding to the scenario, or create it if it doesn't exist
    // NOTES:
    // - The file will have the same name as the scenario
    // - The XS script is in change of creating the file, not the Python script
    bool file_status = false;
    bool closing_status = false;
    file_status = xsOpenFile(); // NOTE : do not use xsCreateFile() here, as there is a bug if you open it in append mode


    if (file_status == false) {
        xsChatData("File was not found, creating it...");
        // Just continue the loop without reading the file. this will allow us to ensure the file is always created (by the code below)
    }
    else {

        // Read first variable, which is the lock
        xsSetFilePosition(0);
        int lock = -1;
        lock = xsReadInt();
        xsChatData("Lock = "+lock);

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
    }

    // GAMEPLAY SCRIPTING
    // Optional: Here you can do something with the values, potentially modifying them.
    // Gameplay may also modify them.
    // For example, you can set the trigger variables to the values of other trigger variables which are modified in game.
    // This will ensure that communication is synchronized, since we will only re-write the file after the lines of code here are executed.


    // Close and reopen the file to write back the values
    closing_status = xsCloseFile();
    file_status = xsCreateFile(false); // "false" means we open in write mode and not append mode, so the file will be erased at each loop and we can write the values back

    // Write the current trigger values back to the file
    if (true) { // TODO : add an additional lock before writing, so that the triggers in game gets an opportunity to modify the values before they are written again ?
        // Write back to file
        xsSetFilePosition(0);
        xsWriteInt(LOCK_XS_DONE); // Set lock to indicate XS has processed the data
        // Note: This will overwrite the previous values in the file ! It does not append.
        for (i = 0; < NUM_VARS) {
            xsWriteInt(xsTriggerVariable(i));
        }
    }


    closing_status = xsCloseFile();
    if(closing_status) {
        xsChatData("Loop complete.");
    }

    return;
}
