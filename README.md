# swscust2ics
Convert SWSCUST timetables to ICS Calendar files

## How to
1. First, browse to your timetables website and under `MyTimetable`, select the Semester you want.
2. Make sure that `Type of Report` is set to `List` and NOT `Grid`.
3. Click `View Timetable`
4. Save the webpage as a `.html` file to the same folder as this repository.
5. From a terminal/command prompt run `./swscust2ics.py input.html output.ics` where `input.html` is whatever you saved the timetable webpage as.
6. You can now import the `output.ics` file into whatever application you want.

You'll need to do each Semester separately.
