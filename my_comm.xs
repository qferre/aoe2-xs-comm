#include "Constants.xs"

#define NUM_VARS         4    // Must match Python's NUM_VARS
#define LOCK_FREE        0
#define LOCK_PYTHON_DONE 1
#define LOCK_XS_DONE     2



void main() {
    if (!xsOpenFile("xs_data_file.xsdat")) {
        xsChatData("ERROR: cannot open xs_data_file.xsdat");
        return;
    }

    // Read first variable, which is the lock
    xsSetFilePosition(0);
    int lock = xsReadInt();

    // Write only if the lock id free (Python thread has signaled it is done)
    if (lock == LOCK_PYTHON_DONE) {

        int values = xsArrayCreateInt(NUM_VARS, int defaultValue, string uniqueName)

        // Read values
        for (int i = 0; i < NUM_VARS; i++) {
            values[i] = xsReadInt();
        }



        // Write to trigger vars
        for (int i = 0; i < NUM_VARS; i++) {
            xsSetTriggerVariable(i, values[i]);
        }

        // Optional: invert values
        for (int i = 0; i < NUM_VARS; i++) {
            values[i] = -values[i];
        }

        // Write back to file
        xsSetFilePosition(0);
        xsWriteInt(LOCK_XS_DONE);
        for (int i = 0; i < NUM_VARS; i++) {
            xsWriteInt(values[i]);
        }
    }

    xsCloseFile();
}


// Debug print rule
rule chatAllVariables
    active
    minInterval 1
    maxInterval 1
    group chatGroup
{
    string msg = "XS VARS:";
    for (int i = 0; i < NUM_VARS; i++) {
        msg = xsAddString(msg, xsIToS(i));
        msg = xsAddString(msg, "=");
        msg = xsAddString(msg, xsIToS(values[i]));
        if (i < NUM_VARS - 1) msg = xsAddString(msg, ", ");
    }
    xsChatData(msg);
}