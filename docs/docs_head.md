# Wood Trains Documentation

## Usage

**Track Layout Tools**
- Adding Track Pieces
- Automatic Layout
  - Adjusting the current track flow direction
  - Adjusting the current Peg
- Adjusting Track position
  - "Nudging" a Track position
  - Using Maya's manipulators

## Troubleshooting
##### My track isn't linking!
##### My train isn't moving
##### My train keeps breaking into pieces
##### My train keeps reversing

## Caveats
- This is primarily a toy, not a commercial product.  There are shortcomings and pitfalls.  You're welcome to a full refund at any time.
- Like most animation tools, it works only within certain limits and boundaries.  Clearly there are track configurations that cause it to break.  That's partly why the "train reset" tools exist to be easy to use.
- Maya's performance tools try hard never to re-evaluate the same thing twice.  The script for this simulator predates most of those tools, and explicitly re-evaluates everything.  So the frame-rate performance will be slower than more modern rigs.  Maya Evaluation Manager will skip evaluating the trains.  This simulator sets the evaluation mode back to the base line `DG Mode` to force evaluation.  This will result in losing all of the performance benefit of the Evaluation Manager, Animation Caching, and other tools.
- Maya will re-use the result of a frame if it doesn't believe that anything has changed (and this simulator doesn't notify Maya that anything relevant has changed).  So it's best to set the animation playback range to an absurdly high number like 10,000 frames so that the playback never has to loop back to the same frame numbers again.  

## Under the Hood

Behind the scenes, this simulator is very simple.  At each frame an expression triggers part of the `track.py` module to move all of the trains.  Each train is some geometry and transform nodes constrained to a set of locators (one point constraint and an aim constraint for each train car).

#### Track and Parametric Curves
Each Track piece has a parametric curve embedded in it for each possible route a train can take along it.  This is usually just one route, but some tracks have several.  Each parametric curve has **Pegs** at each endpoint.  During the **Linking** process, these Pegs are associated with their neighboring Pegs.  The DAG path to the neighboring peg is stored as a string attr on peg, for each neighbor.  

Parametric curves are all directional, and some care is taken to annotate the orientation of the curve within the piece by the names of the Pegs.  Pegs will end in a 1 or a 0 denoting which end of their associated parameter curve they are located at.  (femalePegA**0**`)

The wooden interlocking element of the track geometry also carries a directionality to it (denoted by female/male peg designations), but this is only relevant to the track layout toolkit, not the simulator step. (**female**PegA0`)

Pegs also have capital letters designating which of the parameter curves they are an endpoint for (femalePeg**A**0).  For switch-tracks, this notifies the simulator to query the track among the multiple curve options (femalePeg**ABC**0).  For cross-tracks, this keeps the two independent curves separated, so an incoming train will stay on the correct path through the Track: (femalePeg**A0** <-> femalePeg**A1**,  malePeg**B0** <-> malePeg**B1**).  The **A** track Pegs stay together, and the **B** track Pegs stay together.

The simulation step for each train moves each locator by some speed/distance along its current curve.  When the needed next step would carry a locator beyond the end of its current curve, the simulator queries the **Peg** at the upcoming endpoint to see which (if any) Track piece is next.  If there is a next piece, then the locator is moved the relevant remaining distance along this new track.  (This train/track hand-off logic process is the part that I'm most proud of in this project.)

#### Linking
The **Linking** process is straightforward.  It's a quick game of "Everyone try to hold hands".  
- Make a list of every Peg in the scene and erase any pair assignments on them all.  
- Loop over each Peg, and see if there is a Peg from a _different_ track piece that is both near enough to it and wooden-peg compatible with it.  
  - If so, pair those two pegs (store their names on the other peg).  
- If there are any pegs _without_ a pair buddy, add a scene annotation marker to raise them to the attention of the user.   
  - unpaired Track Pegs are not a problem in the simulator at all.  The trains just treat them as a track terminus and reverse direction.  But unpaired Tracks frequently result from track pieces that aren't quite aligned successfully, so it's polite to inform the user in case the intent was to connect that track.
  
## FAQ
  
**BRIO, not Thomas?**
I prefer Scandinavian mid-century modern minimalism to the creepy anthropomorphism of souls trapped in transportation equipment; eternally doomed like Sisyphus to eternally orbit their island prison.  Working hard, and accomplishing nothing.  

But, to each their own.  The art assets of this project can be extended to include other trains and tracks.  
