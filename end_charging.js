// 1) get commandline arguments:
//     - the drone's ethereum address,
//     - the station's eth address,
//     - the start of the timeslot in seconds (unix time)
// 2) interact with the booking function of the station's contract
// 3) wait for the new booking event
// 4) Return 0 if booking is o.k., return 1 if not