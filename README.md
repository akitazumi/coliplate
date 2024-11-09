# coliplate
python for RGB detection from coliplates

# user instruction

don't use iphone, use regular cameras
pictures should be straight 


# notes  
v02.py fixed the RGB reverse order, not BGR anymore, and RGB output format is tab delim. <br/>
also takes in number of points to pick and filename from users $python v02.py pic1.jpg -points 500 <br/>
basename is pic1 and should output: <br/>
1. {basename}_cropped.jpg for removing the edges of plates assuming users submit nice picture <br/>
2. {basename}_wells.jpg to confirm that the well grid is not off <br/>
3. {basename}_points.jpg showing where it was picked,  <br/>
4. {basename}_cols.txt for all values, same as stdout <br/>
needs more work as discussed in the meeting but uploading for a record and for sake of Friday ;) <br/>

v01.py had extra PIL conversion that i thought i needed for RGB consistency between java and python, but based on the feedback that the values were consistent already, im removing the conversion. now it runs without errors. 
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
