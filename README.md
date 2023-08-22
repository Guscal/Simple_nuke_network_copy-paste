# Simple nuke network copy paste
a network copy paste to send and recibe nodes  inside of nuke.

dont hesitate to leave feedback or what improvements i could do.
  

# v1.1.0 - nuke 13 and up


  # change log
  
  moved the user and ip config to an .json file
  added adavanced options to edit users directly in nuke
  
  # setup
  
  
  before running the code open it in your IDE of preference or notepad haha.
  edit the network path your network path.
  
  ![image](https://github.com/Guscal/Simple_nuke_network_copy-paste/assets/57334994/8b2d4dfe-540a-4ee1-b8f2-7c01ac37711e)
  

  
  then add the name of your users and their local ipv4 if you have ethernet connected use that ipv4 instead.
  
  this setup is very manual so it might be better suited for really small teams/studios but im working in a more elegant solution for maintainability and scalability.
  
  ![image](https://github.com/Guscal/Simple_nuke_network_copy-paste/assets/57334994/140aba2d-0dab-41b9-93c3-98f832669d1c)


  # install

  
  drop the .py file inside of your .nk folder usually in C:\Users\User\ .nuke or in your network .nk, Drive:\Network\Path\ .nk.
  
  open your menu.py located in C:\Users\User\ .nuke or Drive:\Network\Path\ .nk, if menu.py does not exist just create it.

  inside the menu py add the following lines 


```python
import Networkcopy
​
# Add commands to the Nuke's main menu`
nuke.menu('Nodes').addCommand('Custom/Copy to User', 'Networkcopy.display_user_selection_dialog()', "ctrl+alt+c")
nuke.menu('Nodes').addCommand('Custom/Paste', 'Networkcopy.paste_nodes_from_network()', "ctrl+alt+v") "
```
or if the code is located in a network path

```python

import sys

sys.path.append('/some/network/path')

import Networkcopy
​
# Add commands to the Nuke's main menu`
nuke.menu('Nodes').addCommand('Custom/Copy to User', 'Networkcopy.display_user_selection_dialog()', "ctrl+alt+c")
nuke.menu('Nodes').addCommand('Custom/Paste', 'Networkcopy.paste_nodes_from_network()', "ctrl+alt+v") "
```
# use
after install open nuke

select some nodes, hit the shorcut `ctrl+alt+c` and you should be presented with this window

![image](https://github.com/Guscal/Simple_nuke_network_copy-paste/assets/57334994/3a81b940-1942-426a-9e07-9e64378aed1b)

select a user to send the nodes

and they should be able o hit `ctrl+alt+v` and paste the sended nodes.

done! be happy :)




