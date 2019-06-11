def iteration_progress(log, counter, interval, processing_group):
    if log:
        if type(processing_group) == int:
            processing_group_len = processing_group
        else:
            processing_group_len = len(processing_group)

        counter += 1
        if counter % interval == 0:
            print("Progress " + str(counter) + "/" + str(processing_group_len))

        if counter == processing_group_len:
            print("Finished " + str(counter) + "/" + str(processing_group_len))
            print()

    return counter
