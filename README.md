# coliplate
python for RGB detection from coliplates

# user instruction

don't use iphone, use regular cameras
pictures should be straight 

# powerpoint records
for screenshot and memo: https://ars-usda.box.com/s/ddqe6xd6qgn7imjhopgu2oqt07sfx85k<br/>

# python dependencies
cv2 version: 4.10.0<br/>
numpy version: 1.26.4<br/>
and standard library modules: random, argparse, os, statistics<br/>
currently testing with python 3.11.7<br/>


# v03
included ave and stdev, for all wells or just left half and right half<br/>
individual well colors are in {basename}_cols.txt as previously<br/>
and additional file {basename}_stats.txt has this 6 lines for lightness and 9 line for color stat output:<br/>
<br/>

| --- | --- | --- | --- | --- |
| pic5.jpg | points=500 | lightness | center.wells | 137.28 |
| pic5.jpg | points=500 | lightness | top.edge | 156.86 |
| pic5.jpg | points=500 | lightness | bottom.edge | 155.65 |
| pic5.jpg | points=500 | lightness | left.edge | 174.69 |
| pic5.jpg | points=500 | lightness | right.edge | 180.21 |
| pic5.jpg | points=500 | lightness | all.edge | 166.85 |
| pic5.jpg | points=500 | Average.RGB | all | 146 | 170 | 49 | "#92aa31" |
| pic5.jpg | points=500 | Stdev.RGB.-2SD | all | 99 | 143 | 6 | "#638e06" |
| pic5.jpg | points=500 | Stdev.RGB.+2SD | all | 193 | 197 | 92 | "#c0c55b" |
| pic5.jpg | points=500 | Average.RGB | left | 135 | 161 | 40 | "#87a128" |
| pic5.jpg | points=500 | Stdev.RGB.-2SD | left | 101 | 139 | 22 | "#648b15" |
| pic5.jpg | points=500 | Stdev.RGB.+2SD | left | 169 | 183 | 58 | "#a9b63a" |
| pic5.jpg | points=500 | Average.RGB | right | 155 | 175 | 56 | "#9baf38" |
| pic5.jpg | points=500 | Stdev.RGB.-2SD | right | 108 | 151 | 13 | "#6b970c" |
| pic5.jpg | points=500 | Stdev.RGB.+2SD | right | 202 | 199 | 99 | "#cac663" |

# v02
v02.py fixed the RGB reverse order, not BGR anymore, and RGB output format is tab delim. <br/>
also takes in number of points to pick and filename from users $python v02.py pic1.jpg -points 500 <br/>
basename is pic1 and should output: <br/>
1. {basename}_cropped.jpg for removing the edges of plates assuming users submit nice picture <br/>
2. {basename}_wells.jpg to confirm that the well grid is not off <br/>
3. {basename}_points.jpg showing where it was picked,  <br/>
4. {basename}_cols.txt for all values, same as stdout <br/>
needs more work as discussed in the meeting but uploading for a record and for sake of Friday ;) <br/>

# v01
v01.py had extra PIL conversion that i thought i needed for RGB consistency between java and python, but based on the feedback that the values were consistent already, im removing the conversion. now it runs without errors. <br/>
v01.py from 11/06/24, discussed on 11/07/24, for full-skirted plate with circular 96 wells <br/>
see Atharva's summary in discussion for details and more<br/><br/>
-needs RGB in 3 columns and reverse orders <br/>
-add median per area (left/right/user-defined) <br/>
-get date and add to txt file <br/>
-users-defined pick number <br/>
-take in layout from user somehow <br/>
-heat source variation warning "avoid edges" <br/>
-add camera instruction <br/>
-can it accommodate different plates square/circle wells <br/>
