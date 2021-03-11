# Online-Gungi
<img width="1214" alt="Screen Shot 2021-03-11 at 12 11 32 AM" src="https://user-images.githubusercontent.com/24733269/110739294-dfb83600-81fe-11eb-9b0f-480cb6a2af57.png">

Gungi is a fictional two-player strategy game invented by Yoshihiro Togashi, creator of the popular manga series, Hunter X Hunter. This chess inspired game is taken to a new level by adding a third dimension to the gameplay by allowing pieces to stack on top of one another. While no official ruleset exists, dedicated fans attempted to make one themeselves. I would like to give a special thanks to the Hunter Hunter community for making this game possible.

## How to Play
This game is fully playable online ones own local network. To do so just change self.server in Network.py and and server in Server.py to your ipv4 address. 
After that just run Server.py and then have two runs Client.py to play. 
For the rules I mainly used https://www.docdroid.net/P4r6Fvq/gungi-pdf#page=2 as a guide with a few exceptions.
  1) I made samurai tier 2 cover the first 2 spaces in the diagnol instead of just the one.
  2) Fortresses elevate all friendly pieces within their movement range as if they were stacked directly on the fortress.
  3) After players have taken turns placing their first 18 pieces, they gain the ability to “pass” instead of placing a new piece on the 8 subsequent rounds. A player may pass multiple times in a row until either both players agree to pass,or 26 total placement rounds have been played.
  4) Pawns are able to move an extra space forward if they are in the first row of their own starting area.
  5) I adjusted some piece starting numbers (muskeeteer is now 2(+1), captain is 2(+1), and Lieutenant General is 2(-2))

## Future Plans
I intend to later add a few new features to this game in the near future. These include but are not limited to:
  1) Better graphics
  2) Online support on any network
  3) Computer AI
